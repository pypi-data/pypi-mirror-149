"""Base module for various event handlers."""
import typing

import asyncio
import structlog
from typing_extensions import Protocol, runtime_checkable, TypedDict

from diffusion.internal import exceptions
from diffusion.internal.utils import coroutine

LOG = structlog.get_logger()


@runtime_checkable
class Handler(Protocol):
    """Protocol for event handlers implementation."""

    async def handle(self, event: str, **kwargs) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            kwargs: Additional arguments.
        """
        ...  # pragma: no cover


HandlersMapping = typing.MutableMapping[typing.Hashable, Handler]


class UnknownHandlerError(exceptions.DiffusionError):
    """ Raised when a requested handler key has not been registered in the session. """


@runtime_checkable
class SubHandlerProtocol(Protocol):
    def __init__(self):
        pass

    async def __call__(
        self,
        *,
        old_value: typing.Any,
        topic_path: str,
        topic_value: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Any:
        pass


# fallback for tooling that doesn't support Callable Protocols
SubHandler = typing.Union[
    SubHandlerProtocol, typing.Callable, typing.Callable[[typing.Any], typing.Any]
]


class SimpleHandler(Handler):
    """ Wraps a callable into a Handler protocol instance. """

    def __init__(self, callback: SubHandler):
        self._callback = coroutine(callback)

    async def handle(self, event: str = "", **kwargs):
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            kwargs: Additional arguments.
        """
        return await self._callback(**kwargs)


class HandlerSet(set, Handler):
    """ A collection of handlers to be invoked together. """

    async def handle(self, event: str = "", **kwargs) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            kwargs: Additional arguments.

        Returns:
            Aggregated list of returned values.
        """
        return await asyncio.gather(*[handler(**kwargs) for handler in self])


class SubHandlerDict(TypedDict, total=False):
    subscribe: SubHandler


class OptionalDict(SubHandlerDict, total=False):
    pass


class ErrorHandler(Protocol):
    async def __call__(self, code: int, description: str) -> None:
        pass


SubHandlerDictType = typing.TypeVar('SubHandlerDictType', bound=SubHandlerDict)


class EventStreamHandler(Handler):
    """Generic handler of event streams.

    Each keyword argument is a callable which will be converted to coroutine
    and awaited to handle the event matching the argument keyword.
    """
    _handlers: SubHandlerDict

    def __init__(self, *, on_error: ErrorHandler = None, **kwargs: typing.Optional[SubHandler]):
        all_args = typing.cast(typing.Dict[str, typing.Any], kwargs)
        all_args.update(on_error=on_error)
        self._handlers: SubHandlerDict = typing.cast(
            SubHandlerDict,
            {event: coroutine(callback) for event, callback in all_args.items() if callback},
        )

    async def handle(self, event: str, **kwargs):
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            kwargs: Additional arguments.
        """
        try:
            handler = (typing.cast(typing.Mapping[str, typing.Callable], self._handlers))[event]
        except KeyError:
            LOG.debug("No handler registered for event.", stream_event=event, **kwargs)
        else:
            return await handler(**kwargs)
