import datetime
from typing import *

import attr
import structlog

from elgas import application, connection, constants, parser, state, transport, utils

LOG = structlog.get_logger("client")


@attr.s(auto_attribs=True)
class ElgasClient:
    """Elgas client"""

    transport: transport.ElgasTransport
    password: str = attr.ib(converter=utils.to_secret_str)
    password_id: int
    encryption_key: Optional[bytes] = attr.ib(
        converter=utils.to_secret_byte, default=None
    )
    encryption_key_id: Optional[int] = attr.ib(default=None)
    # device_configuration: List[object]
    elgas_connection: connection.ElgasConnection = attr.ib(
        default=attr.Factory(
            lambda self: connection.ElgasConnection(
                password=self.password,
                password_id=self.password_id,
                destination_address_1=0,
                destination_address_2=0,
                source_address_1=0,
                source_address_2=0,
                encryption_key=self.encryption_key,
                encryption_key_id=self.encryption_key_id,
            ),
            takes_self=True,
        )
    )

    def connect(self):
        self.transport.connect()

    def disconnect(self):
        self.transport.disconnect()

    def send(self, *events):
        for event in events:
            data = self.elgas_connection.send(event)
            self.transport.send(data)
            response_data = self.transport.recv()
            self.elgas_connection.receive_data(response_data)

    def next_event(self) -> Any:
        while True:
            event = self.elgas_connection.next_event()
            if event is state.NEED_DATA:
                self.elgas_connection.receive_data(self.transport.recv())
                continue
            return event

    def read_instantaneous_values(self) -> application.ReadInstantaneousValuesResponse:
        LOG.info("Reading instantaneous values")
        request = application.ReadInstantaneousValuesRequest(password=self.password)
        self.send(request)
        response: application.ReadInstantaneousValuesResponse = self.next_event()
        LOG.info("Received instantaneous values")
        return response

    def read_time(self):
        LOG.info("Reading device time")
        request = application.ReadTimeRequest()
        self.send(request)
        response: application.ReadTimeResponse = self.next_event()
        LOG.info("Got device time", time=response.time.isoformat())
        return response.time

    def write_time(self, device_time: datetime):
        LOG.info("Writing time to device", time=device_time.isoformat())
        request = application.WriteTimeRequest(
            password=self.password, device_time=device_time
        )
        self.send(request)
        self.next_event()
        LOG.info("Finished writing time to device")

    def read_parameters(self, read_from: int = 0) -> List[Any]:
        LOG.info(f"Reading device parameters", read_from=read_from)
        should_stop = False
        total_parameter_data = b""
        object_count = read_from
        while not should_stop:
            LOG.info("Requesting device parameters", object_count=object_count)
            request = application.ReadDeviceParametersRequest(
                password=self.password, object_count=object_count, buffer_length=1024
            )
            self.send(request)
            response: application.ReadDeviceParametersResponse = self.next_event()
            LOG.info("Received device parameters", object_amount=response.object_amount)
            total_parameter_data += response.data
            should_stop = response.is_end
            object_count += response.object_amount
            if not should_stop:
                LOG.info("More parameters available", next_object_count=object_count)

        LOG.debug("Received total parameters data", data=total_parameter_data)
        parsed = parser.ScadaParameterParser().parse(total_parameter_data)
        return parsed

    def read_archive(
        self, archive: constants.Archive, amount: int, oldest_record_id: int
    ):
        request = application.ReadArchiveRequest(
            password=self.password,
            archive=archive,
            amount=amount,
            oldest_record_id=oldest_record_id,
        )
        self.send(request)
        response = self.next_event()
        return response

    def read_archive_by_time(
        self, archive: constants.Archive, amount: int, oldest_timestamp: datetime
    ):
        request = application.ReadArchiveByTimeRequest(
            password=self.password,
            archive=archive,
            amount=amount,
            oldest_timestamp=oldest_timestamp,
        )
        self.send(request)
        response = self.next_event()
        return response
