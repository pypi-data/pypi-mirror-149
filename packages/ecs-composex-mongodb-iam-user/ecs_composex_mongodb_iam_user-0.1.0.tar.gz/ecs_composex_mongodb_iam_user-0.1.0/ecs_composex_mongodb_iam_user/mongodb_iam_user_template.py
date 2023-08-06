"""Main module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mongodb_iam_user import MongodbIamUser
    from troposphere import Template
    from ecs_composex.common.settings import ComposeXSettings
    from ecs_composex.common.stacks import ComposeXStack

from copy import deepcopy

from compose_x_common.compose_x_common import keyisset, set_else_none
from ecs_composex.common import add_parameters, add_resource
from ecs_composex.ecs.task_iam.task_role import IAM_ROLE_ARN
from ecs_composex.resources_import import import_record_properties
from troposphere import Ref

from .mongodb_atlas_awsiamdatabaseuser import MongoDbAwsIamDatabaseUser


def handle_api_key_str(api_key: str) -> str:
    """
    Placeholder if one finds something smart to do with this.
    :param api_key:
    """
    return api_key


def handle_api_key_dict(api_key: dict) -> str:
    """
    :param dict api_key:
    """
    secret_id = set_else_none(
        "SecretArn", api_key, set_else_none("SecretName", api_key)
    )
    if not secret_id:
        raise "A value must set for SecretName or SecretArn."
    json_key = set_else_none("JsonKey", api_key)

    secret_resolve = "{{resolve:secretsmanager:" + secret_id
    if json_key:
        secret_resolve = f"{secret_resolve}" + f":SecretString:{json_key}" + r"}}"
    else:
        secret_resolve = secret_resolve + r"}}"
    return secret_resolve


def import_from_parameters(new_db_user: MongodbIamUser, props: dict) -> None:
    """
    Finds parameters set in there to update the resource props

    :param new_db_user:
    :param props:
    """
    public_key = set_else_none("PublicKey", new_db_user.parameters)
    private_key = set_else_none("PrivateKey", new_db_user.parameters)

    if not keyisset("ApiKeys", props):
        props.update({"ApiKeys": {}})

    if not private_key or not public_key:
        raise KeyError(
            "You did not set Properties.ApiKeys nor set "
            "MacroParameters.PublicKey and MacroParameters.PrivateKey"
        )
    if isinstance(public_key, str):
        secret_resolve = handle_api_key_str(public_key)
        props["ApiKeys"]["PublicKey"] = secret_resolve

    elif isinstance(public_key, dict):
        secret_resolve = handle_api_key_dict(public_key)
        props["ApiKeys"]["PublicKey"] = secret_resolve

    if isinstance(private_key, str):
        secret_resolve = handle_api_key_str(private_key)
        props["ApiKeys"]["PrivateKey"] = secret_resolve

    elif isinstance(private_key, dict):
        secret_resolve = handle_api_key_dict(private_key)
        props["ApiKeys"]["PrivateKey"] = secret_resolve


def iterate_over_db_role_services(
    props: dict,
    service_name: str,
    new_db_user: MongodbIamUser,
    stack: ComposeXStack,
    template: Template,
    settings: ComposeXSettings,
) -> None:
    """
    For each service associated with this MongoDB User "role", create a dedicated resource for each service Task Role
    :param props:
    :param service_name:
    :param new_db_user:
    :param stack:
    :param template:
    :param settings:
    :return:
    """
    service_resource_props = deepcopy(props)
    if service_name in settings.families:
        family = settings.families[service_name]
        title = f"{family.logical_name}{new_db_user.logical_name}"
        role_arn_id = family.iam_manager.task_role.attributes_outputs[IAM_ROLE_ARN]
    else:
        raise KeyError(
            new_db_user.module.res_key,
            new_db_user.name,
            f"Service {service_name} is not defined in families",
            settings.families,
        )
    service_resource_props["AwsIamResource"] = Ref(role_arn_id["ImportParameter"])
    add_parameters(template, [role_arn_id["ImportParameter"]])
    cfn_props = import_record_properties(
        service_resource_props,
        MongoDbAwsIamDatabaseUser,
        ignore_missing_required=True,
    )
    stack.Parameters.update(
        {role_arn_id["ImportParameter"].title: role_arn_id["ImportValue"]}
    )
    new_db_user.cfn_resource = MongoDbAwsIamDatabaseUser(title, **cfn_props)
    add_resource(template, new_db_user.cfn_resource)


def process_new_resources(
    new_resources: list[MongodbIamUser],
    stack: ComposeXStack,
    template: Template,
    settings: ComposeXSettings,
) -> None:
    """
    For each new mongoDB IAM "user" / role, associate with service roles and add resource

    :param list[MongodbIamUser] new_resources:
    :param ComposeXStack stack:
    :param Template template:
    :param ComposeXSettings settings:
    """
    for new_db_user in new_resources:
        props = {}
        if not new_db_user.parameters and not keyisset(
            "ApiKeys", new_db_user.properties
        ):
            raise KeyError(
                f"{new_db_user.module.res_key}.{new_db_user.name} - You must specify ApiKeys"
            )
        elif new_db_user.parameters and not keyisset("ApiKeys", new_db_user.properties):
            import_from_parameters(new_db_user, props)
            props.update(new_db_user.properties)
        for service_name in new_db_user.services:
            iterate_over_db_role_services(
                props, service_name, new_db_user, stack, template, settings
            )
