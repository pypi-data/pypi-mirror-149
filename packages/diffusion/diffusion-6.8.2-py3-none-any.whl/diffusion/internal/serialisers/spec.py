""" Specifications for serialisers, based on `spec.clj`. """

from __future__ import annotations

import typing
from enum import Enum
from typing import Iterator, Mapping, MutableMapping, Optional, Sequence, Type, Union

import copy
import structlog

from diffusion.internal.encoded_data import Byte, Bytes, EncodingProtocol, Int32, Int64, String
import diffusion.internal.encoded_data as encoded_data

LOG = structlog.get_logger()

EncodingClass = Type[EncodingProtocol]
SerialiserChain = Sequence[Optional[EncodingClass]]
SerialiserMapValue = Union[EncodingClass, SerialiserChain]
SerialiserMap = MutableMapping[str, SerialiserMapValue]
SerialiserOutput = Iterator[Optional[Type[EncodingProtocol]]]

NULL_VALUE_KEY = "void"
ENCODING_TYPE_KEYS = {
    NULL_VALUE_KEY: [],
    "BYTE": Byte,
    "BYTES": Bytes,
    "FIXED_BYTES": Bytes,
    "INT32": Int32,
    "INT64": Int64,
    "STRING": String,
}


class CompoundSpec(typing.NamedTuple):
    type: Compound
    args: typing.Tuple[typing.Any]

    def __repr__(self):
        return f"{self.type}({','.join(map(repr, self.args))})"


class Compound(Enum):
    """Types of compound types."""

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return name

    ONE_OF = "one-of"
    N_OF = "n-of"
    SET_OF = "set-of"
    SORTED_SET = "sorted-set"
    MAP_OF = "map-of"

    def __call__(self, *args):
        """Return an instance of the corresponding spec."""
        return CompoundSpec(type=self, args=args)

    def __repr__(self, *args):
        return f"Compound.{self._name_}"


SpecItem = Union[str, CompoundSpec]
SerialiserSpecItem = Optional[Union[EncodingClass, Sequence[SpecItem], SerialiserChain]]

