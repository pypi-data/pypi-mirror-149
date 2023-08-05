from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..models.aws_ecs_execution_method_capability_tags import AwsEcsExecutionMethodCapabilityTags
from ..models.aws_ecs_launch_type import AwsEcsLaunchType
from ..models.aws_ecs_service_options import AwsEcsServiceOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsEcsExecutionMethodCapability")


@attr.s(auto_attribs=True)
class AwsEcsExecutionMethodCapability:
    """A ModelSerializer that takes additional arguments for
    "fields", "omit" and "expand" in order to
    control which fields are displayed, and whether to replace simple
    values with complex, nested serializations

        Attributes:
            task_definition_arn (Union[Unset, str]):
            task_definition_infrastructure_website_url (Union[Unset, str]):
            allocated_cpu_units (Union[Unset, int]):
            allocated_memory_mb (Union[Unset, int]):
            type (Union[Unset, str]):
            capabilities (Union[Unset, List[str]]):
            tags (Optional[AwsEcsExecutionMethodCapabilityTags]):
            default_subnets (Union[Unset, None, List[str]]):
            default_subnet_infrastructure_website_urls (Union[Unset, List[str]]):
            default_launch_type (Union[Unset, None, AwsEcsLaunchType]):  Default: AwsEcsLaunchType.FARGATE.
            supported_launch_types (Union[Unset, None, List[AwsEcsLaunchType]]):
            default_cluster_arn (Union[Unset, str]):
            default_cluster_infrastructure_website_url (Union[Unset, str]):
            default_security_groups (Union[Unset, None, List[str]]):
            default_security_group_infrastructure_website_urls (Union[Unset, List[str]]):
            default_assign_public_ip (Union[Unset, None, bool]):
            default_execution_role (Union[Unset, str]):
            default_execution_role_infrastructure_website_url (Union[Unset, str]):
            default_task_role (Union[Unset, str]):
            default_task_role_infrastructure_website_url (Union[Unset, str]):
            default_platform_version (Union[Unset, str]):
            main_container_name (Union[Unset, str]):
            service_options (Union[Unset, AwsEcsServiceOptions]): Options for running a Task as a service in AWS ECS.
    """

    tags: Optional[AwsEcsExecutionMethodCapabilityTags]
    task_definition_arn: Union[Unset, str] = UNSET
    task_definition_infrastructure_website_url: Union[Unset, str] = UNSET
    allocated_cpu_units: Union[Unset, int] = UNSET
    allocated_memory_mb: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    capabilities: Union[Unset, List[str]] = UNSET
    default_subnets: Union[Unset, None, List[str]] = UNSET
    default_subnet_infrastructure_website_urls: Union[Unset, List[str]] = UNSET
    default_launch_type: Union[Unset, None, AwsEcsLaunchType] = AwsEcsLaunchType.FARGATE
    supported_launch_types: Union[Unset, None, List[AwsEcsLaunchType]] = UNSET
    default_cluster_arn: Union[Unset, str] = UNSET
    default_cluster_infrastructure_website_url: Union[Unset, str] = UNSET
    default_security_groups: Union[Unset, None, List[str]] = UNSET
    default_security_group_infrastructure_website_urls: Union[Unset, List[str]] = UNSET
    default_assign_public_ip: Union[Unset, None, bool] = UNSET
    default_execution_role: Union[Unset, str] = UNSET
    default_execution_role_infrastructure_website_url: Union[Unset, str] = UNSET
    default_task_role: Union[Unset, str] = UNSET
    default_task_role_infrastructure_website_url: Union[Unset, str] = UNSET
    default_platform_version: Union[Unset, str] = UNSET
    main_container_name: Union[Unset, str] = UNSET
    service_options: Union[Unset, AwsEcsServiceOptions] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_definition_arn = self.task_definition_arn
        task_definition_infrastructure_website_url = self.task_definition_infrastructure_website_url
        allocated_cpu_units = self.allocated_cpu_units
        allocated_memory_mb = self.allocated_memory_mb
        type = self.type
        capabilities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        tags = self.tags.to_dict() if self.tags else None

        default_subnets: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.default_subnets, Unset):
            if self.default_subnets is None:
                default_subnets = None
            else:
                default_subnets = self.default_subnets

        default_subnet_infrastructure_website_urls: Union[Unset, List[str]] = UNSET
        if not isinstance(self.default_subnet_infrastructure_website_urls, Unset):
            default_subnet_infrastructure_website_urls = self.default_subnet_infrastructure_website_urls

        default_launch_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.default_launch_type, Unset):
            default_launch_type = self.default_launch_type.value if self.default_launch_type else None

        supported_launch_types: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.supported_launch_types, Unset):
            if self.supported_launch_types is None:
                supported_launch_types = None
            else:
                supported_launch_types = []
                for supported_launch_types_item_data in self.supported_launch_types:
                    supported_launch_types_item = supported_launch_types_item_data.value

                    supported_launch_types.append(supported_launch_types_item)

        default_cluster_arn = self.default_cluster_arn
        default_cluster_infrastructure_website_url = self.default_cluster_infrastructure_website_url
        default_security_groups: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.default_security_groups, Unset):
            if self.default_security_groups is None:
                default_security_groups = None
            else:
                default_security_groups = self.default_security_groups

        default_security_group_infrastructure_website_urls: Union[Unset, List[str]] = UNSET
        if not isinstance(self.default_security_group_infrastructure_website_urls, Unset):
            default_security_group_infrastructure_website_urls = self.default_security_group_infrastructure_website_urls

        default_assign_public_ip = self.default_assign_public_ip
        default_execution_role = self.default_execution_role
        default_execution_role_infrastructure_website_url = self.default_execution_role_infrastructure_website_url
        default_task_role = self.default_task_role
        default_task_role_infrastructure_website_url = self.default_task_role_infrastructure_website_url
        default_platform_version = self.default_platform_version
        main_container_name = self.main_container_name
        service_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service_options, Unset):
            service_options = self.service_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tags": tags,
            }
        )
        if task_definition_arn is not UNSET:
            field_dict["task_definition_arn"] = task_definition_arn
        if task_definition_infrastructure_website_url is not UNSET:
            field_dict["task_definition_infrastructure_website_url"] = task_definition_infrastructure_website_url
        if allocated_cpu_units is not UNSET:
            field_dict["allocated_cpu_units"] = allocated_cpu_units
        if allocated_memory_mb is not UNSET:
            field_dict["allocated_memory_mb"] = allocated_memory_mb
        if type is not UNSET:
            field_dict["type"] = type
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if default_subnets is not UNSET:
            field_dict["default_subnets"] = default_subnets
        if default_subnet_infrastructure_website_urls is not UNSET:
            field_dict["default_subnet_infrastructure_website_urls"] = default_subnet_infrastructure_website_urls
        if default_launch_type is not UNSET:
            field_dict["default_launch_type"] = default_launch_type
        if supported_launch_types is not UNSET:
            field_dict["supported_launch_types"] = supported_launch_types
        if default_cluster_arn is not UNSET:
            field_dict["default_cluster_arn"] = default_cluster_arn
        if default_cluster_infrastructure_website_url is not UNSET:
            field_dict["default_cluster_infrastructure_website_url"] = default_cluster_infrastructure_website_url
        if default_security_groups is not UNSET:
            field_dict["default_security_groups"] = default_security_groups
        if default_security_group_infrastructure_website_urls is not UNSET:
            field_dict[
                "default_security_group_infrastructure_website_urls"
            ] = default_security_group_infrastructure_website_urls
        if default_assign_public_ip is not UNSET:
            field_dict["default_assign_public_ip"] = default_assign_public_ip
        if default_execution_role is not UNSET:
            field_dict["default_execution_role"] = default_execution_role
        if default_execution_role_infrastructure_website_url is not UNSET:
            field_dict[
                "default_execution_role_infrastructure_website_url"
            ] = default_execution_role_infrastructure_website_url
        if default_task_role is not UNSET:
            field_dict["default_task_role"] = default_task_role
        if default_task_role_infrastructure_website_url is not UNSET:
            field_dict["default_task_role_infrastructure_website_url"] = default_task_role_infrastructure_website_url
        if default_platform_version is not UNSET:
            field_dict["default_platform_version"] = default_platform_version
        if main_container_name is not UNSET:
            field_dict["main_container_name"] = main_container_name
        if service_options is not UNSET:
            field_dict["service_options"] = service_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_definition_arn = d.pop("task_definition_arn", UNSET)

        task_definition_infrastructure_website_url = d.pop("task_definition_infrastructure_website_url", UNSET)

        allocated_cpu_units = d.pop("allocated_cpu_units", UNSET)

        allocated_memory_mb = d.pop("allocated_memory_mb", UNSET)

        type = d.pop("type", UNSET)

        capabilities = cast(List[str], d.pop("capabilities", UNSET))

        _tags = d.pop("tags")
        tags: Optional[AwsEcsExecutionMethodCapabilityTags]
        if _tags is None:
            tags = None
        else:
            tags = AwsEcsExecutionMethodCapabilityTags.from_dict(_tags)

        default_subnets = cast(List[str], d.pop("default_subnets", UNSET))

        default_subnet_infrastructure_website_urls = cast(
            List[str], d.pop("default_subnet_infrastructure_website_urls", UNSET)
        )

        _default_launch_type = d.pop("default_launch_type", UNSET)
        default_launch_type: Union[Unset, None, AwsEcsLaunchType]
        if _default_launch_type is None:
            default_launch_type = None
        elif isinstance(_default_launch_type, Unset):
            default_launch_type = UNSET
        else:
            default_launch_type = AwsEcsLaunchType(_default_launch_type)

        supported_launch_types = []
        _supported_launch_types = d.pop("supported_launch_types", UNSET)
        for supported_launch_types_item_data in _supported_launch_types or []:
            supported_launch_types_item = AwsEcsLaunchType(supported_launch_types_item_data)

            supported_launch_types.append(supported_launch_types_item)

        default_cluster_arn = d.pop("default_cluster_arn", UNSET)

        default_cluster_infrastructure_website_url = d.pop("default_cluster_infrastructure_website_url", UNSET)

        default_security_groups = cast(List[str], d.pop("default_security_groups", UNSET))

        default_security_group_infrastructure_website_urls = cast(
            List[str], d.pop("default_security_group_infrastructure_website_urls", UNSET)
        )

        default_assign_public_ip = d.pop("default_assign_public_ip", UNSET)

        default_execution_role = d.pop("default_execution_role", UNSET)

        default_execution_role_infrastructure_website_url = d.pop(
            "default_execution_role_infrastructure_website_url", UNSET
        )

        default_task_role = d.pop("default_task_role", UNSET)

        default_task_role_infrastructure_website_url = d.pop("default_task_role_infrastructure_website_url", UNSET)

        default_platform_version = d.pop("default_platform_version", UNSET)

        main_container_name = d.pop("main_container_name", UNSET)

        _service_options = d.pop("service_options", UNSET)
        service_options: Union[Unset, AwsEcsServiceOptions]
        if isinstance(_service_options, Unset):
            service_options = UNSET
        else:
            service_options = AwsEcsServiceOptions.from_dict(_service_options)

        aws_ecs_execution_method_capability = cls(
            task_definition_arn=task_definition_arn,
            task_definition_infrastructure_website_url=task_definition_infrastructure_website_url,
            allocated_cpu_units=allocated_cpu_units,
            allocated_memory_mb=allocated_memory_mb,
            type=type,
            capabilities=capabilities,
            tags=tags,
            default_subnets=default_subnets,
            default_subnet_infrastructure_website_urls=default_subnet_infrastructure_website_urls,
            default_launch_type=default_launch_type,
            supported_launch_types=supported_launch_types,
            default_cluster_arn=default_cluster_arn,
            default_cluster_infrastructure_website_url=default_cluster_infrastructure_website_url,
            default_security_groups=default_security_groups,
            default_security_group_infrastructure_website_urls=default_security_group_infrastructure_website_urls,
            default_assign_public_ip=default_assign_public_ip,
            default_execution_role=default_execution_role,
            default_execution_role_infrastructure_website_url=default_execution_role_infrastructure_website_url,
            default_task_role=default_task_role,
            default_task_role_infrastructure_website_url=default_task_role_infrastructure_website_url,
            default_platform_version=default_platform_version,
            main_container_name=main_container_name,
            service_options=service_options,
        )

        aws_ecs_execution_method_capability.additional_properties = d
        return aws_ecs_execution_method_capability

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
