""" Various utilities that don't fit into any particular module. """

import enum
import functools
import typing
from collections import defaultdict
from functools import reduce, wraps
from inspect import iscoroutinefunction, ismethod
from itertools import chain
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Type,
    Union,
    TypeVar,
    Generic,
    cast
)

import pydantic
from pydantic import ValidationError

from diffusion.datatypes import DataType
from diffusion.internal.encoded_data import EncodingType

if typing.TYPE_CHECKING:
    from pydantic.decorator import ConfigType, AnyCallableT


def coroutine(fn: Callable) -> Callable:
    """Decorator to convert a regular function to a coroutine function.

    Since asyncio.coroutine is set to be removed in 3.10, this allows
    awaiting a regular function. Not useful as a @-based decorator,
    but very helpful for inline conversions of unknown functions, and
    especially lambdas.
    """
    if iscoroutinecallable(fn):
        return fn

    @wraps(fn)
    async def _wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return _wrapper


def iscoroutinecallable(obj: Callable):
    """Return `True` if the object is a coroutine callable.

    Similar to `inspect.iscoroutinefunction`, except that it also accepts
    objects with coroutine `__call__` methods.
    """
    return iscoroutinefunction(obj) or (
        callable(obj)
        and ismethod(obj.__call__)  # type: ignore
        and iscoroutinefunction(obj.__call__)  # type: ignore
    )


T = TypeVar('T', bound=Type[Any])


def get_all_subclasses(cls: T) -> List[T]:
    """Returns a dict containing all the subclasses of the given class.

    Follows the inheritance tree recursively.
    """
    subclasses = list(cls.__subclasses__())
    if subclasses:
        subclasses.extend(chain.from_iterable(get_all_subclasses(c) for c in subclasses))
    return subclasses


def fnmap(functions: Iterable[Callable[[Any], Any]], *values: Any) -> Union[Any, Iterator[Any]]:
    """Applies a series of single-argument functions to each of the values.

    Returns a single value if one value was given, or an iterator if multiple.
    """
    results = map(lambda val: reduce(lambda v, fn: fn(v), functions, val), values)
    return next(results) if len(values) == 1 else results


def get_fnmap(*functions: Callable[[Any], Any]) -> Callable[..., Any]:
    """ Prepares a single-argument function to apply all the functions. """
    return lambda *values: fnmap(functions, *values)


class CollectionEnum(enum.EnumMeta):
    """Metaclass which allows lookup on enum values.

    The default implementation of `EnumMeta.__contains__` looks
    for instances of the Enum class, which is not very useful.
    With this, it is possible to check whether an Enum class
    contains a certain value.

    Usage:
        >>> class MyEnum(enum.Enum, metaclass=CollectionEnum):
        ...     FOO = "foo"
        ...     BAR = "bar"
        ...
        >>> "foo" in MyEnum
        True
        >>> "blah" in MyEnum
        False
        >>> MyEnum.BAR in MyEnum
        True
    """

    def __contains__(cls, item):
        return isinstance(item, cls) or item in [v.value for v in cls.__members__.values()]


def flatten_mapping(values: Iterable) -> Iterable:
    """Extract an iterable of values from an iterable of nested mappings.

    Usage:
        >>> values = ({"a": {"b": "c"}, "d": {"e": "f"}}, {"g": "h"})
        >>> tuple(flatten_mapping(values))
        ('c', 'f', 'h')
    """
    for item in values:
        if isinstance(item, Mapping):
            yield from flatten_mapping(item.values())
        else:
            yield item


def nested_dict():
    """Creates a recursive defaultdict of any depth.

    Usage:
        >>> d = nested_dict()
        >>> d["a"] = 1
        >>> d["b"]["c"] = 2
        >>> d == {"a": 1, "b": {"c": 2}}
        True
    """
    return defaultdict(nested_dict)


def assert_arg_type(obj, tp: type):
    if not isinstance(obj, tp):
        raise TypeError(f"Expected a {tp.__module__}:{tp.__qualname__} but got {obj} "
                        f"of type {type(obj)}")


Model_T = typing.TypeVar("Model_T", bound='Model')


