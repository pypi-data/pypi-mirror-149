""" Serialisers for values consisting of multiple individual values. """

from __future__ import annotations

import io
from typing import cast, Collection, Dict, Generic, Iterable, Sequence, Type, TypeVar, Union

from stringcase import pascalcase

from diffusion.internal.encoded_data import EncodingProtocol, EncodingType, Int32
from diffusion.internal.encoded_data.exceptions import DataValidationError, StreamExhausted
from .spec import SERIALISER_SPECS
from ..encoded_data.abstract import EncodingTypeVar, Enc_K, Enc_V

T = TypeVar("T", bound=EncodingType)


class GenericScalarSetSerialiser(EncodingProtocol, Generic[T]):
    """Generic set for multiple scalar values.

    Not technically a set, more of a collection.
    """

    scalar_type: Type[T]

    def __init__(self, values: Collection[T]):
        self.values: Sequence[EncodingType] = [
            value if isinstance(value, EncodingType) else self.scalar_type(value)
            for value in values
        ]
        self.validate()

    @property
    def value(self):
        """ All the values; needed for compatibility with `EncodingType`. """
        return self.values

    @classmethod
    def read(cls, stream: io.BytesIO) -> GenericScalarSetSerialiser:
        """ Read the values from a stream. """
        result = []
        length = Int32.read(stream).value
        if length:
            while True:
                try:
                    result.append(cls.scalar_type.read(stream))
                except StreamExhausted:
                    break
        return cls(result)

    def to_bytes(self) -> bytes:
        """ Convert the values to bytes. """
        return Int32(len(self.values)).to_bytes() + b"".join(
            value.to_bytes() for value in self.values
        )

    def write(self, stream: io.BytesIO) -> io.BytesIO:
        """ Write the bytes representation of a value into a binary stream. """
        stream.write(self.to_bytes())
        return stream

    def validate(self) -> None:
        """Validate all values.

        Raises:
            DataValidationError: If the value is not a collection of `scalar_type` objects.
        """
        for value in self.values:
            if not isinstance(value, self.scalar_type):
                raise DataValidationError(
                    f"{type(self)} requires a collection of {self.scalar_type.__name__} objects"
                )
            value.validate()  # type: ignore

    def __repr__(self):
        return f"<{type(self).__name__} length={len(self.values)}>"


class SetSerialiser(type):
    """ Metaclass for set serialisers. """


class ScalarSetSerialiser(Generic[EncodingTypeVar], SetSerialiser):
    """ Serialiser for a set of scalar values. """

    _serialisers: Dict[str, ScalarSetSerialiser] = {}

    def __new__(
        mcs, serialiser: Type[EncodingTypeVar]
    ) -> ScalarSetSerialiser[EncodingTypeVar]:
        """Class constructor."""
        name = pascalcase(f"{serialiser.__name__}SetSerialiser")
        if name not in mcs._serialisers:
            mcs._serialisers[name] = cast(
                ScalarSetSerialiser,
                type(name, (GenericScalarSetSerialiser,), {"scalar_type": serialiser}),
            )
        return cast(ScalarSetSerialiser[EncodingTypeVar], mcs._serialisers[name])


class GenericMapSerialiser(Dict[Enc_K, Enc_V], EncodingProtocol):
    """ Serialiser for a mapping value. """

    key_type: Type[EncodingType]
    value_type: Type[EncodingType]

    def __init__(self, values: Union[dict, Iterable[tuple]]):
        cast_values = {}
        if isinstance(values, dict):
            values = values.items()
        for key, value in values:
            if not isinstance(key, EncodingType):
                key = self.key_type(key)
            if not isinstance(value, EncodingType):
                value = self.value_type(value)
            cast_values[key] = value
        super().__init__(cast_values)
        self.validate()

    @classmethod
    def read(cls, stream: io.BytesIO) -> GenericMapSerialiser:
        """ Read the values from a stream. """
        result = {}
        length = Int32.read(stream).value
        if length:
            for _ in range(length):
                try:
                    key = cls.key_type.read(stream)
                    value = cls.value_type.read(stream)
                except StreamExhausted:
                    break
                else:
                    result[key] = value
        return cls(result)

    def to_bytes(self) -> bytes:
        """ Convert the values to bytes. """
        return Int32(len(self)).to_bytes() + b"".join(
            key.to_bytes() + value.to_bytes() for key, value in self.items()
        )

    def write(self, stream: io.BytesIO) -> io.BytesIO:
        """ Write the bytes representation of a value into a binary stream. """
        stream.write(self.to_bytes())
        return stream

    def validate(self) -> None:
        """ Validate all values. """
        for key, value in self.items():
            if not isinstance(key, self.key_type):
                raise DataValidationError(
                    f"Key {key}: expected {self.key_type}, got {type(key)}."
                )
            key.validate()
            if not isinstance(value, self.value_type):
                raise DataValidationError(
                    f"Value {key}: expected {self.value_type}, got {type(value)}."
                )
            value.validate()

    @property
    def value(self):
        """ All the values; needed for compatibility with `EncodingType`. """
        return self

    def __repr__(self):
        return f"<{type(self).__name__} length={len(self)}>"


class MapSerialiser(Generic[Enc_K, Enc_V]):
    """ Metaclass for mapping serialisers. """

    _serialisers: Dict[str, MapSerialiser] = {}

    def __new__(
        mcs,
        key_serialiser: Union[str, Type[Enc_K]],
        value_serialiser: Union[str, Type[Enc_V]],
    ) -> MapSerialiser[Enc_K, Enc_V]:
        """ Class constructor. """
        ks_resolved: Type[Enc_K]
        vs_resolved: Type[Enc_V]
        if isinstance(key_serialiser, str):
            ks_resolved = cast(Type[Enc_K], SERIALISER_SPECS[key_serialiser])
        else:
            ks_resolved = key_serialiser
        if isinstance(value_serialiser, str):
            vs_resolved = cast(Type[Enc_V], SERIALISER_SPECS[value_serialiser])
        else:
            vs_resolved = value_serialiser
        name = pascalcase(
            f"{ks_resolved.__name__}{vs_resolved.__name__}MapSerialiser"  # type: ignore
        )
        if name not in mcs._serialisers:
            mcs._serialisers[name] = cast(
                MapSerialiser,
                type(
                    name,
                    (GenericMapSerialiser,),
                    {"key_type": ks_resolved, "value_type": vs_resolved},
                ),
            )
        return cast(MapSerialiser[Enc_K, Enc_V], mcs._serialisers[name])
