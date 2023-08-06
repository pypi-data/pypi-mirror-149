from typing import ClassVar, Optional

import attr
import marshmallow

from elgas.parameters.enumerations import ParameterObjectType
from elgas.utils import parse_ip_address, pop_many, pretty_text


@attr.s(auto_attribs=True)
class Modem:
    object_type: ClassVar[ParameterObjectType] = ParameterObjectType.MODEM

    number: int
    bit_control_0: int
    title: str
    modem_type: int
    initialization: str
    call_to_dispatching: str
    modem_hang_up: str
    special_initialization: str
    ip_address_for_registration_and_diagnostics: str
    ip_address_for_calling_to_dispatching: str
    registration_send_period: int
    authentication_mode: int
    port_for_registration: int
    port_for_calling_to_dispatching: int
    sms_call: str
    gprs_user_name: str
    gprs_password: str
    ip_address_for_ping: str
    ping_period: int
    transition_into_command_mode: str
    pin: str
    owner_sim_number: Optional[str]

    @classmethod
    def from_bytes(cls, in_data: bytes):
        data = bytearray(in_data)
        number = data.pop(0)
        bit_control_0 = data.pop(0)
        title = pretty_text(pop_many(data, 7))
        modem_type = data.pop(0)
        initialization = pretty_text(pop_many(data, 32))
        call_to_dispatching = pretty_text(pop_many(data, 32))
        modem_hang_up = pretty_text(pop_many(data, 8))
        special_initialization = pretty_text(pop_many(data, 80))
        ip_address_for_registration_and_diagnostics = parse_ip_address(
            pop_many(data, 4)
        )
        ip_address_for_calling_to_dispatching = parse_ip_address(pop_many(data, 4))
        registration_send_period = data.pop(0)
        authentication_mode = data.pop(0)
        port_for_registration = int.from_bytes(pop_many(data, 2), "little")
        port_for_calling_to_dispatching = int.from_bytes(pop_many(data, 2), "little")
        sms_call = pretty_text(pop_many(data, 32))
        gprs_user_name = pretty_text(pop_many(data, 49))
        gprs_password = pop_many(data, 33).hex()
        ip_address_for_ping = parse_ip_address(pop_many(data, 4))
        ping_period = int.from_bytes(pop_many(data, 2), "little")
        transition_into_command_mode = pretty_text(pop_many(data, 8))
        pin = pop_many(data, 9).hex()
        owner_sim_number = pretty_text(pop_many(data, 17))

        assert not data  # Should be empty now

        return cls(
            number=number,
            bit_control_0=bit_control_0,
            title=title,
            modem_type=modem_type,
            initialization=initialization,
            call_to_dispatching=call_to_dispatching,
            modem_hang_up=modem_hang_up,
            special_initialization=special_initialization,
            ip_address_for_registration_and_diagnostics=ip_address_for_registration_and_diagnostics,
            ip_address_for_calling_to_dispatching=ip_address_for_calling_to_dispatching,
            registration_send_period=registration_send_period,
            authentication_mode=authentication_mode,
            port_for_registration=port_for_registration,
            port_for_calling_to_dispatching=port_for_calling_to_dispatching,
            sms_call=sms_call,
            gprs_user_name=gprs_user_name,
            gprs_password=gprs_password,
            ip_address_for_ping=ip_address_for_ping,
            ping_period=ping_period,
            transition_into_command_mode=transition_into_command_mode,
            pin=pin,
            owner_sim_number=owner_sim_number,
        )


class ModemSchema(marshmallow.Schema):

    number = marshmallow.fields.Integer(required=True)
    bit_control_0 = marshmallow.fields.Integer(required=True)
    title = marshmallow.fields.String(required=True)
    modem_type = marshmallow.fields.Integer(required=True)
    initialization = marshmallow.fields.String(required=True)
    call_to_dispatching = marshmallow.fields.String(required=True)
    modem_hang_up = marshmallow.fields.String(required=True)
    special_initialization = marshmallow.fields.String(required=True)
    ip_address_for_registration_and_diagnostics = marshmallow.fields.String(
        required=True
    )
    ip_address_for_calling_to_dispatching = marshmallow.fields.String(required=True)
    registration_send_period = marshmallow.fields.Integer(required=True)
    authentication_mode = marshmallow.fields.Integer(required=True)
    port_for_registration = marshmallow.fields.Integer(required=True)
    port_for_calling_to_dispatching = marshmallow.fields.Integer(required=True)
    sms_call = marshmallow.fields.String(required=True)
    gprs_user_name = marshmallow.fields.String(required=True)
    gprs_password = marshmallow.fields.String(required=True)
    ip_address_for_ping = marshmallow.fields.String(required=True)
    ping_period = marshmallow.fields.Integer(required=True)
    transition_into_command_mode = marshmallow.fields.String(required=True)
    pin = marshmallow.fields.String(required=True)
    owner_sim_number = marshmallow.fields.String(required=True, allow_none=True)
