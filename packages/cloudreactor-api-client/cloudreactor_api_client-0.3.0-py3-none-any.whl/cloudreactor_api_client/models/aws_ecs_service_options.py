from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aws_ecs_service_load_balancer_details import AwsEcsServiceLoadBalancerDetails
from ..models.aws_ecs_service_options_tags import AwsEcsServiceOptionsTags
from ..models.propagate_tags_enum import PropagateTagsEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsEcsServiceOptions")


@attr.s(auto_attribs=True)
class AwsEcsServiceOptions:
    """Options for running a Task as a service in AWS ECS.

    Attributes:
        load_balancers (Union[Unset, List[AwsEcsServiceLoadBalancerDetails]]):
        health_check_grace_period_seconds (Union[Unset, int]):
        force_new_deployment (Union[Unset, bool]):
        deploy_minimum_healthy_percent (Union[Unset, int]):
        deploy_maximum_percent (Union[Unset, int]):
        deploy_enable_circuit_breaker (Union[Unset, bool]):
        deploy_rollback_on_failure (Union[Unset, bool]):
        enable_ecs_managed_tags (Union[Unset, bool]):
        propagate_tags (Union[Unset, PropagateTagsEnum]):
        tags (Union[Unset, None, AwsEcsServiceOptionsTags]):
    """

    load_balancers: Union[Unset, List[AwsEcsServiceLoadBalancerDetails]] = UNSET
    health_check_grace_period_seconds: Union[Unset, int] = UNSET
    force_new_deployment: Union[Unset, bool] = UNSET
    deploy_minimum_healthy_percent: Union[Unset, int] = UNSET
    deploy_maximum_percent: Union[Unset, int] = UNSET
    deploy_enable_circuit_breaker: Union[Unset, bool] = UNSET
    deploy_rollback_on_failure: Union[Unset, bool] = UNSET
    enable_ecs_managed_tags: Union[Unset, bool] = UNSET
    propagate_tags: Union[Unset, PropagateTagsEnum] = UNSET
    tags: Union[Unset, None, AwsEcsServiceOptionsTags] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        load_balancers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.load_balancers, Unset):
            load_balancers = []
            for load_balancers_item_data in self.load_balancers:
                load_balancers_item = load_balancers_item_data.to_dict()

                load_balancers.append(load_balancers_item)

        health_check_grace_period_seconds = self.health_check_grace_period_seconds
        force_new_deployment = self.force_new_deployment
        deploy_minimum_healthy_percent = self.deploy_minimum_healthy_percent
        deploy_maximum_percent = self.deploy_maximum_percent
        deploy_enable_circuit_breaker = self.deploy_enable_circuit_breaker
        deploy_rollback_on_failure = self.deploy_rollback_on_failure
        enable_ecs_managed_tags = self.enable_ecs_managed_tags
        propagate_tags: Union[Unset, str] = UNSET
        if not isinstance(self.propagate_tags, Unset):
            propagate_tags = self.propagate_tags.value

        tags: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict() if self.tags else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if load_balancers is not UNSET:
            field_dict["load_balancers"] = load_balancers
        if health_check_grace_period_seconds is not UNSET:
            field_dict["health_check_grace_period_seconds"] = health_check_grace_period_seconds
        if force_new_deployment is not UNSET:
            field_dict["force_new_deployment"] = force_new_deployment
        if deploy_minimum_healthy_percent is not UNSET:
            field_dict["deploy_minimum_healthy_percent"] = deploy_minimum_healthy_percent
        if deploy_maximum_percent is not UNSET:
            field_dict["deploy_maximum_percent"] = deploy_maximum_percent
        if deploy_enable_circuit_breaker is not UNSET:
            field_dict["deploy_enable_circuit_breaker"] = deploy_enable_circuit_breaker
        if deploy_rollback_on_failure is not UNSET:
            field_dict["deploy_rollback_on_failure"] = deploy_rollback_on_failure
        if enable_ecs_managed_tags is not UNSET:
            field_dict["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if propagate_tags is not UNSET:
            field_dict["propagate_tags"] = propagate_tags
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        load_balancers = []
        _load_balancers = d.pop("load_balancers", UNSET)
        for load_balancers_item_data in _load_balancers or []:
            load_balancers_item = AwsEcsServiceLoadBalancerDetails.from_dict(load_balancers_item_data)

            load_balancers.append(load_balancers_item)

        health_check_grace_period_seconds = d.pop("health_check_grace_period_seconds", UNSET)

        force_new_deployment = d.pop("force_new_deployment", UNSET)

        deploy_minimum_healthy_percent = d.pop("deploy_minimum_healthy_percent", UNSET)

        deploy_maximum_percent = d.pop("deploy_maximum_percent", UNSET)

        deploy_enable_circuit_breaker = d.pop("deploy_enable_circuit_breaker", UNSET)

        deploy_rollback_on_failure = d.pop("deploy_rollback_on_failure", UNSET)

        enable_ecs_managed_tags = d.pop("enable_ecs_managed_tags", UNSET)

        _propagate_tags = d.pop("propagate_tags", UNSET)
        propagate_tags: Union[Unset, PropagateTagsEnum]
        if isinstance(_propagate_tags, Unset):
            propagate_tags = UNSET
        else:
            propagate_tags = PropagateTagsEnum(_propagate_tags)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, None, AwsEcsServiceOptionsTags]
        if _tags is None:
            tags = None
        elif isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = AwsEcsServiceOptionsTags.from_dict(_tags)

        aws_ecs_service_options = cls(
            load_balancers=load_balancers,
            health_check_grace_period_seconds=health_check_grace_period_seconds,
            force_new_deployment=force_new_deployment,
            deploy_minimum_healthy_percent=deploy_minimum_healthy_percent,
            deploy_maximum_percent=deploy_maximum_percent,
            deploy_enable_circuit_breaker=deploy_enable_circuit_breaker,
            deploy_rollback_on_failure=deploy_rollback_on_failure,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            propagate_tags=propagate_tags,
            tags=tags,
        )

        aws_ecs_service_options.additional_properties = d
        return aws_ecs_service_options

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
