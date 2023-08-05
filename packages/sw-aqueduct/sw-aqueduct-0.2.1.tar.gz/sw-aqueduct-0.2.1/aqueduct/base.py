# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from collections.abc import Iterable
from .utils.logger import LoggingBase
import inspect


class Base(metaclass=LoggingBase):

    source_instance = None
    destination_instance = None
    remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']
    group_exclusions = ['Everyone']
    role_exclusions = ['Administrator']
    live = None
    _diff_log = {}
    source_host = None
    dest_host = None
    offline = False
    update_reports = False
    update_dashboards = False
    continue_on_error = False
    include = None
    exclude = None
    __diff_types = [
        'added',
        'updated',
        'upgraded',
        'removed'
    ]

    def add_to_diff_log(self, name, type, subcomponent=None, value=None):
        if type in self.__diff_types:
            component = None
            parent = inspect.stack()[1][0].f_locals.get('self', None)
            component = parent.__class__.__name__
            if not self._diff_log.get(component):
                self._diff_log[component] = {}
            if not self._diff_log[component].get(name):
                self._diff_log[component][name] = []
            if subcomponent:
                self._diff_log[component][name].append({
                    subcomponent: {
                        type: value
                    }
                })
                getattr(parent, f'_{component}__logger').info(f"Dry Run: Component '{component}' named '{name}' with subcomponent '{subcomponent}' with value of '{value if value else ''}' would have been {type} on destination.")
            else:
                self._diff_log[component][name].append(type)
                getattr(parent, f'_{component}__logger').info(f"Dry Run: Component '{component}' named '{name}' would have been {type} on destination.")
        else:
            raise ValueError(f"Unknown type of '{type}' provided. Cannot add to diff log...")

    def log_exception(self, val, level='error'):
        getattr(self.__logger, level)(val)

    def _is_in_include_exclude_lists(self, name, type):
        if self.exclude and self.exclude.get(type) and name in self.exclude[type]:
            self.__logger.info(f"{type.capitalize()} '{name}' in exclude list. Skipping...")
            return True
        if self.include and self.include.get(type) and name not in self.include[type]:
            self.__logger.info(f"{type.capitalize()} '{name}' is not in include list. Skipping...")
            return True
        return False

    def canonicalize(self, x):
        if isinstance(x, dict):
            x = sorted((self.canonicalize(k), self.canonicalize(v)) for k, v in x.items())
        elif isinstance(x, Iterable) and not isinstance(x, str):
            x = sorted(map(self.canonicalize, x))
        else:
            try:
                bool(x < x) # test for unorderable types like complex
            except TypeError:
                x = repr(x) # replace with something orderable
        return x

    def scrub(self, obj, bad_key="$type"):
        """Used to remove a specific provided key from a dictionary
        that may contain both nested dictionaries and lists.
        
        This method is recurisve.

        Args:
            obj (dict): A dictionary or list to remove keys from.
            bad_key (str, optional): The bad key to remove from the provided dict or list. Defaults to "$type".
        """
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key == bad_key:
                    del obj[key]
                else:
                    self.scrub(obj[key], bad_key)
        elif isinstance(obj, list):
            for i in reversed(range(len(obj))):
                if obj[i] == bad_key:
                    del obj[i]
                else:
                    self.scrub(obj[i], bad_key)
        else:
            pass
