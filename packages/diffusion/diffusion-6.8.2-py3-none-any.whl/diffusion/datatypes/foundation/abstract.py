""" Core definitions of data types. """
from __future__ import annotations

from typing import Any, Optional

from io import BytesIO

from diffusion.datatypes.exceptions import InvalidDataError
from .datatype import DataType
from diffusion.internal.encoder import Encoder, DefaultEncoder


class AbstractDataType(DataType):
    encoder: Encoder = DefaultEncoder()

    def __init__(self, value: Optional[Any]) -> None:
        super().__init__(value)

    def write_value(self, stream: BytesIO) -> BytesIO:
        """Write the value into a binary stream.

        Args:
            stream: Binary stream to serialise the value into.
        """
        stream.write(self.encode(self.value))
        return stream

    def to_bytes(self) -> bytes:
        """ Convert the value into the binary representation.

        Convenience method, not to be overridden"""

        return self.encoder.dumps(self.value)

    @classmethod
    def read_value(cls, stream: BytesIO) -> Optional[AbstractDataType]:
        """Read the value from a binary stream.

        Args:
            stream: Binary stream containing the serialised data.

        Returns:
            An initialised instance of the DataType.
        """
        return cls.from_bytes(stream.read())

    @property
    def value(self):
        """ Current value of the instance. """
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        if isinstance(value, bytes):
            value = self.decode(value)
        self._value = value

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional[AbstractDataType]:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            An initialised instance of the DataType.
        """
        value = cls.decode(data)
        if value is None:
            return None
        return cls(value)

    @property
    def serialised_value(self) -> dict:
        """Return the sequence of values ready to be serialised.

        It is assumed that the serialisation will use the
        `serialised-value` serialiser.
        """
        return {"data-type-name": self.type_name, "bytes": self.encode(self.value)}

    @classmethod
    def encode(cls, value: Any) -> bytes:
        """Convert a value into the corresponding binary representation.

        Args:
            value:
                Native value to be serialised

        Returns:
            Serialised binary representation of the value.
        """
        return cls.encoder.dumps(value)

    @classmethod
    def decode(cls, data: bytes) -> Any:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            Deserialised value.
        """
        with BytesIO(data) as fp:
            value = cls.encoder.load(fp)
            if len(fp.read(1)) > 0:
                raise InvalidDataError("Excess CBOR data")
        return value

    def set_from_bytes(self, data: bytes) -> None:
        """ Convert bytes and set the corresponding value on the instance. """
        self.value = self.decode(data)

    def __eq__(self, other) -> bool:
        try:
            return self.type_name == other.type_name and self.value == other.value
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return f"<{type(self).__name__} value={self.value}>"

    def __str__(self) -> str:
        return str(self.value)
