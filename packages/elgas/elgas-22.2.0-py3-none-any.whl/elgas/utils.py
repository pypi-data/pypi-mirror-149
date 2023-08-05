import random
import sys
from datetime import datetime
from typing import *


class SecretStr(str):
    """
    String that censors its __repr__ if called from another repr.
    """

    def __repr__(self):
        """Produce a string representation."""
        frame_depth = 1

        try:
            while True:
                f = sys._getframe(frame_depth)
                frame_depth += 1

                if f.f_code.co_name == "__repr__":
                    return "<SECRET>"
        except ValueError:
            pass

        return super().__repr__()


class SecretByte(bytes):
    """
    Bytes that censors its __repr__ if called from another repr.
    """

    def __repr__(self):
        """Produce a string representation."""
        frame_depth = 1

        try:
            while True:
                f = sys._getframe(frame_depth)
                frame_depth += 1

                if f.f_code.co_name == "__repr__":
                    return "<SECRET>"
        except ValueError:
            pass

        return super().__repr__()


def to_secret_byte(data: bytes) -> SecretByte:
    if data:
        return SecretByte(data)


def to_secret_str(data: str) -> SecretStr:
    return SecretStr(data)


def calculate_lrc(data: bytearray) -> int:
    lrc = 0
    for _byte in data:
        temp = lrc ^ _byte
        lrc = temp & 0xFF
    return lrc & 0xFF


def calculate_checksum(data: bytearray) -> int:
    checksum = 0
    for _byte in data:
        temp = checksum + _byte
        checksum = temp & 0xFF
    return checksum & 0xFF


def calculate_drc(data: bytearray) -> int:
    drc = 0
    for _byte in data:
        temp = drc << 1
        if temp & 0x100:
            temp = temp + 1
        temp = temp & 0xFF
        temp = temp ^ _byte
        drc = temp & 0xFF
    return drc & 0xFF


def generate_crc16_table():
    result = []
    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
            byte >>= 1
        result.append(crc)
    return result


crc16_table = generate_crc16_table()


def calculate_crc(data: bytearray):
    crc = 0xFFFF
    for a in data:
        idx = crc16_table[(crc ^ a) & 0xFF]
        crc = ((crc >> 8) & 0xFF) ^ idx
    result = ((crc << 8) & 0xFF00) | ((crc >> 8) & 0x00FF)
    return result


def escape_characters(data: bytes) -> bytes:
    """
    Characters that are used for telegram control are replaced with others
    so that it easier to parse the message over the wire.
    Final character is never replaced.

    '\x0d' -> '\x1b\x0e'
    '\x1b' -> '\x1b\x1b'
    '\x8d' -> '\x1b\x0f'
    """
    if not data.endswith(b"\x0d"):
        raise ValueError("Data does not end with end-char 0x0D")
    workable_data = data[:-1]
    escaped_data = (
        workable_data.replace(b"\x1b", b"\x1b\x1b")
        .replace(b"\x0d", b"\x1b\x0e")
        .replace(b"\x8d", b"\x1b\x0f")
    )
    return escaped_data + b"\x0d"


def return_characters(data: bytes) -> bytes:
    """
    Characters that are used for telegram control are replaced with others
    so that it is easier to parse the message over the wire.
    Final character is never replaced.
    This function returns them to their original form.

    '\x1b\x0e' -> '\x0d'
    '\x1b\x1b' -> '\x1b'
    '\x1b\x0f' -'\x8d'

    It is important to only do one pass as the first pass can result in new combinations
    of escape sequence. Ex '\x1b\x1b\x0e' -> '\x1b\x0e'
    """
    in_data = bytearray(data)
    out = bytearray()
    while in_data:
        byte = in_data.pop(0)

        if byte == 0x1B:
            next_byte = in_data.pop(0)
            if next_byte == 0x0E:
                out.append(0x0D)
            elif next_byte == 0x1B:
                out.append(0x1B)
            elif next_byte == 0x0F:
                out.append(0x8D)
            else:
                out.append(byte)
                out.append(next_byte)
        else:
            out.append(byte)

    return bytes(out)


def pad_password(password: str):
    """
    Passwords are 6 characters long. But are sent as 10 characters where the last
    4 characters are insignificant.
    """
    possible_chars = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ0123456789"
    two_random = random.choices(possible_chars, k=2)
    # return password + "".join(four_random)
    return password + "!\x04" + "".join(two_random)


def bytes_to_datetime(data: bytes) -> Tuple[datetime, bool, bool]:
    """
    BCD of 6 bytes  seconds, minutes, hour, day, month, year
    10 33 12 30 05 06 == 2006-05-30T12:33:10
    """
    if len(data) != 6:
        raise ValueError(f"{data!r} is not a BCD encoded datetime")
    second = from_bcd(data[0:1])
    minute = from_bcd(data[1:2])
    hour_data = data[2]
    hour_byte = (hour_data & 0b00111111).to_bytes(1, "little")
    hour = from_bcd(hour_byte)
    is_dst = bool(hour_data & 0b10000000)
    supports_dst = bool(hour_data & 0b01000000)
    day = from_bcd(data[3:4])
    month = from_bcd(data[4:5])
    # The year is only the last 2 digits. We set it so all dates are in the 20xx
    # I will probably be retired when it becomes a problem :)
    year = from_bcd(data[5:]) + 2000

    return (
        datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        ),
        is_dst,
        supports_dst,
    )


def datetime_to_bytes(timestamp: datetime) -> bytes:
    """
    Packs a datetime into a BCD encoded format
    """
    out = bytearray()
    out.extend(to_bdc(timestamp.second))
    out.extend(to_bdc(timestamp.minute))
    out.extend(to_bdc(timestamp.hour))
    out.extend(to_bdc(timestamp.day))
    out.extend(to_bdc(timestamp.month))
    out.extend(to_bdc(timestamp.year - 2000))

    return bytes(out)


def to_bdc(number: int) -> bytes:
    """
    4 bit bcd (Binary Coded Decimal)
    Example: Decimal 30 would be encoded with b"\x30" or 0b0011 0000
    """
    chars = str(number)
    if (len(chars) % 2) != 0:
        # pad string to make it a hexadecimal one.
        chars = "0" + chars
    bcd = bytes.fromhex(str(chars))
    return bcd


def from_bcd(data: bytes) -> int:
    """
    make a bcd encoded bytestring into an integer
    Example: b"\x30" should be 30
    """
    chars = data.hex()
    return int(chars)


def pop_many(array: bytearray, amount: int) -> bytearray:
    if amount < 2:
        raise ValueError("Only use pop_many if you need to get more than 1 byte")
    out = bytearray()
    for _ in range(0, amount):
        out.append(array.pop(0))
    return out


def pretty_text(in_data: bytes) -> str:
    """
    To removed data that should not be present in the text but might be on bit-level
    """
    termination_char = b"\x00"

    try:
        last_termination_char = in_data.rindex(termination_char)
        in_data = in_data[:last_termination_char]
    except ValueError:
        # no termination char in text
        pass
    return in_data.replace(b"\x00", b" ").lstrip().rstrip().decode("latin-1")


def parse_ip_address(data: bytes) -> str:
    if len(data) != 4:
        raise ValueError(f"IP addreess data should be 4 bytes, got {len(data)}")
    numbers = [str(x) for x in data]
    return ".".join(numbers)
