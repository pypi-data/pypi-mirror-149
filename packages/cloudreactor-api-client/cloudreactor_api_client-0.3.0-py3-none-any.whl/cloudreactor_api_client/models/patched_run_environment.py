import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.aws_ecs_run_environment_execution_method_capability import AwsEcsRunEnvironmentExecutionMethodCapability
from ..models.group import Group
from ..models.name_and_uuid import NameAndUuid
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRunEnvironment")


@attr.s(auto_attribs=True)
class PatchedRunEnvironment:
    """RunEnvironments contain common settings for running a set of
    related Tasks. Usually RunEnvironments group Tasks in the same
    deployment environment (e.g. staging or production).
    Task and Workflows belong to a RunEnvironment but can override
    the RunEnvironment's settings.

        Attributes:
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
            created_by_group (Union[Unset, Group]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
            aws_account_id (Union[Unset, str]):
            aws_default_region (Union[Unset, str]):
            aws_access_key (Union[Unset, str]):
            aws_assumed_role_external_id (Union[Unset, str]):
            aws_events_role_arn (Union[Unset, str]):
            aws_workflow_starter_lambda_arn (Union[Unset, str]):
            aws_workflow_starter_access_key (Union[Unset, str]):
            default_alert_methods (Union[Unset, List[NameAndUuid]]):
            execution_method_capabilities (Union[Unset, List[AwsEcsRunEnvironmentExecutionMethodCapability]]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    aws_account_id: Union[Unset, str] = UNSET
    aws_default_region: Union[Unset, str] = UNSET
    aws_access_key: Union[Unset, str] = UNSET
    aws_assumed_role_external_id: Union[Unset, str] = UNSET
    aws_events_role_arn: Union[Unset, str] = UNSET
    aws_workflow_starter_lambda_arn: Union[Unset, str] = UNSET
    aws_workflow_starter_access_key: Union[Unset, str] = UNSET
    default_alert_methods: Union[Unset, List[NameAndUuid]] = UNSET
    execution_method_capabilities: Union[Unset, List[AwsEcsRunEnvironmentExecutionMethodCapability]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        uuid = self.uuid
        name = self.name
        description = self.description
        dashboard_url = self.dashboard_url
        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        aws_account_id = self.aws_account_id
        aws_default_region = self.aws_default_region
        aws_access_key = self.aws_access_key
        aws_assumed_role_external_id = self.aws_assumed_role_external_id
        aws_events_role_arn = self.aws_events_role_arn
        aws_workflow_starter_lambda_arn = self.aws_workflow_starter_lambda_arn
        aws_workflow_starter_access_key = self.aws_workflow_starter_access_key
        default_alert_methods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.default_alert_methods, Unset):
            default_alert_methods = []
            for default_alert_methods_item_data in self.default_alert_methods:
                default_alert_methods_item = default_alert_methods_item_data.to_dict()

                default_alert_methods.append(default_alert_methods_item)

        execution_method_capabilities: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.execution_method_capabilities, Unset):
            execution_method_capabilities = []
            for execution_method_capabilities_item_data in self.execution_method_capabilities:
                execution_method_capabilities_item = execution_method_capabilities_item_data.to_dict()

                execution_method_capabilities.append(execution_method_capabilities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if aws_account_id is not UNSET:
            field_dict["aws_account_id"] = aws_account_id
        if aws_default_region is not UNSET:
            field_dict["aws_default_region"] = aws_default_region
        if aws_access_key is not UNSET:
            field_dict["aws_access_key"] = aws_access_key
        if aws_assumed_role_external_id is not UNSET:
            field_dict["aws_assumed_role_external_id"] = aws_assumed_role_external_id
        if aws_events_role_arn is not UNSET:
            field_dict["aws_events_role_arn"] = aws_events_role_arn
        if aws_workflow_starter_lambda_arn is not UNSET:
            field_dict["aws_workflow_starter_lambda_arn"] = aws_workflow_starter_lambda_arn
        if aws_workflow_starter_access_key is not UNSET:
            field_dict["aws_workflow_starter_access_key"] = aws_workflow_starter_access_key
        if default_alert_methods is not UNSET:
            field_dict["default_alert_methods"] = default_alert_methods
        if execution_method_capabilities is not UNSET:
            field_dict["execution_method_capabilities"] = execution_method_capabilities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        created_by_user = d.pop("created_by_user", UNSET)

        _created_by_group = d.pop("created_by_group", UNSET)
        created_by_group: Union[Unset, Group]
        if isinstance(_created_by_group, Unset):
            created_by_group = UNSET
        else:
            created_by_group = Group.from_dict(_created_by_group)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        aws_account_id = d.pop("aws_account_id", UNSET)

        aws_default_region = d.pop("aws_default_region", UNSET)

        aws_access_key = d.pop("aws_access_key", UNSET)

        aws_assumed_role_external_id = d.pop("aws_assumed_role_external_id", UNSET)

        aws_events_role_arn = d.pop("aws_events_role_arn", UNSET)

        aws_workflow_starter_lambda_arn = d.pop("aws_workflow_starter_lambda_arn", UNSET)

        aws_workflow_starter_access_key = d.pop("aws_workflow_starter_access_key", UNSET)

        default_alert_methods = []
        _default_alert_methods = d.pop("default_alert_methods", UNSET)
        for default_alert_methods_item_data in _default_alert_methods or []:
            default_alert_methods_item = NameAndUuid.from_dict(default_alert_methods_item_data)

            default_alert_methods.append(default_alert_methods_item)

        execution_method_capabilities = []
        _execution_method_capabilities = d.pop("execution_method_capabilities", UNSET)
        for execution_method_capabilities_item_data in _execution_method_capabilities or []:
            execution_method_capabilities_item = AwsEcsRunEnvironmentExecutionMethodCapability.from_dict(
                execution_method_capabilities_item_data
            )

            execution_method_capabilities.append(execution_method_capabilities_item)

        patched_run_environment = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            dashboard_url=dashboard_url,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            created_at=created_at,
            updated_at=updated_at,
            aws_account_id=aws_account_id,
            aws_default_region=aws_default_region,
            aws_access_key=aws_access_key,
            aws_assumed_role_external_id=aws_assumed_role_external_id,
            aws_events_role_arn=aws_events_role_arn,
            aws_workflow_starter_lambda_arn=aws_workflow_starter_lambda_arn,
            aws_workflow_starter_access_key=aws_workflow_starter_access_key,
            default_alert_methods=default_alert_methods,
            execution_method_capabilities=execution_method_capabilities,
        )

        patched_run_environment.additional_properties = d
        return patched_run_environment

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
