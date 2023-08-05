# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import AnyStr
from attr import (
    define,
    field
)


@define
class Descriptor:
    type: AnyStr = field()
    base64Image: AnyStr = field()
    family: AnyStr = field()
    version: AnyStr = field()
    description: AnyStr = field()
    testScript: AnyStr = field()
    testScriptFile: AnyStr = field()
    pythonVersion: AnyStr = field()
    imageId: AnyStr = field()
    name: AnyStr = field()
    disabled: bool = field()
    id: AnyStr = field()
    inputParameters: dict = field(default={})
    packageDescriptor: dict = field(default={})

    def __init__(self, **kwargs):
        from ..base import Base
        from ..utils.exceptions import ModelError
        Base().scrub(kwargs)
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            raise ModelError(err=te, name='Descriptor')

    def __attrs_post_init__(self):
        if self.packageDescriptor:
            from .plugin import Plugin
            try:
                self.packageDescriptor = Plugin(**self.packageDescriptor)
            except Exception as e:
                pass


@define
class Asset:
    type: AnyStr = field()
    pythonVersion: AnyStr = field()
    valid: bool = field()
    uid: AnyStr = field()
    version: int = field()
    id: AnyStr = field()
    name: AnyStr = field()
    disabled: bool = field()
    description: AnyStr = field(default=None)
    parameters: dict = field(default={})
    descriptor: Descriptor = field(default={})

    def __init__(self, **kwargs):
        from ..base import Base
        from ..utils.exceptions import ModelError
        Base().scrub(kwargs)
        try:
            self.__attrs_init__(**kwargs)
        except TypeError as te:
            raise ModelError(err=te, name='Asset')
