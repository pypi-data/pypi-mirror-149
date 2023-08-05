""" Protocol-related exceptions. """
import attr
from typing import List
from diffusion.internal.exceptions import DiffusionError


class ProtocolError(ConnectionError, DiffusionError):
    """ General protocol error. """


class ServerConnectionError(ProtocolError):
    """ General error when connecting to server. """


class ServerDisconnectedError(ProtocolError):
    """ General error when server disconnected """
    def __init__(self):
        super().__init__("Not connected to Diffusion server!")


class ServerConnectionResponseError(ServerConnectionError):
    """ Error when the server returns a non-OK code on connection. """

    def __init__(self, response_code):
        super().__init__(f"Failed to connect: {response_code.name}")
        self.response_code = response_code


class ServiceMessageError(ProtocolError):
    """ Error when handling service messages. """


@attr.s(auto_attribs=True)
class ErrorReport(object):
    message: str
    line: int
    column: int


class ReportsError(DiffusionError):
    def __init__(self, reports: List[ErrorReport], msg: str = None):
        super().__init__(msg or f"{msg or type(self)} caused by {reports}")
        self.reports = reports


class InvalidSessionFilterError(ReportsError):
    def __init__(self, reports: List[ErrorReport], msg: str = None):
        super().__init__(reports, msg)


class AbortMessageError(ServiceMessageError):
    """ Abort message received from the server. """


# Conversation errors.


class ConversationError(DiffusionError):
    """ Base conversation error. """


class CIDGeneratorExhaustedError(ConversationError):
    """ Error stating that a CID generator was exhausted. """


class NoSuchConversationError(ConversationError):
    """ The conversation with this CID does not exist in the `ConversationSet`. """

    def __init__(self, cid):
        super().__init__(f"Unknown conversation {cid}")
