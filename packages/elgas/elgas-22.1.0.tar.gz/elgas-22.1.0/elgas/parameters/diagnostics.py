from typing import ClassVar

import attr
import marshmallow
from marshmallow import post_load

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import pop_many, pretty_text


@attr.s(auto_attribs=True)
class Diagnostics:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.DIAGNOSTICS

    number: int
    id: int
    address_in_actual_values: int
    address_in_data_archive_record: int
    bit_control: int
    in_data_archive: bool
    in_daily_archive: bool
    in_monthly_archive: bool
    in_factory_archive: bool
    name: str

    address_in_daily_archive_record: int
    address_in_monthly_archive_record: int
    mask_1_of_status_archive: int
    mask_2_of_status_archive: int
    mask_1_of_alarm: int
    mask_2_of_alarm: int
    mask_1_of_calling_to_dispatching: int
    mask_2_of_calling_to_dispatching: int
    action_during_change: int

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
        in_factory_archive = bool(bit_control & 0b00001000)
        name = pretty_text(pop_many(data, 23))

        address_in_daily_archive_record = int.from_bytes(pop_many(data, 2), "little")
        address_in_monthly_archive_record = int.from_bytes(pop_many(data, 2), "little")
        mask_1_of_status_archive = int.from_bytes(pop_many(data, 4), "little")
        mask_2_of_status_archive = int.from_bytes(pop_many(data, 4), "little")
        mask_1_of_alarm = int.from_bytes(pop_many(data, 4), "little")
        mask_2_of_alarm = int.from_bytes(pop_many(data, 4), "little")
        mask_1_of_calling_to_dispatching = int.from_bytes(pop_many(data, 4), "little")
        mask_2_of_calling_to_dispatching = int.from_bytes(pop_many(data, 4), "little")
        action_during_change = data.pop(0)

        return cls(
            number=number,
            id=id,
            address_in_actual_values=address_in_actual_values,
            address_in_data_archive_record=address_in_data_archive_record,
            bit_control=bit_control,
            in_data_archive=in_data_archive,
            in_daily_archive=in_daily_archive,
            in_monthly_archive=in_monthly_archive,
            in_factory_archive=in_factory_archive,
            name=name,
            address_in_daily_archive_record=address_in_daily_archive_record,
            address_in_monthly_archive_record=address_in_monthly_archive_record,
            mask_1_of_status_archive=mask_1_of_status_archive,
            mask_2_of_status_archive=mask_2_of_status_archive,
            mask_1_of_alarm=mask_1_of_alarm,
            mask_2_of_alarm=mask_2_of_alarm,
            mask_1_of_calling_to_dispatching=mask_1_of_calling_to_dispatching,
            mask_2_of_calling_to_dispatching=mask_2_of_calling_to_dispatching,
            action_during_change=action_during_change,
        )


class DiagnosticsSchema(marshmallow.Schema):

    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    address_in_actual_values = marshmallow.fields.Integer(required=True)
    address_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_control = marshmallow.fields.Integer(required=True)
    in_data_archive = marshmallow.fields.Boolean(required=True)
    in_daily_archive = marshmallow.fields.Boolean(required=True)
    in_monthly_archive = marshmallow.fields.Boolean(required=True)
    in_factory_archive = marshmallow.fields.Boolean(required=True)
    name = marshmallow.fields.String(required=True)

    address_in_daily_archive_record = marshmallow.fields.Integer(required=True)
    address_in_monthly_archive_record = marshmallow.fields.Integer(required=True)
    mask_1_of_status_archive = marshmallow.fields.Integer(required=True)
    mask_2_of_status_archive = marshmallow.fields.Integer(required=True)
    mask_1_of_alarm = marshmallow.fields.Integer(required=True)
    mask_2_of_alarm = marshmallow.fields.Integer(required=True)
    mask_1_of_calling_to_dispatching = marshmallow.fields.Integer(required=True)
    mask_2_of_calling_to_dispatching = marshmallow.fields.Integer(required=True)
    action_during_change = marshmallow.fields.Integer(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Diagnostics(**data)
