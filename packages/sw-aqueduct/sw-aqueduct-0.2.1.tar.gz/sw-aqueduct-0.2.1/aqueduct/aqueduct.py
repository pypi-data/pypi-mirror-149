# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from base64 import b64decode
from collections import OrderedDict

from . import __meta__
from .base import Base
from .instance import SwimlaneInstance
from .utils.exceptions import UnsupportedSwimlaneVersion
from .components import (
    Applications,
    Assets,
    Dashboards,
    Groups,
    KeyStore,
    Packages,
    Plugins,
    Reports,
    Roles,
    Tasks,
    Users,
    Workspaces
)


COMPONENTS = OrderedDict([
    ('keystore', KeyStore),
    ('packages', Packages),
    ('plugins', Plugins),
    ('assets', Assets),
    ('workspaces', Workspaces),
    ('applications', Applications),
    ('tasks', Tasks),
    ('reports', Reports),
    ('dashboards', Dashboards),
    ('users', Users),
    ('groups', Groups),
    ('roles', Roles)
])


class Aqueduct(Base):

    """Aqueduct is used to migrate content from one Swimlane instance to another.
    """

    def __init__(self, source: SwimlaneInstance, 
                       destination: SwimlaneInstance, 
                       live: bool = False,
                       offline: bool = False, 
                       update_reports: bool = False, 
                       update_dashboards: bool = False, 
                       continue_on_error: bool = False,
                       use_unsupported_version: bool = False,
                       force_unsupported_version: bool = False
                ):
        """To use aqueduct you must provide two SwimlaneInstance objects. One is the source of content wanting to migrate.
        The other is the destination of where the content will be migrated to.

        Args:
            source (SwimlaneInstance): The source Swimlane instance. Typically this is considered a development instance.
            destination (SwimlaneInstance): The destination Swimlane instance. Typically this is considered a production instance.
            live (bool): Whether or not this run of aqueduct is a live migration or not. Default is False.
            offline (bool): Whether or not the destination is considered offline. Default is False
            update_reports (bool): Whether or not to force update reports if changes are detected. Default is False.
            update_dashboards: (bool): Whether or not to force update dashboards if changes are detected. Default is False.
            continue_on_error: (bool): Whether or not to continue when an API error occurs. Default is False.
            use_unsupported_version: (bool): Whether or not to transfer content from one version Swimlane to a different version of Swimlane. Use this at your own risk. Default is False.
            force_unsupported_version: (bool): Whether or not to force usage of an unsupported version. This is used when running aqueduct headless/non-interactive. Default is False.
        """
        if use_unsupported_version:# and source.swimlane.product_version != destination.swimlane.product_version:
            self.__logger.warning(f"You specified you want to transfer of content from version {source.swimlane.product_version} to {destination.swimlane.product_version}. This is not officially supported. Please use at your own risk.")
            if not force_unsupported_version and not self.__want_to_continue():
                exit()
        elif source.swimlane.product_version != destination.swimlane.product_version:
            raise UnsupportedSwimlaneVersion(source=source, destination=destination)
        Base.source_instance = source
        Base.destination_instance = destination
        Base.live = live
        Base.source_host = Base.source_instance.swimlane.host
        Base.dest_host = Base.destination_instance.swimlane.host
        Base.offline = offline
        Base.update_reports = update_reports
        Base.update_dashboards = update_dashboards
        Base.continue_on_error = continue_on_error

    def __want_to_continue(self):
        response = input('Do you want to continue (y or n): ')
        if response.capitalize()[0] == 'N':
            return False
        elif response.capitalize()[0] == 'Y':
            return True
        else:
            self.__want_to_continue()

    def __sort_sync_order(self, components: list):
        ordered = []
        for key,val in COMPONENTS.items():
            if key in components:
                ordered.append(key)
        return ordered

    def sync(self, components=COMPONENTS, exclude: dict = {}, include: dict = {}):
        """The main method to begin syncing components from one Swimlane instance to another.

        There are several available components you can specify. The order of these components if forced. The defaults are:

        * keystore
        * packages
        * plugins
        * assets
        * workspaces
        * applications (we update workflows here)
        * tasks
        * reports
        * dashboards
        * users
        * groups
        * roles

        You can include and exclude specific component items like specific applications, tasks, plugins, etc. To do so
        provide a dictionary for each argument (include or exclude). For example:

        exclude = {'applications': ["Phishing Triage"], 'tasks': ['PT - Get Emails'], etc.}
        include = {'applications': ["Security Alert & Incident Management"], 'reports': ['SAIM - New Incidents'], etc.}

        aq.sync(include=include, exclude=exclude)

        Args:
            components (list, optional): A list of one or more components to sync. Defaults to COMPONENTS.
        """
        Base.include = include
        Base.exclude = exclude
        for component in self.__sort_sync_order(components):
            if COMPONENTS.get(component):
                getattr(COMPONENTS[component](), 'sync')()
        if not Base.live:
            return Base._diff_log
        print(b64decode(__meta__.__logo__).decode('ascii'))
