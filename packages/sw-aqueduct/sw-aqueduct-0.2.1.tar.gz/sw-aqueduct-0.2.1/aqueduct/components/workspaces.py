# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base
from ..models import Workspace
from ..utils.exceptions import (
    AddComponentError,
    UpdateComponentError
)

class Workspaces(Base):

    """Used to sync workspaces from a source instance to a destination instance of Swimlane
    """

    def sync_workspace(self, workspace: Workspace):
        if not self._is_in_include_exclude_lists(workspace.name, 'workspaces'):
            self.__logger.info(f"Processing workspace '{workspace.name}'")
            dest_workspace = self.destination_instance.get_workspace(workspace.id)
            if not dest_workspace:
                if Base.live:
                    self.__logger.info(f"Adding workspace '{workspace.name}' to destination.")
                    dest_workspace = self.destination_instance.add_workspace(workspace)
                    if not dest_workspace:
                        raise AddComponentError(model=workspace, name=workspace.name)
                    self.__logger.info(f"Successfully added workspace '{workspace.name}' to destination.")
                else: self.add_to_diff_log(workspace.name, 'added')
            else:
                if workspace.uid == dest_workspace.uid:
                    self.__logger.info(f"Workspace '{workspace.name}' already exists on destination. Checking differences...")
                    the_same = True
                    for key in ['uid', 'id', 'name', 'description', 'dashboards', 'applications']:
                        if hasattr(workspace, key) and hasattr(dest_workspace, key):
                            if getattr(workspace, key) != getattr(dest_workspace, key):
                                the_same = False
                        elif hasattr(workspace, key) and not hasattr(dest_workspace, key) or not hasattr(workspace, key) and hasattr(dest_workspace, key):
                            the_same = False
                    if not the_same:
                        if Base.live:
                            self.__logger.info(f"The source and destination workspace '{workspace.name}' are not the same. Updating...")
                            dest_workspace = self.destination_instance.get_workspace(workspace.id)
                            dashboards = []
                            for dashboard in dest_workspace.dashboards:
                                if self.destination_instance.get_dashboard(dashboard_id=dashboard):
                                    dashboards.append(dashboard)
                            workspace.dashboards = dashboards
                            from .applications import Applications
                            for application_id in workspace.applications:
                                if application_id not in self.destination_instance.application_id_list:
                                    Applications().sync_application(application_id=application_id)
                            resp = self.destination_instance.update_workspace(workspace_id=workspace.id, workspace=workspace)
                            if not resp:
                                raise UpdateComponentError(model=workspace, name=workspace.name)
                            self.__logger.info(f"Successfully updated workspace '{workspace.name}' on destination.")
                        else: self.add_to_diff_log(workspace.name, 'updated')
                    else:
                        self.__logger.info(f"The source and destination workspace '{workspace.name}' are the same. Skipping...")

    def sync(self):
        """This method is used to sync all workspaces from a source instance to a destination instance
        """
        self.__logger.info(f"Starting to sync workspaces from '{self.source_host}' to '{self.dest_host}'")
        workspaces = self.source_instance.get_workspaces()
        if workspaces:
            for workspace in workspaces:
                self.sync_workspace(workspace=workspace)
