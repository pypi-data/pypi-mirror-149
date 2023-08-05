# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import (
    AnyStr
)
from attr import (
    define,
    field
)


@define
class SharedBase:
    id: AnyStr = field()
    name: AnyStr = field()

@define
class CreatedByUser(SharedBase):
    pass
