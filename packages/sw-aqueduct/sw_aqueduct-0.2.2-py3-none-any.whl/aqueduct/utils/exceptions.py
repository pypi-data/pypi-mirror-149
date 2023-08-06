# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from ..models import (
    Application,
    Asset,
    Group,
    Package,
    Report,
    Role,
    Workflow,
    Workspace,
    Dashboard,
    Plugin,
    Task,
    User
)


class UnsupportedSwimlaneVersion(NotImplementedError):
    """
    Raised when a source and destination Swimlane instance do not match
    """
    def __init__(self, source, destination) -> None:
        from ..base import Base
        message = f"The source instance ({source.swimlane.host}) version {source.swimlane.product_version} and destination instance ({destination.swimlane.host}) version {destination.swimlane.product_version} must be the same version to continue."
        Base().log_exception(
            val=message,
            level='critical'
        )
        super(UnsupportedSwimlaneVersion, self).__init__(message)

class ModelError(TypeError):

    """
    Raised when a provided dictionary does not comform to the defined data model for that object
    """
    def __init__(self, err: TypeError, name: str):
        from ..base import Base
        message = f"The provided dictionary object to the '{name}' data model is {str(err).split('()')[-1]}"
        Base().log_exception(
            val=message,
            level='critical'
        )
        super(ModelError, self).__init__(message)


class ComponentError(Exception):

    """
    Raised when an error has occurred within a component class of aqueduct.
    """


class AddComponentError(ComponentError):
    """
    Raised when an error occurrs attempting to add a component from a source Swimlane instance to a destination instance
    
    Attributes:
        model (Application or Asset or Group or Package or Report or Role or Workflow or Workspace or Dashboard or Plugin or Task or User): An aqueduct model object
    """

    def __init__(self, model: Application or Asset or Group or Package or Report or Role or Workflow or Workspace or Dashboard or Plugin or Task or User or dict, name: str = None):
        from ..base import Base
        message = f"Unable to add {name if name else model.__class__.__name__} '{model.get('name') if isinstance(model, dict) else model.name}' to destination instance!!"
        Base().log_exception(
            val=message,
            level='critical'
        )
        super(AddComponentError, self).__init__(message)


class UpdateComponentError(ComponentError):
    """
    Raised when an error occurrs attempting to update an existing component from a source Swimlane instance to a destination instance
    
    Attributes:
        model (Application or Asset or Group or Package or Report or Role or Workflow or Workspace or Dashboard or Plugin or Task or User): An aqueduct model object
    """

    def __init__(self, model: Application or Asset or Group or Package or Report or Role or Workflow or Workspace or Dashboard or Plugin or Task or User or dict, name: str = None):
        from ..base import Base
        message = f"Unable to update {name if name else model.__class__.__name__} '{model.get('name') if isinstance(model, dict) else model.name}' on destination instance!!"
        Base().log_exception(
            val=message,
            level='critical'
        )
        super(UpdateComponentError, self).__init__(message)


class GetComponentError(ComponentError):
    """
    Raised when an error occurrs attempting to get a component from a source Swimlane instance
    
    Attributes:
        model (Application or Asset or Group or Package or Report or Role or Workflow or Workspace or Dashboard or Plugin or Task or User): An aqueduct model object
    """

    def __init__(self, type: str, name: str = None, id: str =None):
        from ..base import Base
        message = f"Unable to find {type} {name if name else ''} '({id})' on source Swimlane instance!!"
        Base().log_exception(
            val=message,
            level='critical'
        )
        super(GetComponentError, self).__init__(message)
