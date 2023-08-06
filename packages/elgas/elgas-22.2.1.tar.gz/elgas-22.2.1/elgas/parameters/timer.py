from typing import ClassVar

import attr
import marshmallow
from marshmallow import post_load

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import pop_many, pretty_text


@attr.s(auto_attribs=True)
class Timer:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.TIMER
    value_length: ClassVar[int] = 4

    number: int
    id: int
    address_in_actual_values: int
    address_in_data_archive_record: int
    bit_control: int
    in_data_archive: int
    in_daily_archive: int
    in_monthly_archive: int
    is_metrological_quantity: int
    name: str

    address_in_daily_archive_record: int
    address_in_monthly_archive_record: int

    @classmethod
    def from_bytes(cls, in_data: bytes):
        data = bytearray(in_data)
        number = int.from_bytes(pop_many(data, 2), "little")
        id = int.from_bytes(pop_many(data, 2), "little")
        address_in_actual_values = int.from_bytes(pop_many(data, 2), "little")
        address_in_data_archive_record = int.from_bytes(pop_many(data, 2), "little")
        bit_control = data.pop(0)
        in_data_archive = bool(bit_control & 0b00000001)
        in_daily_archive = bool(bit_control & 0b00000010)
        in_monthly_archive = bool(bit_control & 0b00000100)
        is_metrological_quantity = bool(bit_control & 0b00010000)
        name = pretty_text(pop_many(data, 23))

        address_in_daily_archive_record = int.from_bytes(pop_many(data, 2), "little")
        address_in_monthly_archive_record = int.from_bytes(pop_many(data, 2), "little")

        assert not data

        return cls(
            number=number,
            id=id,
            address_in_actual_values=address_in_actual_values,
            address_in_data_archive_record=address_in_data_archive_record,
            bit_control=bit_control,
            in_data_archive=in_data_archive,
            in_daily_archive=in_daily_archive,
            in_monthly_archive=in_monthly_archive,
            is_metrological_quantity=is_metrological_quantity,
            name=name,
            address_in_daily_archive_record=address_in_daily_archive_record,
            address_in_monthly_archive_record=address_in_monthly_archive_record,
        )


class TimerSchema(marshmallow.Schema):
    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    address_in_actual_values = marshmallow.fields.Integer(required=True)
    address_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_control = marshmallow.fields.Integer(required=True)
    in_data_archive = marshmallow.fields.Integer(required=True)
    in_daily_archive = marshmallow.fields.Integer(required=True)
    in_monthly_archive = marshmallow.fields.Integer(required=True)
    is_metrological_quantity = marshmallow.fields.Integer(required=True)
    name = marshmallow.fields.String(required=True)

    address_in_daily_archive_record = marshmallow.fields.Integer(required=True)
    address_in_monthly_archive_record = marshmallow.fields.Integer(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Timer(**data)
