import struct
from typing import ClassVar, Optional

import attr
import marshmallow
from marshmallow import post_load

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import pop_many, pretty_text


@attr.s(auto_attribs=True)
class AnalogQuantity:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.ANALOG_MEASURAND
    value_length: ClassVar[int] = 2

    number: int
    id: int
    address_in_actual_values: int
    address_in_data_archive_record: int
    bit_control: int  # seems to be which archives the values is in?
    in_data_archive: bool
    in_daily_archive: bool
    in_monthly_archive: bool
    is_metrological_quantity: bool
    in_fast_archive_1: bool
    in_fast_archvie_2: bool
    name: str
    unit: str
    digit: float
    offset: float
    lower_limit_measuring_range: float
    upper_limit_measuring_range: float
    serial_number_transducer: int
    error_bit_order_in_actual_values: int
    error_bit_order_in_binary_archive: int
    error_bit_order_in_data_archive: int
    address_in_daily_archive_record: int
    address_in_monthly_archive_record: int
    samples_in_fast_archive: int
    decimals: Optional[int]

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
        in_fast_archive_1 = bool(bit_control & 0b00100000)
        in_fast_archvie_2 = bool(bit_control & 0b01000000)
        name = pretty_text(pop_many(data, 23))
        unit = pretty_text(pop_many(data, 8))
        digit = round(struct.unpack("<f", pop_many(data, 4))[0], 7)
        offset = struct.unpack("<f", pop_many(data, 4))[0]
        lower_limit_measuring_range = round(
            struct.unpack("<f", pop_many(data, 4))[0], 7
        )
        upper_limit_measuring_range = struct.unpack("<f", pop_many(data, 4))[0]
        serial_number_transducer = int.from_bytes(pop_many(data, 4), "little")
        error_bit_order_in_actual_values = int.from_bytes(pop_many(data, 2), "little")
        error_bit_order_in_binary_archive = int.from_bytes(pop_many(data, 2), "little")
        error_bit_order_in_data_archive = int.from_bytes(pop_many(data, 2), "little")
        address_in_daily_archive_record = int.from_bytes(pop_many(data, 2), "little")
        address_in_monthly_archive_record = int.from_bytes(pop_many(data, 2), "little")
        samples_in_fast_archive = data.pop(0)

        if data:
            decimals = data.pop(0)
        else:
            decimals = None

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
            in_fast_archive_1=in_fast_archive_1,
            in_fast_archvie_2=in_fast_archvie_2,
            name=name,
            unit=unit,
            digit=digit,
            offset=offset,
            lower_limit_measuring_range=lower_limit_measuring_range,
            upper_limit_measuring_range=upper_limit_measuring_range,
            serial_number_transducer=serial_number_transducer,
            error_bit_order_in_actual_values=error_bit_order_in_actual_values,
            error_bit_order_in_binary_archive=error_bit_order_in_binary_archive,
            error_bit_order_in_data_archive=error_bit_order_in_data_archive,
            address_in_daily_archive_record=address_in_daily_archive_record,
            address_in_monthly_archive_record=address_in_monthly_archive_record,
            samples_in_fast_archive=samples_in_fast_archive,
            decimals=decimals,
        )


class AnalogQuantitySchema(marshmallow.Schema):
    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    address_in_actual_values = marshmallow.fields.Integer(required=True)
    address_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_control = marshmallow.fields.Integer(required=True)
    in_data_archive = marshmallow.fields.Boolean(required=True)
    in_daily_archive = marshmallow.fields.Boolean(required=True)
    in_monthly_archive = marshmallow.fields.Boolean(required=True)
    is_metrological_quantity = marshmallow.fields.Boolean(required=True)
    in_fast_archive_1 = marshmallow.fields.Boolean(required=True)
    in_fast_archvie_2 = marshmallow.fields.Boolean(required=True)
    name = marshmallow.fields.String(required=True)
    unit = marshmallow.fields.String(required=True)
    digit = marshmallow.fields.Number(required=True)
    offset = marshmallow.fields.Number(required=True)
    lower_limit_measuring_range = marshmallow.fields.Number(required=True)
    upper_limit_measuring_range = marshmallow.fields.Number(required=True)
    serial_number_transducer = marshmallow.fields.Integer(required=True)
    error_bit_order_in_actual_values = marshmallow.fields.Integer(required=True)
    error_bit_order_in_binary_archive = marshmallow.fields.Integer(required=True)
    error_bit_order_in_data_archive = marshmallow.fields.Integer(required=True)
    address_in_daily_archive_record = marshmallow.fields.Integer(required=True)
    address_in_monthly_archive_record = marshmallow.fields.Integer(required=True)
    samples_in_fast_archive = marshmallow.fields.Integer(required=True)
    decimals = marshmallow.fields.Integer(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return AnalogQuantity(**data)