class Model(pydantic.BaseModel):
    __field_names__: typing.Optional[List[str]] = None

    @classmethod
    def _field_names(cls):
        if cls.__field_names__ is None:
            cls.__field_names__ = list(cls.__fields__.keys())
        return cls.__field_names__

    class Config(object):
        error_msg_templates = {
            "type_error.none.not_allowed": "None is an invalid value",
            "value_error.any_str.min_length": "String must be at least of length {limit_value}",
            "type_error.bool": "Boolean required",
            "type_error.str": "Value is not a string"
        }
        arbitrary_types_allowed = True
        TC_ERROR = ValidationError

        @classmethod
        def from_tuple(cls,
                       modelcls: typing.Type['Model_T'],
                       tp: typing.Tuple[typing.Any, ...]) -> Model_T:
            fn = modelcls._field_names()
            args = {
                fn[i]: modelcls.Config.decode(value)
                for i, value in enumerate(tp[:len(fn)])
            }
            return modelcls(**args)

        @classmethod
        def decode(cls, item):
            if isinstance(item, (DataType, EncodingType)):
                item = item.value
            if isinstance(item, list):
                return [cls.decode(x) for x in item]
            if isinstance(item, dict):
                return {k: cls.decode(v) for k, v in item.items()}
            return item

        @classmethod
        def as_tuple(cls, item: 'Model') -> typing.Tuple[typing.Any, ...]:
            return tuple(item.dict(by_alias=True).get(key) for key in item._field_names())

    @classmethod
    def from_tuple(cls: typing.Type['Model'], tp: typing.Tuple[typing.Any, ...]):
        result = cls.Config.from_tuple(cls, tp)
        return result


def validate_member_arguments(
    func: "AnyCallableT", config: "ConfigType" = Model.Config, **fwd_refs
) -> "AnyCallableT":
    """
    Decorator to validate member function arguments.
    Automatically updates forward refs for class members
    that reference the type of 'self' e.g. Builders...

    Args:
        func: the original function
        **fwd_refs: any additional forward refs

    Returns:
        The decorated function with argument validation
    """

    validator = pydantic.validate_arguments(config=config)
    result = validator(func)
    result.model.update_forward_refs(**fwd_refs)  # type: ignore

    def first_time(self, *args, **kwargs):
        nonlocal wrapped
        result.model.update_forward_refs(**{type(self).__name__: type(self)})
        wrapped = result
        return result(self, *args, **kwargs)

    wrapped = first_time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)

    return cast('AnyCallableT', wrapper)


ModelImpl = TypeVar('ModelImpl', bound=Model)


class BuilderBase(Generic[ModelImpl]):
    tp: Type[ModelImpl]
    _target: ModelImpl

    # noinspection PyTypeChecker
    @classmethod
    @functools.lru_cache(maxsize=None)
    def __class_getitem__(cls, tp: Type[ModelImpl]) -> "BuilderBase[ModelImpl]":
        dct = {"tp": tp, **cls.__dict__}
        return cast(
            "BuilderBase[ModelImpl]",
            type(f"{tp.__name__}BuilderBase", cls.__bases__, dct)
        )

    def __init__(self, *args, **kwargs):
        """
        Generic builder.

        Builds an object of type `ModelImpl`.

        Args:
            *args: positional arguments to pass into `ModelImpl`
                constructor on initialisation/reset
            **kwargs: keyword arguments to pass into `ModeLimpl`
                constructor on initialisation/reset
        """
        self._args = args
        self._kwargs = kwargs
        self.reset()

    V = TypeVar('V', bound="BuilderBase")

    def reset(self: V) -> V:
        """
        Reset the builder.

        Returns:
            this builder
        """
        self._target = self.tp(*self._args, **self._kwargs)
        return self

    def _create(self: V, **kwargs) -> ModelImpl:
        """
        Create a new `ModelImpl` using the values
        currently know to this builder.

        Args:
            **kwargs: overriden arguments

        Returns:
            a new `ModelImpl` with all of the current settings of
            the builder, overriden as specified
        """
        dct = self._target.dict()
        dct.update(**kwargs)
        return self.tp(**dct)
