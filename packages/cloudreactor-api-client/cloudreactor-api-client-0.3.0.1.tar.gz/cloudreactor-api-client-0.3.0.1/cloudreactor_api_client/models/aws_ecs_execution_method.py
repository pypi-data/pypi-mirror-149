from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..models.aws_ecs_execution_method_tags import AwsEcsExecutionMethodTags
from ..models.aws_ecs_launch_type import AwsEcsLaunchType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsEcsExecutionMethod")


@attr.s(auto_attribs=True)
class AwsEcsExecutionMethod:
    """AwsEcsExecutionMethods contain configuration for running Tasks in
    AWS ECS.

        Attributes:
            type (Union[Unset, str]):
            task_definition_arn (Union[Unset, str]):
            task_definition_infrastructure_website_url (Union[Unset, str]):
            allocated_cpu_units (Union[Unset, int]):
            allocated_memory_mb (Union[Unset, int]):
            tags (Optional[AwsEcsExecutionMethodTags]):
            subnets (Union[Unset, List[str]]):
            subnet_infrastructure_website_urls (Union[Unset, None, List[Optional[str]]]):
            security_groups (Union[Unset, List[str]]):
            security_group_infrastructure_website_urls (Union[Unset, None, List[Optional[str]]]):
            assign_public_ip (Union[Unset, bool]):
            task_arn (Union[Unset, str]):
            launch_type (Union[Unset, AwsEcsLaunchType]):  Default: AwsEcsLaunchType.FARGATE.
            cluster_arn (Union[Unset, str]):
            cluster_infrastructure_website_url (Union[Unset, str]):
            execution_role (Union[Unset, str]):
            execution_role_infrastructure_website_url (Union[Unset, str]):
            task_role (Union[Unset, str]):
            task_role_infrastructure_website_url (Union[Unset, str]):
            platform_version (Union[Unset, str]):
    """

    tags: Optional[AwsEcsExecutionMethodTags]
    type: Union[Unset, str] = UNSET
    task_definition_arn: Union[Unset, str] = UNSET
    task_definition_infrastructure_website_url: Union[Unset, str] = UNSET
    allocated_cpu_units: Union[Unset, int] = UNSET
    allocated_memory_mb: Union[Unset, int] = UNSET
    subnets: Union[Unset, List[str]] = UNSET
    subnet_infrastructure_website_urls: Union[Unset, None, List[Optional[str]]] = UNSET
    security_groups: Union[Unset, List[str]] = UNSET
    security_group_infrastructure_website_urls: Union[Unset, None, List[Optional[str]]] = UNSET
    assign_public_ip: Union[Unset, bool] = UNSET
    task_arn: Union[Unset, str] = UNSET
    launch_type: Union[Unset, AwsEcsLaunchType] = AwsEcsLaunchType.FARGATE
    cluster_arn: Union[Unset, str] = UNSET
    cluster_infrastructure_website_url: Union[Unset, str] = UNSET
    execution_role: Union[Unset, str] = UNSET
    execution_role_infrastructure_website_url: Union[Unset, str] = UNSET
    task_role: Union[Unset, str] = UNSET
    task_role_infrastructure_website_url: Union[Unset, str] = UNSET
    platform_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        task_definition_arn = self.task_definition_arn
        task_definition_infrastructure_website_url = self.task_definition_infrastructure_website_url
        allocated_cpu_units = self.allocated_cpu_units
        allocated_memory_mb = self.allocated_memory_mb
        tags = self.tags.to_dict() if self.tags else None

        subnets: Union[Unset, List[str]] = UNSET
        if not isinstance(self.subnets, Unset):
            subnets = self.subnets

        subnet_infrastructure_website_urls: Union[Unset, None, List[Optional[str]]] = UNSET
        if not isinstance(self.subnet_infrastructure_website_urls, Unset):
            if self.subnet_infrastructure_website_urls is None:
                subnet_infrastructure_website_urls = None
            else:
                subnet_infrastructure_website_urls = self.subnet_infrastructure_website_urls

        security_groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = self.security_groups

        security_group_infrastructure_website_urls: Union[Unset, None, List[Optional[str]]] = UNSET
        if not isinstance(self.security_group_infrastructure_website_urls, Unset):
            if self.security_group_infrastructure_website_urls is None:
                security_group_infrastructure_website_urls = None
            else:
                security_group_infrastructure_website_urls = self.security_group_infrastructure_website_urls

        assign_public_ip = self.assign_public_ip
        task_arn = self.task_arn
        launch_type: Union[Unset, str] = UNSET
        if not isinstance(self.launch_type, Unset):
            launch_type = self.launch_type.value

        cluster_arn = self.cluster_arn
        cluster_infrastructure_website_url = self.cluster_infrastructure_website_url
        execution_role = self.execution_role
        execution_role_infrastructure_website_url = self.execution_role_infrastructure_website_url
        task_role = self.task_role
        task_role_infrastructure_website_url = self.task_role_infrastructure_website_url
        platform_version = self.platform_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tags": tags,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if task_definition_arn is not UNSET:
            field_dict["task_definition_arn"] = task_definition_arn
        if task_definition_infrastructure_website_url is not UNSET:
            field_dict["task_definition_infrastructure_website_url"] = task_definition_infrastructure_website_url
        if allocated_cpu_units is not UNSET:
            field_dict["allocated_cpu_units"] = allocated_cpu_units
        if allocated_memory_mb is not UNSET:
            field_dict["allocated_memory_mb"] = allocated_memory_mb
        if subnets is not UNSET:
            field_dict["subnets"] = subnets
        if subnet_infrastructure_website_urls is not UNSET:
            field_dict["subnet_infrastructure_website_urls"] = subnet_infrastructure_website_urls
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups
        if security_group_infrastructure_website_urls is not UNSET:
            field_dict["security_group_infrastructure_website_urls"] = security_group_infrastructure_website_urls
        if assign_public_ip is not UNSET:
            field_dict["assign_public_ip"] = assign_public_ip
        if task_arn is not UNSET:
            field_dict["task_arn"] = task_arn
        if launch_type is not UNSET:
            field_dict["launch_type"] = launch_type
        if cluster_arn is not UNSET:
            field_dict["cluster_arn"] = cluster_arn
        if cluster_infrastructure_website_url is not UNSET:
            field_dict["cluster_infrastructure_website_url"] = cluster_infrastructure_website_url
        if execution_role is not UNSET:
            field_dict["execution_role"] = execution_role
        if execution_role_infrastructure_website_url is not UNSET:
            field_dict["execution_role_infrastructure_website_url"] = execution_role_infrastructure_website_url
        if task_role is not UNSET:
            field_dict["task_role"] = task_role
        if task_role_infrastructure_website_url is not UNSET:
            field_dict["task_role_infrastructure_website_url"] = task_role_infrastructure_website_url
        if platform_version is not UNSET:
            field_dict["platform_version"] = platform_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        task_definition_arn = d.pop("task_definition_arn", UNSET)

        task_definition_infrastructure_website_url = d.pop("task_definition_infrastructure_website_url", UNSET)

        allocated_cpu_units = d.pop("allocated_cpu_units", UNSET)

        allocated_memory_mb = d.pop("allocated_memory_mb", UNSET)

        _tags = d.pop("tags")
        tags: Optional[AwsEcsExecutionMethodTags]
        if _tags is None:
            tags = None
        else:
            tags = AwsEcsExecutionMethodTags.from_dict(_tags)

        subnets = cast(List[str], d.pop("subnets", UNSET))

        subnet_infrastructure_website_urls = cast(
            List[Optional[str]], d.pop("subnet_infrastructure_website_urls", UNSET)
        )

        security_groups = cast(List[str], d.pop("security_groups", UNSET))

        security_group_infrastructure_website_urls = cast(
            List[Optional[str]], d.pop("security_group_infrastructure_website_urls", UNSET)
        )

        assign_public_ip = d.pop("assign_public_ip", UNSET)

        task_arn = d.pop("task_arn", UNSET)

        _launch_type = d.pop("launch_type", UNSET)
        launch_type: Union[Unset, AwsEcsLaunchType]
        if isinstance(_launch_type, Unset):
            launch_type = UNSET
        else:
            launch_type = AwsEcsLaunchType(_launch_type)

        cluster_arn = d.pop("cluster_arn", UNSET)

        cluster_infrastructure_website_url = d.pop("cluster_infrastructure_website_url", UNSET)

        execution_role = d.pop("execution_role", UNSET)

        execution_role_infrastructure_website_url = d.pop("execution_role_infrastructure_website_url", UNSET)

        task_role = d.pop("task_role", UNSET)

        task_role_infrastructure_website_url = d.pop("task_role_infrastructure_website_url", UNSET)

        platform_version = d.pop("platform_version", UNSET)

        aws_ecs_execution_method = cls(
            type=type,
            task_definition_arn=task_definition_arn,
            task_definition_infrastructure_website_url=task_definition_infrastructure_website_url,
            allocated_cpu_units=allocated_cpu_units,
            allocated_memory_mb=allocated_memory_mb,
            tags=tags,
            subnets=subnets,
            subnet_infrastructure_website_urls=subnet_infrastructure_website_urls,
            security_groups=security_groups,
            security_group_infrastructure_website_urls=security_group_infrastructure_website_urls,
            assign_public_ip=assign_public_ip,
            task_arn=task_arn,
            launch_type=launch_type,
            cluster_arn=cluster_arn,
            cluster_infrastructure_website_url=cluster_infrastructure_website_url,
            execution_role=execution_role,
            execution_role_infrastructure_website_url=execution_role_infrastructure_website_url,
            task_role=task_role,
            task_role_infrastructure_website_url=task_role_infrastructure_website_url,
            platform_version=platform_version,
        )

        aws_ecs_execution_method.additional_properties = d
        return aws_ecs_execution_method

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
