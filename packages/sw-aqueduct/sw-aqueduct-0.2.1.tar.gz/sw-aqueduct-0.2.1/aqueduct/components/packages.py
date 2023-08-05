# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..base import Base
from ..models import Package


class Packages(Base):

    """Syncs Python packages from a source instance to destination. 
    This class can transfer packages directly using the offline switch when creating
    an Aqueduct object.
    """

    def __set_dest_packages(self):
        if not hasattr(self, '__dest_packages'):
            dest_packages = self.destination_instance.get_pip_packages()
            if dest_packages:
                self.__dest_packages = [x.name for x in dest_packages]
            else: self.__dest_packages = None

    def _install_wheels(self, package: Package):
        """Used to install wheels directly from one Swimlane instance to another.

        This is considered an offline installation. To use this method please provide
        offline=True when instantiating the Aqueduct class.

        Args:
            package (Package): A Swimlane Package data model
        """
        if package.fileId:
            self.__logger.info(f"Attempting to transfer wheels for package '{package.name}'")
            filename = f"{package.name}-{package.version.capitalize()}-py3-none-any.whl"
            self.__logger.info(f"Downloading package '{package.name}' version '{package.version}' from source.")
            stream = self.source_instance.download_plugin(file_id=package.fileId)
            self.__logger.info(f"Successfully downloaded '{package.name}' from source.")

            self.__logger.info(f"Uploading package '{package.name}' to destination.")
            try:
                data = {"pythonVersion": package.pythonVersion.capitalize()}
                
                self.destination_instance.install_package_offline(
                    filename=filename,
                    stream=stream,
                    data=data
                )
                self.__logger.info(f"Successfully uploaded package '{package.name}' to destination.")
            except:
                self.__logger.info(F"Error occurred when trying to upload wheels for package '{package.name}' to destination. Please install manually!!")
        else:
            self.__logger.info(f"Unable to transfer wheel package '{package.name}' to destination. Must install manually!!")

    def sync_package(self, package: Package):
        """Syncs a single Python package object based on the Swimlane exported dictionary

        Args:
            package (Package): A Swimlane Python package model definition.
        """
        if not self._is_in_include_exclude_lists(package.name, 'packages'):
            self.__logger.info(f"Processing package '{package.name}'")
            self.__set_dest_packages()
            if package.name not in self.__dest_packages:
                if Base.live:
                    self.__logger.info(f"Installing {package.pythonVersion} package '{package.name}=={package.version}' on destination.")
                    if Base.offline:
                        self._install_wheels(package=package)
                    else:
                        try:
                            resp = self.destination_instance.install_package(package=package)
                        except:
                            self.__logger.info(f"Unable to install {package.pythonVersion} package '{package.name}=={package.version}' on destination. Please install manually...")
                            resp = None
                        if resp:
                            self.__logger.info(f"Successfully installed {package.pythonVersion} package '{package.name}=={package.version}' on destination.")
                else:
                    self.add_to_diff_log(package.name, 'added')
            else:
                self.__logger.info(f"Plugin '{package.name}' already exists on destination '{self.dest_host}'. Skipping....")

    def sync(self):
        """Sync will sync all installed Python packages on a source system with a destination system. 
        If you specified the `offline` switch as `True` then it will transfer the packages directly and 
        install them manually instead of relying on Swimlane to install them from pypi.
        """
        self.__logger.info(f"Attempting to sync packages from '{self.source_host}' to '{self.dest_host}'")
        self.__set_dest_packages()
        packages = self.source_instance.get_pip_packages()
        if packages:
            for package in packages:
                self.sync_package(package=package)
