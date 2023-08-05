""" Diffusion services package. """
from __future__ import annotations

from typing import Type

from .abstract import Service, InboundService, OutboundService, ServiceValue
from .exceptions import ServiceError, UnknownServiceError
from .messaging import MessagingSend, MessagingReceiverControlRegistration
from .session import SystemPing, UserPing
from .topics import Subscribe


def get_by_id(service_id: int) -> Type[Service]:
    """ Retrieve a service class based on its ID number. """
    return Service.get_by_id(service_id)


def get_by_name(service_name: str) -> Type[Service]:
    """ Retrieve a service class based on its name. """
    return Service.get_by_name(service_name)
