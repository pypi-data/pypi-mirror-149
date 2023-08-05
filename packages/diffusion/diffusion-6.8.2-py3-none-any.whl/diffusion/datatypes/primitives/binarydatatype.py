from typing import Optional

from diffusion.datatypes.exceptions import InvalidDataError
from .primitivedatatype import PrimitiveDataType


class BinaryDataType(PrimitiveDataType):
    """ Data type that supports arbitrary binary data. """

    type_code = 14
    type_name = "binary"

    def __init__(self, value: Optional[bytes]) -> None:
        super().__init__(value)

    @classmethod
    def encode(cls, value) -> bytes:
        """ Convert the value into the binary representation. """
        return value

    @classmethod
    def decode(cls, data: bytes) -> bytes:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            Deserialised value.
        """
        return data

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        if not (self.value is None or isinstance(self.value, bytes)):
            raise InvalidDataError(f"Expected bytes but got {type(self.value).__name__}")

    def __str__(self):
        return self.value.decode()
