from typing import ClassVar, Dict, Type

import attr

from elgas.parameters.analog_quantity import AnalogQuantity, AnalogQuantitySchema
from elgas.parameters.binary import Binary, BinarySchema
from elgas.parameters.compressibility import (
    Compressibility,
    CompressibilitySchema,
    CompressibilityZ,
    CompressibilityZBase,
    CompressibilityZBaseSchema,
    CompressibilityZSchema,
)
from elgas.parameters.conversion_coefficient import (
    ConversionCoefficient,
    ConversionCoefficientSchema,
)
from elgas.parameters.counter import (
    Counter,
    CounterSchema,
    DoubleCounter,
    DoubleCounterSchema,
)
from elgas.parameters.device_error import DeviceError, DeviceErrorSchema
from elgas.parameters.diagnostics import Diagnostics, DiagnosticsSchema
from elgas.parameters.difference_counter import (
    DifferenceBaseCounter,
    DifferenceBaseCounterSchema,
    DifferenceCounter,
    DifferenceCounterSchema,
)
from elgas.parameters.energy import Energy, EnergySchema, ErrorEnergy, ErrorEnergySchema
from elgas.parameters.enumerations import ParameterObjectType
from elgas.parameters.error_counter import (
    DoubleErrorCounter,
    DoubleErrorCounterSchema,
    ErrorCounter,
    ErrorCounterSchema,
)
from elgas.parameters.error_standard_counter import (
    ErrorStandardCounter,
    ErrorStandardCounterSchema,
)
from elgas.parameters.flow_rate import (
    FlowRate,
    FlowRateSchema,
    StandardFlowRate,
    StandardFlowRateSchema,
)
from elgas.parameters.modem import Modem, ModemSchema
from elgas.parameters.setpoint import SetPoint, SetPointSchema
from elgas.parameters.standard_counter import StandardCounter, StandardCounterSchema
from elgas.parameters.statistics import (
    AnalogStatistics,
    AnalogStatisticsSchema,
    AnalogTimeStatistics,
    AnalogTimeStatisticsSchema,
    CounterStatistics,
    CounterStatisticsSchema,
    StandardCounterStatistics,
    StandardCounterStatisticsSchema,
    Statistics,
    StatisticsSchema,
    TimeStatistics,
    TimeStatisticsSchema,
)
from elgas.parameters.sum_of_alarms import SumOfAlarms, SumOfAlarmsSchema
from elgas.parameters.system_parameters import SystemParameters, SystemParametersSchema
from elgas.parameters.tariff_counter import (
    BaseTariffCounter,
    BaseTariffCounterSchema,
    DoubleTariffCounter,
    DoubleTariffCounterSchema,
    TariffCounter,
    TariffCounterSchema,
)
from elgas.parameters.time_window import TimeWindow, TimeWindowSchema
from elgas.parameters.timer import Timer, TimerSchema


@attr.s(auto_attribs=True)
class ParameterFactory:

    object_map: ClassVar[Dict[ParameterObjectType, Type]] = {
        ParameterObjectType.SYSTEM_PARAMETER: SystemParameters,
        ParameterObjectType.ANALOG_MEASURAND: AnalogQuantity,
        ParameterObjectType.BINARY: Binary,
        ParameterObjectType.COUNTER: Counter,
        ParameterObjectType.STANDARD_COUNTER: StandardCounter,
        ParameterObjectType.FLOW_RATE: FlowRate,
        ParameterObjectType.STANDARD_FLOW_RATE: StandardFlowRate,
        ParameterObjectType.CONVERSION_COEFFICIENT: ConversionCoefficient,
        ParameterObjectType.ERROR_COUNTER: ErrorCounter,
        ParameterObjectType.ERROR_STANDARD_COUNTER: ErrorStandardCounter,
        ParameterObjectType.COMPRESSIBILITY: Compressibility,
        ParameterObjectType.TIME_WINDOW: TimeWindow,
        ParameterObjectType.DOUBLE_COUNTER: DoubleCounter,
        ParameterObjectType.DOUBLE_ERROR_COUNTER: DoubleErrorCounter,
        ParameterObjectType.DIAGNOSTICS: Diagnostics,
        ParameterObjectType.SET_POINT: SetPoint,
        ParameterObjectType.COMPRESSIBILITY_Z: CompressibilityZ,
        ParameterObjectType.COMPRESSIBILITY_Z_BASE: CompressibilityZBase,
        ParameterObjectType.ENERGY: Energy,
        ParameterObjectType.ERROR_ENERGY: ErrorEnergy,
        ParameterObjectType.TARIFF_COUNTER: TariffCounter,
        ParameterObjectType.DOUBLE_TARIFF_COUNTER: DoubleTariffCounter,
        ParameterObjectType.BASE_TARIFF_COUNTER: BaseTariffCounter,
        ParameterObjectType.DIFFERENCE_COUNTER: DifferenceCounter,
        ParameterObjectType.DIFFERENCE_BASE_COUNTER: DifferenceBaseCounter,
        ParameterObjectType.TIMER: Timer,
        ParameterObjectType.DEVICE_ERROR: DeviceError,
        ParameterObjectType.SUM_OF_ALARMS: SumOfAlarms,
        ParameterObjectType.ANALOG_STATISTICS: AnalogStatistics,
        ParameterObjectType.STATISTICS: Statistics,
        ParameterObjectType.ANALOG_TIME_STATISTICS: AnalogTimeStatistics,
        ParameterObjectType.TIME_STATISTICS: TimeStatistics,
        ParameterObjectType.COUNTER_STATISTICS: CounterStatistics,
        ParameterObjectType.STANDARD_COUNTER_STATISTICS: StandardCounterStatistics,
        ParameterObjectType.MODEM: Modem,
    }

    @staticmethod
    def from_bytes(object_type: ParameterObjectType, in_data: bytes):
        klass = ParameterFactory.object_map[object_type]
        return klass.from_bytes(in_data)


