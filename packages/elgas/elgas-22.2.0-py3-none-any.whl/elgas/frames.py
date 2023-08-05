from __future__ import annotations

from typing import *

import attr

from elgas import constants, utils


@attr.s(auto_attribs=True)
class Request:
    TYPE: ClassVar[int] = 0x84
    service: constants.ServiceNumber
    destination_address_1: int
    destination_address_2: int
    source_address_1: int
    source_address_2: int
    data: bytes

    ...

    @property
    def length(self) -> int:
        """
        All bytes are counted except STX, before replacing reserved characters
        """
        return len(self.data) + 15

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.append(0x02)
        out.append(0xFE)
        out.append(self.TYPE)
        out.append(self.service)
        out.extend(self.length.to_bytes(2, "little"))
        out.extend(self.destination_address_1.to_bytes(2, "big"))
        out.append(self.destination_address_2)
        out.extend(self.source_address_1.to_bytes(2, "big"))
        out.append(self.source_address_2)
        out.extend(self.data)
        redundancy_source = out[1:]
        out.append(utils.calculate_lrc(redundancy_source))
        out.append(utils.calculate_checksum(redundancy_source))
        out.append(utils.calculate_drc(redundancy_source))
        out.append(0x0D)

        return bytes(out)


@attr.s(auto_attribs=True)
class Response:
    TYPE: ClassVar[int] = 0x86
    service: constants.ServiceNumber
    destination_address_1: int
    destination_address_2: int
    source_address_1: int
    source_address_2: int
    data: bytes

    @property
    def length(self) -> int:
        """
        All bytes are counted except STX, before replacing reserved characters
        """
        return len(self.data) + 15

    def to_bytes(self) -> bytes:
        out = bytearray()
        out.append(0x02)
        out.append(0xFE)
        out.append(self.TYPE)
        out.append(self.service)
        out.extend(self.length.to_bytes(2, "little"))
        out.extend(self.destination_address_1.to_bytes(2, "little"))
        out.append(self.destination_address_2)
        out.extend(self.source_address_1.to_bytes(2, "little"))
        out.append(self.source_address_2)
        out.extend(self.data)
        redundancy_source = out[1:]
        out.append(utils.calculate_lrc(redundancy_source))
        out.append(utils.calculate_checksum(redundancy_source))
        out.append(utils.calculate_drc(redundancy_source))
        out.append(0x0D)

        return bytes(out)

    @classmethod
    def from_bytes(cls, in_bytes: bytes):
        if not in_bytes.startswith(b"\x02\xfe" + cls.TYPE.to_bytes(1, "little")):
            raise ValueError("Not a Response frame")
        if not in_bytes.endswith(b"\x0d"):
            raise ValueError("Data does not end with end char")
        service = constants.ServiceNumber(int.from_bytes(in_bytes[3:4], "little"))
        length = int.from_bytes(in_bytes[4:6], "little")
        if length != len(in_bytes) - 1:  # STX is not counted
            raise ValueError(
                f"Length field does not correspond to length of data. Got {len(in_bytes)-1}, should be {length} "
            )
        destination_address_1 = int.from_bytes(in_bytes[6:8], "little")
        destination_address_2 = int.from_bytes(in_bytes[8:9], "little")
        source_address_1 = int.from_bytes(in_bytes[9:11], "little")
        source_address_2 = int.from_bytes(in_bytes[11:12], "little")
        data = in_bytes[12:-4]
        redundancy_source = bytearray(in_bytes[1:-4])
        lrc = in_bytes[-4]
        calculated_lrc = utils.calculate_lrc(redundancy_source)
        if lrc != calculated_lrc:
            raise ValueError(
                f"Incorrect LRC. Got {lrc!r}, should be {calculated_lrc!r}"
            )
        checksum = in_bytes[-3]
        calculated_checksum = utils.calculate_checksum(redundancy_source)
        if checksum != calculated_checksum:
            raise ValueError(
                f"Incorrect CHECKSUM. Got {checksum!r}, should be {calculated_checksum!r}"
            )
        drc = in_bytes[-2]
        calculated_drc = utils.calculate_drc(redundancy_source)
        if drc != calculated_drc:
            raise ValueError(f"Incorrect DRC. Got {drc!r}, should be {drc!r}")

        return cls(
            service=service,
            destination_address_1=destination_address_1,
            destination_address_2=destination_address_2,
            source_address_1=source_address_1,
            source_address_2=source_address_2,
            data=data,
        )


@attr.s(auto_attribs=True)
class EncryptedRequest(Request):
    TYPE: ClassVar[int] = 0x85


@attr.s(auto_attribs=True)
class EncryptedResponse(Response):
    TYPE: ClassVar[int] = 0x87


@attr.s(auto_attribs=True)
class ResponseFactory:
    @staticmethod
    def from_bytes(in_data: bytes):
        if in_data.startswith(b"\x02\xfe\x86"):
            return Response.from_bytes(in_data)
        elif in_data.startswith(b"\x02\xfe\x87"):
            return EncryptedResponse.from_bytes(in_data)
        else:
            raise ValueError("Data is not a response frame")
