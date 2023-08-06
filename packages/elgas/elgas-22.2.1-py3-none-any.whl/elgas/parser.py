from typing import *

import attr

import elgas.parameters
import elgas.parameters.enumerations
import elgas.parameters.factory
from elgas.utils import pop_many


@attr.s(auto_attribs=True)
class SimpleObjectHolder:
    """Just a class to hold data to verify in development."""

    length: int
    object_type: int
    data: bytes


@attr.s(auto_attribs=True)
class ScadaParameterParser:
    data: Optional[bytes] = attr.ib(default=None)

    def parse(self, data: Optional[bytes] = None):
        working_data = bytearray(self.data or data)

        if not working_data:
            raise ValueError("No data to parse")

        object_list = list()

        while working_data:
            length = int.from_bytes(pop_many(working_data, 2), "little")
            object_type = elgas.parameters.enumerations.ParameterObjectType(
                working_data.pop(0)
            )
            data = working_data[: length - 3]
            object_list.append(
                elgas.parameters.factory.ParameterFactory.from_bytes(object_type, data)
            )

            working_data = working_data[length - 3 :]

        return object_list
