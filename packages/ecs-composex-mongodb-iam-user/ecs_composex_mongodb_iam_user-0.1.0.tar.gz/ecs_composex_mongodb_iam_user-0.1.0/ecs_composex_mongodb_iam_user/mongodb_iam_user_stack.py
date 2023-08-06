"""Main module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecs_composex.common.settings import ComposeXSettings
    from ecs_composex.mods_manager import XResourceModule

from ecs_composex.common import LOG, build_template
from ecs_composex.common.stacks import ComposeXStack
from ecs_composex.compose.x_resources.helpers import (
    set_lookup_resources,
    set_new_resources,
    set_resources,
)

from ecs_composex_mongodb_iam_user.mongodb_iam_user import MongodbIamUser
from ecs_composex_mongodb_iam_user.mongodb_iam_user_template import (
    process_new_resources,
)


class XStack(ComposeXStack):
    """
    Class to manage the stack for mongodb_iam_user
    """

    def __init__(
        self, title, settings: ComposeXSettings, module: XResourceModule, **kwargs
    ):
        set_resources(settings, MongodbIamUser, module)
        x_resources = settings.compose_content[module.res_key].values()
        lookup_resources = set_lookup_resources(x_resources)
        if lookup_resources:
            LOG.error(f"{module.res_key} - Lookup is not supported.")
        new_resources = set_new_resources(x_resources)
        if new_resources:
            stack_template = build_template(
                f"{module.res_key} - root stack",
            )
            super().__init__(title, stack_template, **kwargs)
            process_new_resources(new_resources, self, stack_template, settings)
        else:
            self.is_void = True
        for resource in x_resources:
            resource.stack = self
