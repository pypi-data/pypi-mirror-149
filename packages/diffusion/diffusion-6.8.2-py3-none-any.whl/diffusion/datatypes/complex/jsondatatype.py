from __future__ import annotations

from typing import Optional, Union

from diffusion.datatypes.foundation.abstract import AbstractDataType
from diffusion.datatypes.exceptions import InvalidDataError

JsonTypes = Union[dict, list, str, int, float]


class JsonDataType(AbstractDataType):
    """ JSON data type implementation. """

    type_code = 15
    type_name = "json"
    valid_types = JsonTypes.__args__  # type: ignore

    def __init__(self, value: Optional[JsonTypes]) -> None:
        super().__init__(value)

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        if not (self.value is None or isinstance(self.value, self.valid_types)):
            raise InvalidDataError(
                "The value must be either None, or one of the following types:"
                f" {', '.join(t.__name__ for t in self.valid_types)};"
                f" got {type(self.value).__name__} instead."
            )
