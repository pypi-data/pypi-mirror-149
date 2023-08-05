#  Copyright (c) 2022 Push Technology Ltd., All Rights Reserved.
#
#  Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.
import typing

import stringcase  # type: ignore

from diffusion.internal.serialisers import Serialiser
from diffusion.internal.services import ServiceValue
from diffusion.internal.utils import Model, Model_T


class Marshaller(object):
    _serialiser: Serialiser

    def __init__(self, serialiser_name: str):
        self._serialiser = Serialiser.by_name(serialiser_name)

    def as_service_value(self, item: Model) -> ServiceValue:
        sv = ServiceValue(self._serialiser)
        sv.set(**item.dict(by_alias=True))
        return sv

    def as_tuple(self, item: Model_T) -> typing.Tuple[typing.Any, ...]:
        return tuple(self.as_service_value(item).values())

    def from_tuple(self, modelcls: typing.Type[Model], tp: typing.Tuple[typing.Any, ...]):
        sv = ServiceValue(self._serialiser)
        sv.set(*tp)
        result = sv.deserialise_model(modelcls)
        return result


class MarshalledModel(Model):
    class Config(Model.Config):
        """
        Adds Serialiser support to Model.Config
        'alias' defines the name of the serialiser to map to
        """
        alias: typing.ClassVar[str]
        allow_population_by_field_name = True
        alias_generator = stringcase.spinalcase
        _marshaller: typing.Optional[Marshaller] = None

        @classmethod
        def marshaller(cls) -> Marshaller:
            if not cls._marshaller:
                cls._marshaller = Marshaller(cls.alias)
            return cls._marshaller

        @classmethod
        def as_tuple(cls, item: Model_T) -> typing.Tuple[typing.Any, ...]:
            return cls.marshaller().as_tuple(item)

        @classmethod
        def from_tuple(cls, modelcls: typing.Type[Model], tp: typing.Tuple[typing.Any, ...]):
            return cls.marshaller().from_tuple(modelcls, tp)