@attr.s(auto_attribs=True)
class ParameterSchemaFactory:

    object_map: ClassVar[Dict[ParameterObjectType, Type]] = {
        ParameterObjectType.SYSTEM_PARAMETER: SystemParametersSchema,
        ParameterObjectType.ANALOG_MEASURAND: AnalogQuantitySchema,
        ParameterObjectType.BINARY: BinarySchema,
        ParameterObjectType.COUNTER: CounterSchema,
        ParameterObjectType.STANDARD_COUNTER: StandardCounterSchema,
        ParameterObjectType.FLOW_RATE: FlowRateSchema,
        ParameterObjectType.STANDARD_FLOW_RATE: StandardFlowRateSchema,
        ParameterObjectType.CONVERSION_COEFFICIENT: ConversionCoefficientSchema,
        ParameterObjectType.ERROR_COUNTER: ErrorCounterSchema,
        ParameterObjectType.ERROR_STANDARD_COUNTER: ErrorStandardCounterSchema,
        ParameterObjectType.COMPRESSIBILITY: CompressibilitySchema,
        ParameterObjectType.TIME_WINDOW: TimeWindowSchema,
        ParameterObjectType.DOUBLE_COUNTER: DoubleCounterSchema,
        ParameterObjectType.DOUBLE_ERROR_COUNTER: DoubleErrorCounterSchema,
        ParameterObjectType.DIAGNOSTICS: DiagnosticsSchema,
        ParameterObjectType.SET_POINT: SetPointSchema,
        ParameterObjectType.COMPRESSIBILITY_Z: CompressibilityZSchema,
        ParameterObjectType.COMPRESSIBILITY_Z_BASE: CompressibilityZBaseSchema,
        ParameterObjectType.ENERGY: EnergySchema,
        ParameterObjectType.ERROR_ENERGY: ErrorEnergySchema,
        ParameterObjectType.TARIFF_COUNTER: TariffCounterSchema,
        ParameterObjectType.DOUBLE_TARIFF_COUNTER: DoubleTariffCounterSchema,
        ParameterObjectType.BASE_TARIFF_COUNTER: BaseTariffCounterSchema,
        ParameterObjectType.DIFFERENCE_COUNTER: DifferenceCounterSchema,
        ParameterObjectType.DIFFERENCE_BASE_COUNTER: DifferenceBaseCounterSchema,
        ParameterObjectType.TIMER: TimerSchema,
        ParameterObjectType.DEVICE_ERROR: DeviceErrorSchema,
        ParameterObjectType.SUM_OF_ALARMS: SumOfAlarmsSchema,
        ParameterObjectType.ANALOG_STATISTICS: AnalogStatisticsSchema,
        ParameterObjectType.STATISTICS: StatisticsSchema,
        ParameterObjectType.ANALOG_TIME_STATISTICS: AnalogTimeStatisticsSchema,
        ParameterObjectType.TIME_STATISTICS: TimeStatisticsSchema,
        ParameterObjectType.COUNTER_STATISTICS: CounterStatisticsSchema,
        ParameterObjectType.STANDARD_COUNTER_STATISTICS: StandardCounterStatisticsSchema,
        ParameterObjectType.MODEM: ModemSchema,
    }

    @staticmethod
    def by_parameter_id(parameter_id: ParameterObjectType):
        return ParameterSchemaFactory.object_map[parameter_id]
