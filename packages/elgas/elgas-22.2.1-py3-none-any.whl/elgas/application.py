import datetime
from enum import IntEnum
from typing import *

import attr

from elgas import constants, utils


class Archive(IntEnum):
    EXTREME = 0
    DATA = 1
    BINARY = 2
    DAILY = 3
    MONTHLY = 4
    SETTING = 5
    FAST_1 = 6
    FAST_2 = 7
    STATUS = 8
    BILLING = 9
    GAS_COMPOSITION = 10


@attr.s(auto_attribs=True)
class ReadInstantaneousValuesRequest:
    """
    Will request a readout of all current parameters in the device
    """

    service: ClassVar[constants.ServiceNumber] = constants.ServiceNumber.READ_VALUES
    password: str

    def to_bytes(self) -> bytes:
        return utils.pad_password(self.password).encode("latin-1")


@attr.s(auto_attribs=True)
class ReadInstantaneousValuesResponse:
    """
    A long datastructure of parameters that depends on the firmware of the device.
    The parsing is set to ELCORplus Gen 4.
    Instantaneous values are called Actual Values in documentation.
    """

    service: ClassVar[constants.ServiceNumber] = constants.ServiceNumber.READ_VALUES
    current_time: datetime
    is_dst: bool
    supports_dst: bool
    data: bytes
    data_access: int
    status: int
    summary_status: int
    parameter_crc: bytes

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        data = in_bytes
        current_time, is_dst, supports_dst = utils.bytes_to_datetime(data[:6])
        data = data[6:]
        parameter_crc = data[-2:]
        data = data[:-2]
        summary_status = data[-8:]
        data = data[:-8]
        status = data[-8:]
        data = data[:-8]
        data_access = data[-1]
        data = data[:-1]
        return cls(
            data=data,
            current_time=current_time,
            is_dst=is_dst,
            supports_dst=supports_dst,
            parameter_crc=parameter_crc,
            summary_status=summary_status,
            status=status,
            data_access=data_access,
        )


@attr.s(auto_attribs=True)
class ReadTimeRequest:
    """
    Request for the device's time. It contains no data.
    """

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_DEVICE_TIME

    def to_bytes(self) -> bytes:
        return b""


@attr.s(auto_attribs=True)
class ReadTimeResponse:
    """
    Contains the device time. Some firmware adds internal data at the end of the
    message.
    """

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_DEVICE_TIME

    time: datetime
    data_access_result: bytes
    is_dst: bool
    device_supports_dst: bool
    extra_data: bytes

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        time_data = in_bytes[:6]
        data_access_result = in_bytes[6:7]
        extra_data = in_bytes[7:-2]
        # crc = in_bytes[-2:]
        # TODO: Check CRC
        device_time, is_dst, supports_dst = utils.bytes_to_datetime(time_data)
        return cls(
            time=device_time,
            data_access_result=data_access_result,
            is_dst=is_dst,
            device_supports_dst=supports_dst,
            extra_data=extra_data,
        )


@attr.s(auto_attribs=True)
class WriteTimeRequest:
    """
    Request for the device's time. It contains no data.
    """

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.WRITE_DEVICE_TIME

    password: str
    device_time: datetime

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.extend(utils.pad_password(self.password).encode("latin-1"))
        out.extend(utils.datetime_to_bytes(self.device_time))
        out.append(0b00000100)  # Flag to only sync time.

        return bytes(out)


@attr.s(auto_attribs=True)
class WriteTimeResponse:
    """
    Contains the device time. Some firmware adds internal data at the end of the
    message.
    """

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_DEVICE_TIME

    @classmethod
    def from_bytes(cls, in_bytes: bytes):

        return cls()


@attr.s(auto_attribs=True)
class ReadDeviceParametersRequest:
    """"""

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_SCADA_PARAMETERS

    password: str  # todo: set max lenght
    object_count: int  # todo: set max and min
    buffer_length: int  # todo: set max and min

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.extend(utils.pad_password(self.password).encode("latin-1"))
        out.extend(self.object_count.to_bytes(2, "little"))
        out.extend(self.buffer_length.to_bytes(2, "little"))

        return bytes(out)


@attr.s(auto_attribs=True)
class ReadDeviceParametersResponse:
    """"""

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_SCADA_PARAMETERS

    data: bytes
    object_number: int
    object_amount: int
    is_end: int  # TODO: Should this be a separate class to use in state handling?

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        object_number = int.from_bytes(in_bytes[:2], "little")
        object_amount = int.from_bytes(in_bytes[2:4], "little")
        is_end = bool(in_bytes[4])
        data = in_bytes[5:]
        return cls(
            object_number=object_number,
            object_amount=object_amount,
            is_end=is_end,
            data=data,
        )


@attr.s(auto_attribs=True)
class ReadArchiveByTimeRequest:
    """"""

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_ARCHIVES_BY_DATE

    password: str  # todo: set max lenght
    archive: constants.Archive
    amount: int
    oldest_timestamp: datetime

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.extend(utils.pad_password(self.password).encode("latin-1"))
        out.append(self.archive)
        out.extend(self.amount.to_bytes(2, "little"))
        out.extend(utils.datetime_to_bytes(self.oldest_timestamp))

        return bytes(out)


@attr.s(auto_attribs=True)
class ReadArchiveByTimeResponse:
    """"""

    service: ClassVar[
        constants.ServiceNumber
    ] = constants.ServiceNumber.READ_ARCHIVES_BY_DATE

    archive: constants.Archive
    oldest_record_id: int
    data: bytes

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        archive = constants.Archive(in_bytes[0])
        oldest_record_id = int.from_bytes(in_bytes[1:4], "little")
        data = in_bytes[5:]
        return cls(
            archive=archive,
            oldest_record_id=oldest_record_id,
            data=data,
        )


@attr.s(auto_attribs=True)
class ReadArchiveRequest:
    """"""

    service: ClassVar[constants.ServiceNumber] = constants.ServiceNumber.READ_ARCHIVES

    password: str  # todo: set max lenght
    archive: constants.Archive
    amount: int
    oldest_record_id: int

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.extend(utils.pad_password(self.password).encode("latin-1"))
        out.append(self.archive)
        out.extend(self.oldest_record_id.to_bytes(4, "little"))
        out.extend(self.amount.to_bytes(2, "little"))

        return bytes(out)


@attr.s(auto_attribs=True)
class ReadArchiveResponse:
    """"""

    service: ClassVar[constants.ServiceNumber] = constants.ServiceNumber.READ_ARCHIVES

    archive: constants.Archive
    oldest_record_id: int
    data: bytes

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        archive = constants.Archive(in_bytes[0])
        oldest_record_id = int.from_bytes(in_bytes[1:4], "little")
        data = in_bytes[5:]
        return cls(
            archive=archive,
            oldest_record_id=oldest_record_id,
            data=data,
        )
