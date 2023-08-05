from io import BytesIO
from typing import Optional, Any
import cbor2 as cbor

from diffusion.datatypes.exceptions import InvalidDataError
from diffusion.datatypes.foundation.abstract import AbstractDataType


class PrimitiveDataType(AbstractDataType):
    @classmethod
    def decode(cls, data: bytes) -> Optional[Any]:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            Deserialised value.
        """
        with BytesIO(data) as fp:
            try:
                value = cbor.load(fp)
            except cbor.CBORDecodeError as ex:
                raise InvalidDataError("Invalid CBOR data") from ex
            if len(fp.read(1)) > 0:
                raise InvalidDataError("Excess CBOR data")
        return value
