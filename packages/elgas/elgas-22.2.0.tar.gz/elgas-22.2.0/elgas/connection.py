from __future__ import annotations

from typing import *

import attr
import structlog

from elgas import application, constants, exceptions, frames, security, state, utils

LOG = structlog.get_logger("connection")


@attr.s(auto_attribs=True)
class ResponsePduFactory:
    """
    Creates PDU classes from Elgas Responses via the service number.
    """

    service_map: ClassVar[Mapping] = {
        constants.ServiceNumber.READ_VALUES: application.ReadInstantaneousValuesResponse,
        constants.ServiceNumber.READ_DEVICE_TIME: application.ReadTimeResponse,
        constants.ServiceNumber.READ_SCADA_PARAMETERS: application.ReadDeviceParametersResponse,
        constants.ServiceNumber.READ_ARCHIVES_BY_DATE: application.ReadArchiveByTimeResponse,
        constants.ServiceNumber.READ_ARCHIVES: application.ReadArchiveResponse,
        constants.ServiceNumber.WRITE_DEVICE_TIME: application.WriteTimeResponse,
    }

    @staticmethod
    def from_response(response: frames.Response):
        klass = ResponsePduFactory.service_map[response.service]
        return klass.from_bytes(response.data)


def create_cipher_context(
    connection: "ElgasConnection",
) -> Optional[security.CipherContext]:
    """
    If both encryption key and encryption key id is set then return a cipher context
    """
    if connection.encryption_key is None or connection.encryption_key_id is None:
        return None
    else:
        return security.CipherContext(
            connection.encryption_key_id, connection.encryption_key
        )


def raise_error(data: bytes):
    error = data[0]
    if error == 0b00000001:
        raise exceptions.WrongPasswordError()
    elif error == 0b00000010:
        raise exceptions.SettingArchiveFull()
    elif error == 0b00000100:
        raise exceptions.SwitchOff()
    elif error == 0b00001000:
        raise exceptions.BlockedBuffer()
    elif error == 0b00010000:
        raise exceptions.DataError()
    elif error == 0b00100000:
        raise exceptions.CipherKeyError()
    elif error == 0b01000000:
        raise exceptions.WrongEncryptionKeysError()
    elif error == 0b10000000:
        raise exceptions.WriteError()


@attr.s(auto_attribs=True)
class ElgasConnection:
    """
    address1 is used for addressing measuring place  0-65535
    address2 is used for addressing concrete measuring place 0-255
    TODO: exactly what does that mean?..
    Address 0 in any will make all devices respond. In the response the correct
    address will be sent.


    """

    source_address_1: int = attr.ib(
        validator=[attr.validators.ge(0), attr.validators.le(65535)]
    )
    source_address_2: int = attr.ib(
        validator=[attr.validators.ge(0), attr.validators.le(255)]
    )
    destination_address_1: int = attr.ib(
        validator=[attr.validators.ge(0), attr.validators.le(65535)]
    )
    destination_address_2: int = attr.ib(
        validator=[attr.validators.ge(0), attr.validators.le(255)]
    )

    password: str = attr.ib(validator=[attr.validators.max_len(6)])
    password_id: int = attr.ib(
        validator=[attr.validators.ge(801), attr.validators.le(849)]
    )

    encryption_key: Optional[bytes] = attr.ib(default=None)
    encryption_key_id: Optional[security.EncryptionKeyId] = attr.ib(default=None)
    # TODO: Validate that there is an encryption key id if there is an encryption key.

    buffer: bytearray = attr.ib(init=False, factory=bytearray)
    elgas_state: state.ElgasState = attr.ib(factory=state.ElgasState)
    cipher_context: Optional[security.CipherContext] = attr.ib(
        default=attr.Factory(lambda self: create_cipher_context(self), takes_self=True)
    )

    def send(self, event) -> bytes:

        LOG.debug("Sending request PDU", pdu=event)
        self.elgas_state.process_event(event)
        application_data = event.to_bytes()

        if self.cipher_context:
            # replace application_data with encrypted data.

            request = frames.EncryptedRequest(
                service=event.service,
                destination_address_1=self.destination_address_1,
                destination_address_2=self.destination_address_2,
                source_address_1=self.source_address_1,
                source_address_2=self.source_address_2,
                data=self.cipher_context.encrypt(application_data),
            )

        else:
            request = frames.Request(
                service=event.service,
                destination_address_1=self.destination_address_1,
                destination_address_2=self.destination_address_2,
                source_address_1=self.source_address_1,
                source_address_2=self.source_address_2,
                data=application_data,
            )

        LOG.debug("Sending ELGAS request", request=request)
        frame_data = request.to_bytes()
        escaped_data = utils.escape_characters(frame_data)
        return escaped_data

    def receive_data(self, data: bytes):
        """
        Add data into the receive buffer. Also deescape the data so correct data is in
        the buffer.
        After this you could call next_event
        """
        if data:
            if data == b"\x0d" and len(self.buffer) == 0:
                LOG.info(
                    "Received an end char when read buffer was empty. This is a"
                    " known issue and data is ignored."
                )
                return

            self.buffer += data
            LOG.debug(
                f"Added data to connection buffer", data=data, total_buffer=self.buffer
            )

    def next_event(self) -> bytes:

        if not self.buffer:
            LOG.debug("Buffer empty. Need more data")
            return state.NEED_DATA

        # do we have an end char?
        try:
            end_char_index = self.buffer.index(b"\x0d") + 1
        except ValueError:
            # No end char in buffer and we need more data.
            LOG.debug("No end char in data. Need more data")
            return state.NEED_DATA

        data = self.buffer[:end_char_index]
        try:
            response = frames.ResponseFactory.from_bytes(utils.return_characters(data))

            LOG.debug("Received ELGAS response", response=response)

            if isinstance(response, frames.EncryptedResponse):
                response.data = self.cipher_context.decrypt(response.data)
                LOG.debug("Decrypted ELGAS response", decrypted=response)

            if len(response.data) == 1:
                raise_error(response.data)

        except ValueError:
            LOG.debug("Cannot interpret data as frame. Need more data")
            return state.NEED_DATA

        pdu = ResponsePduFactory.from_response(response)
        LOG.info("Received PDU", pdu=pdu)
        self.elgas_state.process_event(pdu)

        self.buffer = bytearray()  # clear buffer

        return pdu
