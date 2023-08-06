import struct
from typing import ClassVar, Optional

import attr
import marshmallow
from marshmallow import post_load

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import pop_many, pretty_text


@attr.s(auto_attribs=True)
class AnalogStatistics:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.ANALOG_STATISTICS

    number: int
    id: int
    address_in_actual_values: int  # Always 0
    address_in_data_archive_record: int
    bit_control: int
    in_data_archive: bool
    in_daily_archive: bool
    in_monthly_archive: bool
    is_metrological_quantity: bool
    name: str
    unit: str
    digit: float
    offset: float
    number_of_primary_quantity: int
    statistics_type: int  # 0 = min, 1 = max.
    address_in_daily_archive_record: int
    address_in_monthly_archive_record: int
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
        name = pretty_text(pop_many(data, 23))
        unit = pretty_text(pop_many(data, 8))
        digit = round(struct.unpack("<f", pop_many(data, 4))[0], 7)
        offset = struct.unpack("<f", pop_many(data, 4))[0]
        number_of_primary_quantity = data.pop(0)
        statistics_type = data.pop(0)
        address_in_daily_archive_record = int.from_bytes(pop_many(data, 2), "little")
        address_in_monthly_archive_record = int.from_bytes(pop_many(data, 2), "little")

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
            name=name,
            unit=unit,
            digit=digit,
            offset=offset,
            number_of_primary_quantity=number_of_primary_quantity,
            statistics_type=statistics_type,
            address_in_daily_archive_record=address_in_daily_archive_record,
            address_in_monthly_archive_record=address_in_monthly_archive_record,
            decimals=decimals,
        )


class AnalogStatisticsSchema(marshmallow.Schema):

    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    address_in_actual_values = marshmallow.fields.Integer(required=True)
    address_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_control = marshmallow.fields.Integer(required=True)
    in_data_archive = marshmallow.fields.Boolean(required=True)
    in_daily_archive = marshmallow.fields.Boolean(required=True)
    in_monthly_archive = marshmallow.fields.Boolean(required=True)
    is_metrological_quantity = marshmallow.fields.Boolean(required=True)
    name = marshmallow.fields.String(required=True)
    unit = marshmallow.fields.String(required=True)
    digit = marshmallow.fields.Float(required=True, as_string=True)
    offset = marshmallow.fields.Float(required=True, as_string=True)
    number_of_primary_quantity = marshmallow.fields.Integer(required=True)
    statistics_type = marshmallow.fields.Integer(required=True)
    address_in_daily_archive_record = marshmallow.fields.Integer(required=True)
    address_in_monthly_archive_record = marshmallow.fields.Integer(required=True)
    decimals = marshmallow.fields.Integer(required=True, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return AnalogStatistics(**data)


class Statistics(AnalogStatistics):
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.STATISTICS


class StatisticsSchema(AnalogStatisticsSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return Statistics(**data)


class AnalogTimeStatistics(AnalogStatistics):
    object_type: ClassVar[
        ParameterObjectType
    ] = ParameterObjectType.ANALOG_TIME_STATISTICS


class AnalogTimeStatisticsSchema(AnalogStatisticsSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return AnalogTimeStatistics(**data)


class TimeStatistics(AnalogStatistics):
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.TIME_STATISTICS


class TimeStatisticsSchema(AnalogStatisticsSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return TimeStatistics(**data)


@attr.s(auto_attribs=True)
class CounterStatistics:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.COUNTER_STATISTICS

    number: int
    id: int
    address_in_actual_values: int  # Always 0
    address_in_data_archive_record: int  # Always 0
    bit_control: int
    in_data_archive: bool
    in_daily_archive: bool
    in_monthly_archive: bool
    is_metrological_quantity: bool
    name: str
    unit: str
    digit: float
    type_of_primary_quantity: int
    number_of_primary_quantity: int
    statistics_type: int  # 0 = min, 1 = max.
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
        unit = pretty_text(pop_many(data, 8))
        digit = struct.unpack("<d", pop_many(data, 8))[0]
        type_of_primary_quantity = data.pop(0)
        number_of_primary_quantity = data.pop(0)
        statistics_type = data.pop(0)
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
            unit=unit,
            digit=digit,
            type_of_primary_quantity=type_of_primary_quantity,
            number_of_primary_quantity=number_of_primary_quantity,
            statistics_type=statistics_type,
            address_in_daily_archive_record=address_in_daily_archive_record,
            address_in_monthly_archive_record=address_in_monthly_archive_record,
        )


class StandardCounterStatistics(CounterStatistics):
    object_type: ClassVar[
        ParameterObjectType
    ] = ParameterObjectType.STANDARD_COUNTER_STATISTICS


class CounterStatisticsSchema(marshmallow.Schema):

    number = marshmallow.fields.Integer(required=True)
    id = marshmallow.fields.Integer(required=True)
    address_in_actual_values = marshmallow.fields.Integer(required=True)
    address_in_data_archive_record = marshmallow.fields.Integer(required=True)
    bit_control = marshmallow.fields.Integer(required=True)
    in_data_archive = marshmallow.fields.Boolean(required=True)
    in_daily_archive = marshmallow.fields.Boolean(required=True)
    in_monthly_archive = marshmallow.fields.Boolean(required=True)
    is_metrological_quantity = marshmallow.fields.Boolean(required=True)
    name = marshmallow.fields.String(required=True)
    unit = marshmallow.fields.String(required=True)
    digit = marshmallow.fields.Float(required=True, as_string=True)
    type_of_primary_quantity = marshmallow.fields.Integer(required=True)
    number_of_primary_quantity = marshmallow.fields.Integer(required=True)
    statistics_type = marshmallow.fields.Integer(required=True)
    address_in_daily_archive_record = marshmallow.fields.Integer(required=True)
    address_in_monthly_archive_record = marshmallow.fields.Integer(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return CounterStatistics(**data)


class StandardCounterStatisticsSchema(CounterStatisticsSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return StandardCounterStatistics(**data)
