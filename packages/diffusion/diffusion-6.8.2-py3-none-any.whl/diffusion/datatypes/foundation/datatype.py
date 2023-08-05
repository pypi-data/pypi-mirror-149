from __future__ import annotations
import io
from abc import ABC, abstractmethod
from typing import Optional


class DataType(ABC):
    """ Generic parent class for all data types implementations. """

    def __init__(self, value) -> None:
        self._value = value
        self.validate()

    type_code: int
    """ Globally unique numeric identifier for the data type. """
    type_name: str
    """ Globally unique identifier for the data type."""

    @property
    @abstractmethod
    def value(self):
        """ Current value of the instance. """

    @value.setter
    def value(self, value) -> None:
        pass

    @classmethod
    def read_value(cls, stream: io.BytesIO) -> Optional['DataType']:
        """Read the value from a binary stream.

        Args:
            stream: Binary stream containing the serialised data.

        Returns:
            An initialised instance of the DataType.
        """
        raise NotImplementedError()

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid. By default there is no validation.
        """

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional['DataType']:
        raise NotImplementedError()
