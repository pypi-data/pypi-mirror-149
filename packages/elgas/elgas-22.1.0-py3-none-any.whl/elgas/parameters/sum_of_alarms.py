from typing import ClassVar, Optional

import attr
import marshmallow
from marshmallow import post_load

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import pop_many, pretty_text


@attr.s(auto_attribs=True)
class SumOfAlarms:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.SUM_OF_ALARMS

    number: int
    id: int
    bit_order_in_actual_values: int
    bit_order_in_data_archive_record: int
    bit_order_in_binary_archive_record: int

    bit_control: int
    in_binary_archive: bool
    in_data_archive: bool
    name: str
    error_bit_order_in_actual_values: int
    error_bit_order_in_binary_archive_record: int  # TODO: Are these switch . Seems weird to have them in reverse order further down in the structure.
    error_bit_order_in_data_archive_record: int
    action_during_change: Optional[int]
    text_log_0: Optional[str]
    text_log_1: Optional[str]

    @classmethod
    def from_bytes(cls, in_data: bytes):
        data = bytearray(in_data)
        number = int.from_bytes(pop_many(data, 2), "little")
        id = int.from_bytes(pop_many(data, 2), "little")
        bit_order_in_actual_values = int.from_bytes(pop_many(data, 2), "little")
        bit_order_in_data_archive_record = int.from_bytes(pop_many(data, 2), "little")
        bit_order_in_binary_archive_record = int.from_bytes(pop_many(data, 2), "little")

        bit_control = data.pop(0)
        in_binary_archive = bool(bit_control & 0b00000001)
        in_data_archive = bool(bit_control & 0b00000010)
        name = pretty_text(pop_many(data, 23))
        if data:
            action_during_change = data.pop(0)
            text_log_0 = pretty_text(pop_many(data, 13))
            text_log_1 = pretty_text(pop_many(data, 13))
        else:
            action_during_change = None
            text_log_0 = None
            text_log_1 = None

        assert not data

        return cls(
            number=number,
            id=id,
            bit_order_in_actual_values=bit_order_in_actual_values,
            bit_order_in_data_archive_record=bit_order_in_data_archive_record,
            bit_order_in_binary_archive_record=bit_order_in_binary_archive_record,
            bit_control=bit_control,
            in_binary_archive=in_binary_archive,
            in_data_archive=in_data_archive,
            name=name,
            action_during_change=action_during_change,
            text_log_0=text_log_0,
            text_log_1=text_log_1,
        )


class SumOfAlarmsSchema(marshmallow.Schema):
    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    bit_order_in_actual_values = marshmallow.fields.Integer(required=True)
    bit_order_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_order_in_binary_archive_record = marshmallow.fields.Integer(required=True)

    bit_control = marshmallow.fields.Integer(required=True)
    in_binary_archive = marshmallow.fields.Boolean(required=True)
    in_data_archive = marshmallow.fields.Boolean(required=True)
    name = marshmallow.fields.String(required=True)
    error_bit_order_in_actual_values = marshmallow.fields.Integer(required=True)
    error_bit_order_in_binary_archive_record = marshmallow.fields.Integer(required=True)
    error_bit_order_in_data_archive_record = marshmallow.fields.Integer(required=True)
    action_during_change = marshmallow.fields.Integer(required=True, allow_none=True)
    text_log_0 = marshmallow.fields.String(required=True, allow_none=True)
    text_log_1 = marshmallow.fields.String(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return SumOfAlarms(**data)
