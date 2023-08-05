import attr
import structlog

from elgas import application, exceptions

LOG = structlog.get_logger("state")


class _SentinelBase(type):
    """
    Sentinel values

     - Inherit identity-based comparison and hashing from object
     - Have a nice repr
     - Have a *bonus property*: type(sentinel) is sentinel

     The bonus property is useful if you want to take the return value from
     next_event() and do some sort of dispatch based on type(event).

     Taken from h11.
    """

    def __repr__(self):
        return self.__name__


def make_sentinel(name):
    cls = _SentinelBase(name, (_SentinelBase,), {})
    cls.__class__ = cls
    return cls


IDLE = make_sentinel("IDLE")
AWAITING_READ_ACTUAL_VALUES_RESPONSE = make_sentinel(
    "AWAITING_READ_ACTUAL_VALUES_RESPONSE"
)
AWAITING_READ_DEVICE_PARAMETERS_RESPONSE = make_sentinel(
    "AWAITING_READ_DEVICE_PARAMETERS_RESPONSE"
)
AWAITING_READ_TIME_RESPONSE = make_sentinel("AWAITING_READ_TIME_RESPONSE")
AWAITING_READ_ARCHIVE_BY_TIME_RESPONSE = make_sentinel(
    "AWAITING_READ_ARCHIVE_BY_TIME_RESPONSE"
)
AWAITING_READ_ARCHIVE_RESPONSE = make_sentinel("AWAITING_READ_ARCHIVE_RESPONSE")

AWAITING_WRITE_TIME_RESPONSE = make_sentinel("AWAITING_WRITE_TIME_RESPONSE")
NEED_DATA = make_sentinel("NEED_DATA")


ELGAS_STATE_TRANSITIONS = {
    IDLE: {
        application.ReadInstantaneousValuesRequest: AWAITING_READ_ACTUAL_VALUES_RESPONSE,
        application.ReadDeviceParametersRequest: AWAITING_READ_DEVICE_PARAMETERS_RESPONSE,
        application.ReadTimeRequest: AWAITING_READ_TIME_RESPONSE,
        application.ReadArchiveByTimeRequest: AWAITING_READ_ARCHIVE_BY_TIME_RESPONSE,
        application.ReadArchiveRequest: AWAITING_READ_ARCHIVE_RESPONSE,
        application.WriteTimeRequest: AWAITING_WRITE_TIME_RESPONSE,
    },
    AWAITING_READ_ACTUAL_VALUES_RESPONSE: {
        application.ReadInstantaneousValuesResponse: IDLE,
    },
    AWAITING_READ_DEVICE_PARAMETERS_RESPONSE: {
        application.ReadDeviceParametersResponse: IDLE
    },
    AWAITING_READ_TIME_RESPONSE: {application.ReadTimeResponse: IDLE},
    AWAITING_READ_ARCHIVE_BY_TIME_RESPONSE: {
        application.ReadArchiveByTimeResponse: IDLE
    },
    AWAITING_READ_ARCHIVE_RESPONSE: {application.ReadArchiveResponse: IDLE},
    AWAITING_WRITE_TIME_RESPONSE: {application.WriteTimeResponse: IDLE},
}


@attr.s(auto_attribs=True)
class ElgasState:
    """
    Handles state changes in ELGAS Protocol
    """

    current_state: _SentinelBase = attr.ib(default=IDLE)

    def process_event(self, event):

        event_type = type(event)

        try:
            new_state = ELGAS_STATE_TRANSITIONS[self.current_state][event_type]
        except KeyError:
            raise exceptions.LocalElgasProtocolError(
                f"Can't handle {event_type} when state={self.current_state}"
            )
        old_state = self.current_state
        self.current_state = new_state
        LOG.debug(f"Elgas state transitioned from {old_state} to {new_state}")
