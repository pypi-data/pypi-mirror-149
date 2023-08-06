# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base
from ..models import User
from ..utils.exceptions import (
    GetComponentError,
    AddComponentError,
    UpdateComponentError
)


class Users(Base):

    """Used to sync users from a source instance to a destination instance of Swimlane
    """

    def __process_user(self, user: User):
        if user.roles:
            self.__logger.info(f"Processing roles for user '{user.name}'")
            role_list = []
            from .roles import Roles
            for role in user.roles:
                _role = Roles().sync_role(role=role)
                if _role:
                    role_list.append(_role)
            user.roles = role_list
        if user.groups:
            self.__logger.info(f"Processing groups for user '{user.name}'")
            group_list = []
            from .groups import Groups
            for group in user.groups:
                _group = Groups().sync_group(group=group)
                if _group:
                    group_list.append(_group)
            user.groups = group_list
        return user

    def sync_user(self, user_id):
        user = self.source_instance.get_user(user_id)
        if not user:
            raise GetComponentError(type='User', id=user_id)
        if user and not self._is_in_include_exclude_lists(user.displayName, 'users'):
            if user.displayName != self.source_instance.swimlane.user.display_name:
                self.__logger.info(f"Attempting to sync user '{user.displayName}' on destination.")
                dest_user = self.destination_instance.search_user(user.displayName)
                if not dest_user:
                    if Base.live:
                        self.__logger.info(f"Adding new user '{user.displayName}' to destination.")
                        dest_user = self.destination_instance.add_user(user)
                        if not dest_user:
                            raise AddComponentError(model=user, name=user.displayName)
                        self.__logger.info(f"Successfully added user '{user.displayName}' to destination.")
                        return dest_user
                    else: self.add_to_diff_log(user.displayName, 'added')
                else:
                    self.__logger.info(f"User '{user.displayName}' exists on destination.")
                    user = self.__process_user(user=user)
                    if Base.live:
                        user.id = dest_user.id
                        dest_user = self.destination_instance.update_user(dest_user.id, user)
                        if not dest_user:
                            raise UpdateComponentError(model=user, name=user.displayName)
                        self.__logger.info(f"Successfully updated user '{user.displayName}' on destination.")
                        return dest_user
                    else: self.add_to_diff_log(user.displayName, 'updated')
            else:
                self.__logger.info(f"Unable to update the currently authenticated user '{self.source_instance.swimlane.user.display_name}'. Skipping...")

    def sync(self):
        """This method is used to sync all users from a source instance to a destination instance
        """
        self.__logger.info(f"Attempting to sync users from '{self.source_host}' to '{self.dest_host}'")
        users = self.source_instance.get_users()
        if users:
            for user in users:
                self.sync_user(user_id=user.id)
