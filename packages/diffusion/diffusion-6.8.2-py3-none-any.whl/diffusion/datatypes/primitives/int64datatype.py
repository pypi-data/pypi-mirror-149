from typing import Optional

from diffusion.datatypes.exceptions import InvalidDataError
from .primitivedatatype import PrimitiveDataType


class Int64DataType(PrimitiveDataType):
    """Data type that supports 64-bit, signed integer values.

    The integer value is serialized as CBOR-format binary. A serialized value
    can be read as JSON instance.
    """

    type_code = 18
    type_name = "int64"
    MAX_VALUE = 1 << 63
    MIN_VALUE = -MAX_VALUE + 1

    def __init__(self, value: Optional[int]):
        super().__init__(value)

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        message = ""
        if self.value is not None:
            if not isinstance(self.value, int):
                message = f"Expected an integer but got {type(self.value).__name__}"
            elif not self.MIN_VALUE <= self.value <= self.MAX_VALUE:
                message = "Integer value out of bounds."
        if message:
            raise InvalidDataError(message)
