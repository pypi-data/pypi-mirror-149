from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsEcsServiceLoadBalancerDetails")


@attr.s(auto_attribs=True)
class AwsEcsServiceLoadBalancerDetails:
    """Configuration for a service AWS ECS Task that is behind an application load
    balancer.

        Attributes:
            target_group_arn (str):
            container_port (int):
            container_name (Union[Unset, str]):
    """

    target_group_arn: str
    container_port: int
    container_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target_group_arn = self.target_group_arn
        container_port = self.container_port
        container_name = self.container_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_group_arn": target_group_arn,
                "container_port": container_port,
            }
        )
        if container_name is not UNSET:
            field_dict["container_name"] = container_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        target_group_arn = d.pop("target_group_arn")

        container_port = d.pop("container_port")

        container_name = d.pop("container_name", UNSET)

        aws_ecs_service_load_balancer_details = cls(
            target_group_arn=target_group_arn,
            container_port=container_port,
            container_name=container_name,
        )

        aws_ecs_service_load_balancer_details.additional_properties = d
        return aws_ecs_service_load_balancer_details

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
