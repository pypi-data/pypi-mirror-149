"""Main module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.common.settings import ComposeXSettings
    from ecs_composex.mods_manager import XResourceModule

from ecs_composex.compose.x_resources.services_resources import ServicesXResource


class MongodbIamUser(ServicesXResource):
    """
    Class to represent the MongoDB AWS IAM User
    """

    def __init__(
        self, name, definition, module: XResourceModule, settings: ComposeXSettings
    ):

        super().__init__(
            name,
            definition,
            module,
            settings,
        )
        self.secret_arn = None
