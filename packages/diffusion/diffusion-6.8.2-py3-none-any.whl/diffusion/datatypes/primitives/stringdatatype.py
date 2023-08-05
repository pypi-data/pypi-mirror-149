from typing import Optional

from diffusion.datatypes.exceptions import InvalidDataError
from .primitivedatatype import PrimitiveDataType


class StringDataType(PrimitiveDataType):
    """String data type.

    The string value is serialized as CBOR-format binary.
    """

    type_code = 17
    type_name = "string"

    def __init__(self, value: Optional[str]):
        super().__init__(value)

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        if not (self.value is None or isinstance(self.value, str)):
            raise InvalidDataError("Expected string but got {type(self.value).__name__}")

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