orig_specs = {
    "add-and-set-topic-request": (
        "topic-path",
        "protocol14-topic-specification",
        "bytes",
        "update-constraint",
    ),
    "add-topic-result": encoded_data.Byte,
    "authenticator-registration-parameters": ("service-id", "control-group", "handler-name"),
    "binary-value-constraint": encoded_data.Bytes,
    "boolean": encoded_data.Byte,
    "branch-mapping": ("session-filter", "path"),
    "branch-mapping-table": ("path", Compound.N_OF("branch-mapping")),
    "byte": encoded_data.Byte,
    "bytes": encoded_data.Bytes,
    "change-principal-request": ("principal", "credentials"),
    "conjunction-constraint": Compound.N_OF(
        Compound.ONE_OF(
            {
                0: ("unconstrained-constraint",),
                2: ("binary-value-constraint",),
                3: ("no-value-constraint",),
                4: ("locked-constraint",),
                5: ("no-topic-constraint",),
            }
        )
    ),
    "control-group": encoded_data.String,
    "conversation-id": encoded_data.Int64,
    "count-or-parser-errors2": Compound.ONE_OF(
        {0: (encoded_data.Int32,), 1: ("error-report",)}
    ),
    "create-topic-view-result": Compound.ONE_OF(
        {
            0: ("topic-view",),
            1: ("error-report",),
            2: ("error-report", "error-report"),
            3: ("error-report", "error-report", "error-report"),
            4: ("error-report", "error-report", "error-report", "error-report"),
        }
    ),
    "credentials": (encoded_data.Byte, encoded_data.Bytes),
    "data-type-name": encoded_data.String,
    "error-reason": (encoded_data.Int32, encoded_data.String),
    "error-report": (encoded_data.String, encoded_data.Int32, encoded_data.Int32),
    "error-report-list": Compound.N_OF("error-report"),
    "exports-to-prometheus": "boolean",
    "filter-response": (
        "conversation-id",
        "session-id",
        Compound.ONE_OF({0: ("messaging-response",), 1: ("error-reason",)}),
    ),
    "groups-by-topic-type": "boolean",
    "handler-name": encoded_data.String,
    "integer": encoded_data.Int32,
    "json-pointer": encoded_data.String,
    "locked-constraint": ("session-lock-name", "session-lock-sequence"),
    "maximum-groups": encoded_data.Int32,
    "message-path": encoded_data.String,
    "message-receiver-control-registration-parameters": (
        "service-id",
        "control-group",
        "topic-path",
        "session-property-keys",
    ),
    "message-receiver-control-registration-request": (
        "message-receiver-control-registration-parameters",
        "conversation-id",
    ),
    "messaging-client-filter-send-request": (
        "conversation-id",
        "session-filter",
        "message-path",
        "serialised-value",
    ),
    "messaging-client-forward-send-request": (
        "conversation-id",
        "session-id",
        "message-path",
        "session-properties",
        "serialised-value",
    ),
    "messaging-client-send-request": ("session-id", "message-path", "serialised-value"),
    "messaging-response": ("serialised-value",),
    "messaging-send-request": ("message-path", "serialised-value"),
    "metric-collector-name": encoded_data.String,
    "no-topic-constraint": (),
    "no-value-constraint": (),
    "partial-json-constraint": (Compound.MAP_OF("json-pointer", encoded_data.Bytes),),
    "path": encoded_data.String,
    "ping-request": (),
    "ping-response": (),
    "principal": encoded_data.String,
    "protocol14-topic-add-request": ("topic-path", "protocol14-topic-specification"),
    "protocol14-topic-specification": ("protocol14-topic-type", "topic-properties"),
    "protocol14-topic-specification-info": (
        "topic-id",
        "topic-path",
        "protocol14-topic-specification",
    ),
    "protocol14-topic-type": encoded_data.Byte,
    "protocol14-unsubscription-notification": ("topic-id", "byte"),
    "protocol18-log-entries-fetch-response": (
        encoded_data.Int64,
        encoded_data.Int64,
        encoded_data.Int64,
        encoded_data.Int64,
        encoded_data.String,
        encoded_data.Int64,
    ),
    "protocol22-unsubscription-notification": ("topic-id", encoded_data.Byte),
    "removes-metrics-with-no-matches": "boolean",
    "remove-topics-request": "topic-selector",
    "role-set": Compound.SET_OF(encoded_data.String),
    "serialised-value": ("data-type-name", "bytes"),
    "service-id": encoded_data.Int32,
    "session-filter": encoded_data.String,
    "session-id": (encoded_data.Int64, encoded_data.Int64),
    "session-lock-name": encoded_data.String,
    "session-lock-sequence": encoded_data.Int64,
    "session-metric-collector": (
        "metric-collector-name",
        "exports-to-prometheus",
        "maximum-groups",
        "removes-metrics-with-no-matches",
        "session-filter",
        "session-property-keys",
    ),
    "session-metric-collectors": Compound.N_OF("session-metric-collector"),
    "session-properties": Compound.SET_OF(encoded_data.String),
    "session-property-keys": Compound.SET_OF(encoded_data.String),
    "session-tree-branch-list": Compound.N_OF("path"),
    "set-topic-request": (
        "topic-path",
        "protocol14-topic-type",
        "bytes",
        "update-constraint",
    ),
    "string": encoded_data.String,
    "topic-id": encoded_data.Int32,
    "topic-path": encoded_data.String,
    "group-by-path-prefix-parts": encoded_data.Int32,
    "topic-metric-collector": (
        "metric-collector-name",
        "exports-to-prometheus",
        "maximum-groups",
        "topic-selector",
        "groups-by-topic-type",
        "group-by-path-prefix-parts"
    ),
    "topic-metric-collectors": Compound.N_OF("topic-metric-collector"),
    "topic-properties": Compound.MAP_OF("topic-property-key", encoded_data.String),
    "topic-property-key": encoded_data.String,
    "topic-selector": encoded_data.String,
    "topic-view": ("topic-view-name", "topic-view-specification", "role-set"),
    "topic-view-name": encoded_data.String,
    "topic-view-specification": encoded_data.String,
    "unconstrained-constraint": (),
    "update-constraint": Compound.ONE_OF(
        {
            0: ("unconstrained-constraint",),
            1: ("conjunction-constraint",),
            2: ("binary-value-constraint",),
            3: ("no-value-constraint",),
            4: ("locked-constraint",),
            5: ("no-topic-constraint",),
            6: ("partial-json-constraint",),
        }
    ),
    "void": None,
}


class DynamicSpecs(object):
    @property
    def specs(self) -> Mapping[str, SerialiserSpecItem]:
        try:
            from ..generated.specs import specs
        except ImportError:
            specs = copy.deepcopy(orig_specs)
        return specs


SERIALISER_SPECS = DynamicSpecs().specs
