"""Stream handlers for topics."""
from typing import Callable, Type

import structlog

from diffusion.datatypes import DataType
from diffusion.handlers import EventStreamHandler, SubHandler

LOG = structlog.get_logger()


class ValueStreamHandler(EventStreamHandler):
    """Stream handler implementation for the value streams of the given type."""

    def __init__(
        self,
        data_type: Type[DataType],
        *,
        subscribe: SubHandler = None,
        update: SubHandler = None,
        **kwargs: Callable,
    ):
        self.type = data_type
        super().__init__(
            subscribe=subscribe,
            update=update,
            **kwargs
        )
