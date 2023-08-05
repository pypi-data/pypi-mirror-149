""" Base features module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .services.locator import ServiceLocator
from .session import InternalSession

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.session import Session


class Component:
    """A base class for various Diffusion "components".

    Args:
        session: The active `Session` to operate on.
    """

    def __init__(self, session: Session):
        self.session: InternalSession = session._internal

    @property
    def services(self) -> ServiceLocator:
        """Alias for the internal session's service locator."""
        return self.session.services
