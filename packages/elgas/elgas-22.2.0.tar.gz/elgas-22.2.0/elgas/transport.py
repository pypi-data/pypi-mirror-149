import socket
import time
from typing import *

import attr
import serial
import structlog

from elgas import exceptions

LOG = structlog.get_logger("transport")


class Timeout:
    """"""

    def __init__(self, duration):
        """Initialize a timeout with given duration"""
        self.is_infinite = duration is None
        self.is_non_blocking = duration == 0
        self.duration = duration
        if duration is not None:
            self.target_time = time.monotonic() + duration
        else:
            self.target_time = None

    def expired(self):
        """Return a boolean, telling if the timeout has expired"""
        return self.target_time is not None and self.time_left() <= 0

    def time_left(self):
        """Return how many seconds are left until the timeout expires"""
        if self.is_non_blocking:
            return 0
        elif self.is_infinite:
            return None
        else:
            delta = self.target_time - time.monotonic()
            if delta > self.duration:
                # clock jumped, recalculate
                self.target_time = time.monotonic() + self.duration
                return self.duration
            else:
                return max(0, delta)

    def restart(self, duration):
        """\
        Restart a timeout, only supported if a timeout was already set up
        before.
        """
        self.duration = duration
        self.target_time = time.monotonic() + duration


class ElgasTransport(Protocol):
    def connect(self):
        ...

    def disconnect(self):
        ...

    def send(self, data: bytes):
        ...

    def recv(self):
        ...


@attr.s(auto_attribs=True)
class BlockingTcpTransport:
    """
    A TCP transport using Blocking I/O.
    """

    host: str
    port: int
    timeout: int = attr.ib(default=10)
    tcp_socket: Optional[socket.socket] = attr.ib(init=False, default=None)

    @property
    def address(self) -> Tuple[str, int]:
        return self.host, self.port

    def connect(self):
        """
        Create a new socket and set it on the transport
        """
        if self.tcp_socket:
            raise RuntimeError(f"There is already an active socket to {self.address}")

        try:
            self.tcp_socket = socket.create_connection(
                address=self.address, timeout=self.timeout
            )
        except (
            OSError,
            IOError,
            socket.timeout,
            socket.error,
            ConnectionRefusedError,
        ) as e:
            raise exceptions.CommunicationError("Unable to connect socket") from e
        LOG.info(f"Connected to {self.address}")

    def disconnect(self):
        """
        Close socket and remove it from the transport. No-op if the socket is already
        closed.
        """
        if self.tcp_socket:
            # only disconnect if there is a socket.
            try:
                self.tcp_socket.shutdown(socket.SHUT_RDWR)
                self.tcp_socket.close()
            except (OSError, IOError, socket.timeout, socket.error) as e:
                self.tcp_socket = None
                raise exceptions.CommunicationError from e
            self.tcp_socket = None
            LOG.info(f"Connection to {self.address} is closed")

    def send(self, data: bytes):
        """"""
        if not self.tcp_socket:
            raise RuntimeError("TCP transport not connected.")
        try:
            self.tcp_socket.sendall(data)
            LOG.debug(f"Sent data", data=data, transport=self)
        except (OSError, IOError, socket.timeout, socket.error) as e:
            raise exceptions.CommunicationError("Could no send data") from e

    def recv(self) -> bytes:
        """"""
        try:
            data = self.recv_until()
            LOG.debug("Received data", data=data, transport=self)
        except (OSError, IOError, socket.timeout, socket.error) as e:
            raise exceptions.CommunicationError("Could not receive data") from e
        return data

    def _recv_bytes(self, amount: int):
        """
        Some implementations will return partial data, and we need to keep on trying
        to read the bytes until we have them all.
        """
        if not self.tcp_socket:
            raise RuntimeError("TCP transport not connected.")

        data = b""
        while len(data) < amount:
            data += self.tcp_socket.recv(amount - len(data))

        return data

    def recv_until(self, expected=b"\x0d", size=None):
        """\
        Read until an expected sequence is found ('\r' by default), the size
        is exceeded or until timeout occurs.
        """
        lenterm = len(expected)
        line = bytearray()
        timeout = Timeout(self.timeout)
        while True:
            c = self._recv_bytes(1)
            if c:
                line += c
                if line[-lenterm:] == expected:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break
            if timeout.expired():
                break
        return bytes(line)


@attr.s(auto_attribs=True)
class SerialTransport:
    """
    A Serial transport
    """

    port: str
    baud_rate: int
    timeout: int = attr.ib(default=10)
    serial_port: Optional[serial.Serial] = attr.ib(init=False, default=None)

    def connect(self):
        """
        Create a new socket and set it on the transport
        """
        if self.serial_port:
            raise RuntimeError(f"There is already an active serial port")

        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=self.timeout,
            )
        except (
            OSError,
            IOError,
            serial.SerialException,
        ) as e:
            raise exceptions.CommunicationError("Unable to connect socket") from e
        LOG.info(f"Connected to {self.port}")

    def disconnect(self):
        """
        Close socket and remove it from the transport. No-op if the socket is already
        closed.
        """
        if self.serial_port:
            # only disconnect if there is a socket.
            try:
                self.serial_port.close()
            except (OSError, IOError, serial.SerialException) as e:
                self.serial_port = None
                raise exceptions.CommunicationError from e
            self.serial_port = None
            LOG.info(f"Connection to {self.port} is closed")

    def send(self, data: bytes):
        """"""
        if not self.serial_port:
            raise RuntimeError("Serial transport not connected.")
        try:
            self.serial_port.write(data)
            LOG.debug(f"Sent data", data=data, transport=self)
        except (OSError, IOError, serial.SerialException) as e:
            raise exceptions.CommunicationError("Could no send data") from e

    def recv(self) -> bytes:
        """"""
        try:
            data = self.recv_until()
            LOG.debug("Received data", data=data, transport=self)
        except (OSError, IOError, serial.SerialException) as e:
            raise exceptions.CommunicationError("Could not receive data") from e
        return data

    def _recv_bytes(self, amount: int):
        """
        Some implementations will return partial data, and we need to keep on trying
        to read the bytes until we have them all.
        """
        if not self.serial_port:
            raise RuntimeError("TCP transport not connected.")

        data = b""
        while len(data) < amount:
            data += self.serial_port.read(amount - len(data))

        return data

    def recv_until(self, expected=b"\x0d", size=None):
        """\
        Read until an expected sequence is found ('\r' by default), the size
        is exceeded or until timeout occurs.
        """
        lenterm = len(expected)
        line = bytearray()
        timeout = Timeout(self.timeout)
        while True:
            c = self._recv_bytes(1)
            if c:
                line += c
                if line[-lenterm:] == expected:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break
            if timeout.expired():
                break
        return bytes(line)
