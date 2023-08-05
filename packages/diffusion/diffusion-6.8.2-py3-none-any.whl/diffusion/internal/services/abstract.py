""" Module for abstract service definition. """

from __future__ import annotations

import io
from abc import ABC, abstractmethod
from typing import (
    KeysView,
    Iterable,
    Mapping,
    Optional,
    Type,
    TYPE_CHECKING,
    Union,
    ValuesView,
    Any,
    TypeVar,
)

import typing

from typing_extensions import Protocol

from diffusion import datatypes as dt
from diffusion.internal.utils import get_all_subclasses, Model_T
from .exceptions import UnknownServiceError
from diffusion.internal.protocol.exceptions import ReportsError

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession
    from diffusion.internal.protocol.message_types import ServiceMessage
    from diffusion.internal.serialisers import Serialiser, SerialiserMap
    from diffusion.datatypes.foundation.abstract import AbstractDataType

    T = TypeVar('T')


class Service(ABC):
    """ Abstract service definition class. """

    service_id: int = 0
    name: str = ""
    request_serialiser: Serialiser
    response_serialiser: Serialiser

    def __init__(self, incoming_message_type: Optional[Type[ServiceMessage]] = None):
        self.request = ServiceValue(self.request_serialiser)
        self.response = ServiceValue(self.response_serialiser)
        self.message_type = incoming_message_type

    def __repr__(self) -> str:
        return f"{self.name}[{self.service_id}]"

    @abstractmethod
    async def consume(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Consume an inbound message. """

    @abstractmethod
    async def produce(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Send an outbound message. """

    @classmethod
    def get_by_id(cls, service_id: int) -> Type[Service]:
        """ Locate and return a service class based on the service ID. """
        for subclass in get_all_subclasses(cls):
            if subclass.service_id == service_id:
                return subclass
        raise UnknownServiceError("Unknown service ID %s", service_id)

    @classmethod
    def get_by_name(cls, service_name: str) -> Type[Service]:
        """ Locate and return a service class based on the service name. """
        for subclass in get_all_subclasses(cls):
            if subclass.name == service_name:
                return subclass
        raise UnknownServiceError("Unknown service name '%s'", service_name)

    async def respond(self, session: InternalSession) -> None:
        """Send a response to a request.

        It is only needed for inbound messages, but is implemented
        here for the sake of type-checking. Does nothing by default.
        """
        ...  # pragma: no cover


class OutboundService(Service):
    """ Abstract class for client-to-server services. """

    def _write_request(self, stream: io.BytesIO) -> None:
        """ Write the value of the request attribute to the stream. """
        self.request_serialiser.write(stream, *self.request.values())

    def _read_response(self, stream: io.BytesIO) -> None:
        """ Read the value of the response attribute from the stream. """
        self.response.set(*self.response_serialiser.read(stream))

    async def consume(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Receive the response from the server. """
        self._read_response(stream)

    async def produce(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Send the request to the server. """
        self._write_request(stream)


class InboundService(Service):
    """ Abstract class for server-to-client services. """

    def _read_request(self, stream: io.BytesIO) -> None:
        """ Read the value of the request attribute from the stream. """
        result = self.request_serialiser.read(stream)
        self.request.set(*result)

    def _write_response(self, stream: io.BytesIO) -> None:
        """ Write the value of the response attribute to the stream. """
        self.response_serialiser.write(stream, *self.response.values())

    async def consume(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Receive the request from the server. """
        self._read_request(stream)

    async def produce(self, stream: io.BytesIO, session: InternalSession) -> None:
        """ Send the response to the server. """
        self._write_response(stream)


class Serialisable(Protocol):
    @classmethod
    def from_fields(cls: typing.Type[T], **kwargs) -> T:
        pass

    @classmethod
    def attr_mappings(cls) -> typing.Dict[str, typing.Any]:
        pass


Serialisable_T = TypeVar('Serialisable_T', bound=Serialisable)


class ServiceValue(Mapping[Union[str, int], Any], Iterable):
    """Container for values of Service.request and Service.response fields.

    The exact contents are defined by the associated serialiser. The object
    behaves as both a mapping and an iterator: both the keys and the order
    of values are defined by the accompanying serialiser.
    """

    __slots__ = ["_serialiser", "_values"]

    def __init__(self, serialiser: Serialiser):
        self._serialiser = serialiser
        self._values = dict.fromkeys(serialiser.fields)

    def set(self, *args, **kwargs):
        """Sets the values from the passed arguments.

        Any keyword arguments will override any positional arguments. For
        example, if the first value is named `foo`, then
        `value.set(123, foo=456)` will set `foo` to 456 and not 123.
        """
        values = dict(zip(self._values, args))
        values.update(kwargs)
        for field, value in values.items():
            self[field] = value

    def keys(self) -> KeysView:
        """ Returns an iterable of all field names. """
        return self._values.keys()

    def values(self) -> ValuesView:
        """ Returns an iterable of all values. """
        return self._values.values()

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self):
        return iter(self._values.items())

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, int):
            return list(self.values())[item]
        return self._values[self._check_item_key(item)]

    def __setitem__(self, item: Union[str, int], value):
        if isinstance(item, int):
            item = list(self.keys())[item]
        if isinstance(value, dt.DataType):
            self.serialised_value = value
        else:
            self._values[self._check_item_key(item)] = value

    def sanitize_key(self, key):
        item_key = key
        if item_key not in self._values:
            item_key = f"{self._serialiser.name}.{key}"
        if item_key not in self._values:
            return None
        return item_key

    def _check_item_key(self, key):
        """Check if an item key omits the serialiser name.

        Serialiser map keys include the serialiser name to ensure uniqueness.
        This allows the convenience of omitting the serialiser name when
        setting or getting an item, so instead of:

            value["messaging-client-forward-send-request.conversation-id"]

        one can use only:

            value["conversation-id"]
        """
        item_key = self.sanitize_key(key)
        if not item_key:
            raise KeyError(f"Unknown field '{item_key}'")
        return item_key

    def __contains__(self, item):
        return item in self._values

    def __repr__(self):
        return (
            f"{type(self).__name__}(serialiser={self._serialiser.name},"
            f" values={tuple(self._values.values())})"
        )

    @property
    def spec(self) -> SerialiserMap:
        """ Returns the serialiser's spec mapping. """
        return self._serialiser.spec

    @property
    def serialised_value(self) -> Optional[dt.DataType]:
        """Retrieves the value of any serialised DataType field in the value.

        Raises a TypeError if there are no any such fields, or if there
        are more than one.
        """
        serialised_fields = self._get_serialised_value_fields()
        data_type_name, bytes_value = serialised_fields.values()
        if bytes_value is None:
            return None
        return dt.get(data_type_name).from_bytes(bytes_value)

    @serialised_value.setter
    def serialised_value(self, value: AbstractDataType):
        """Sets the value of any serialised DataType field in the value.

        Raises a TypeError if there are no any such fields, or if there
        are more than one.
        """
        serialised_fields = self._get_serialised_value_fields()
        for key, value in zip(serialised_fields, value.serialised_value.values()):
            self[key] = value

    def _get_serialised_value_fields(self):
        serialised_fields = [field for field in self.spec if "serialised-value" in field]
        length = len(serialised_fields)
        if length > 2:
            raise TypeError(
                f"The '{self._serialiser.name}' serialiser has multiple serialised values."
            )
        if length < 2:
            raise TypeError(
                f"The '{self._serialiser.name}' serialiser does not have a serialised value."
            )
        return {field: self[field] for field in serialised_fields}

    def deserialise(self, target: Type[Serialisable_T]) -> Serialisable_T:
        fields = {
            (target.attr_mappings().get(k) or getattr(target, k)).__name__: v
            for k, v in zip(self.spec.keys(), self.values())
        }
        try:
            materialise = target.from_fields
        except AttributeError:
            materialise = target
        return materialise(**fields)

    def deserialise_model(self, target: Type[Model_T]) -> Model_T:
        model_to_serialiser_mapping = {
            model_key: self.sanitize_key(model_field.alias)
            for model_key, model_field in target.__fields__.items()
        }
        fields = {
            model_key: target.Config.decode(self[serialiser_key])
            for model_key, serialiser_key in model_to_serialiser_mapping.items()
            if serialiser_key
        }
        try:
            return target(**fields)
        except Exception as e:
            raise e

    async def error_from(self, tp: Type[ReportsError]):
        await self._serialiser.error_from(self, tp)
