from typing import Optional

from diffusion.datatypes.exceptions import InvalidDataError
from .primitivedatatype import PrimitiveDataType


class DoubleDataType(PrimitiveDataType):
    """Data type that supports double-precision floating point numbers.

    (Eight-byte IEEE 754)

    The integer value is serialized as CBOR-format binary. A serialized value
    can be read as a JSON instance.
    """

    type_code = 19
    type_name = "double"

    def __init__(self, value: Optional[float]):
        super().__init__(value)

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        if not (self.value is None or isinstance(self.value, float)):
            raise InvalidDataError(f"Expected a float but got {type(self.value).__name__}")
