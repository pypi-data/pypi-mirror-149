#  Copyright (c) 2021 Push Technology Ltd., All Rights Reserved.
#
#  Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from io import BytesIO
from typing import Any

import cbor2
import diffusion_core.cbor as diffusion_cbor
from typing_extensions import Protocol


class Encoder(Protocol):
    @staticmethod
    def load(buf: BytesIO) -> Any:
        pass

    @staticmethod
    def loads(buf: bytes) -> Any:
        pass

    @staticmethod
    def dumps(value: Any, *args: Any, **kwargs: Any) -> bytes:
        pass


class CBOR2(Encoder):
    @staticmethod
    def load(buf: BytesIO) -> Any:
        from diffusion.datatypes import InvalidDataError
        try:
            return cbor2.load(buf)
        except cbor2.CBORDecodeError as ex:
            raise InvalidDataError("Invalid CBOR data") from ex

    loads = cbor2.loads
    dumps = cbor2.dumps


class DiffCbor(CBOR2):
    dumps = diffusion_cbor.dumps


DefaultEncoder = DiffCbor
