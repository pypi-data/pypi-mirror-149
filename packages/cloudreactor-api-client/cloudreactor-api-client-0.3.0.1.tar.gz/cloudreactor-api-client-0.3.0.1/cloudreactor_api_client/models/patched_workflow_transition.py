import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.name_and_uuid import NameAndUuid
from ..models.rule_type_enum import RuleTypeEnum
from ..models.threshold_property_enum import ThresholdPropertyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedWorkflowTransition")


@attr.s(auto_attribs=True)
class PatchedWorkflowTransition:
    """A WorkflowTransition is a directed edge in a Worfklow, which is a directed
    graph. It contains a source WorkflowTaskInstance, a destination
    WorkflowTaskInstance, as well as conditions for triggering the destination
    to execution.

        Attributes:
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            description (Union[Unset, str]):
            from_workflow_task_instance (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name;
                and 3. URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            to_workflow_task_instance (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and
                3. URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            rule_type (Union[Unset, RuleTypeEnum]):
            exit_codes (Union[Unset, None, List[str]]):
            threshold_property (Union[Unset, ThresholdPropertyEnum]):
            custom_expression (Union[Unset, str]):
            priority (Union[Unset, None, int]):
            ui_color (Union[Unset, str]):
            ui_line_style (Union[Unset, str]):
            ui_scale (Union[Unset, None, float]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    from_workflow_task_instance: Union[Unset, NameAndUuid] = UNSET
    to_workflow_task_instance: Union[Unset, NameAndUuid] = UNSET
    rule_type: Union[Unset, RuleTypeEnum] = UNSET
    exit_codes: Union[Unset, None, List[str]] = UNSET
    threshold_property: Union[Unset, ThresholdPropertyEnum] = UNSET
    custom_expression: Union[Unset, str] = UNSET
    priority: Union[Unset, None, int] = UNSET
    ui_color: Union[Unset, str] = UNSET
    ui_line_style: Union[Unset, str] = UNSET
    ui_scale: Union[Unset, None, float] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        uuid = self.uuid
        description = self.description
        from_workflow_task_instance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.from_workflow_task_instance, Unset):
            from_workflow_task_instance = self.from_workflow_task_instance.to_dict()

        to_workflow_task_instance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.to_workflow_task_instance, Unset):
            to_workflow_task_instance = self.to_workflow_task_instance.to_dict()

        rule_type: Union[Unset, str] = UNSET
        if not isinstance(self.rule_type, Unset):
            rule_type = self.rule_type.value

        exit_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.exit_codes, Unset):
            if self.exit_codes is None:
                exit_codes = None
            else:
                exit_codes = self.exit_codes

        threshold_property: Union[Unset, str] = UNSET
        if not isinstance(self.threshold_property, Unset):
            threshold_property = self.threshold_property.value

        custom_expression = self.custom_expression
        priority = self.priority
        ui_color = self.ui_color
        ui_line_style = self.ui_line_style
        ui_scale = self.ui_scale
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if from_workflow_task_instance is not UNSET:
            field_dict["from_workflow_task_instance"] = from_workflow_task_instance
        if to_workflow_task_instance is not UNSET:
            field_dict["to_workflow_task_instance"] = to_workflow_task_instance
        if rule_type is not UNSET:
            field_dict["rule_type"] = rule_type
        if exit_codes is not UNSET:
            field_dict["exit_codes"] = exit_codes
        if threshold_property is not UNSET:
            field_dict["threshold_property"] = threshold_property
        if custom_expression is not UNSET:
            field_dict["custom_expression"] = custom_expression
        if priority is not UNSET:
            field_dict["priority"] = priority
        if ui_color is not UNSET:
            field_dict["ui_color"] = ui_color
        if ui_line_style is not UNSET:
            field_dict["ui_line_style"] = ui_line_style
        if ui_scale is not UNSET:
            field_dict["ui_scale"] = ui_scale
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        _from_workflow_task_instance = d.pop("from_workflow_task_instance", UNSET)
        from_workflow_task_instance: Union[Unset, NameAndUuid]
        if isinstance(_from_workflow_task_instance, Unset):
            from_workflow_task_instance = UNSET
        else:
            from_workflow_task_instance = NameAndUuid.from_dict(_from_workflow_task_instance)

        _to_workflow_task_instance = d.pop("to_workflow_task_instance", UNSET)
        to_workflow_task_instance: Union[Unset, NameAndUuid]
        if isinstance(_to_workflow_task_instance, Unset):
            to_workflow_task_instance = UNSET
        else:
            to_workflow_task_instance = NameAndUuid.from_dict(_to_workflow_task_instance)

        _rule_type = d.pop("rule_type", UNSET)
        rule_type: Union[Unset, RuleTypeEnum]
        if isinstance(_rule_type, Unset):
            rule_type = UNSET
        else:
            rule_type = RuleTypeEnum(_rule_type)

        exit_codes = cast(List[str], d.pop("exit_codes", UNSET))

        _threshold_property = d.pop("threshold_property", UNSET)
        threshold_property: Union[Unset, ThresholdPropertyEnum]
        if isinstance(_threshold_property, Unset):
            threshold_property = UNSET
        else:
            threshold_property = ThresholdPropertyEnum(_threshold_property)

        custom_expression = d.pop("custom_expression", UNSET)

        priority = d.pop("priority", UNSET)

        ui_color = d.pop("ui_color", UNSET)

        ui_line_style = d.pop("ui_line_style", UNSET)

        ui_scale = d.pop("ui_scale", UNSET)

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

        patched_workflow_transition = cls(
            url=url,
            uuid=uuid,
            description=description,
            from_workflow_task_instance=from_workflow_task_instance,
            to_workflow_task_instance=to_workflow_task_instance,
            rule_type=rule_type,
            exit_codes=exit_codes,
            threshold_property=threshold_property,
            custom_expression=custom_expression,
            priority=priority,
            ui_color=ui_color,
            ui_line_style=ui_line_style,
            ui_scale=ui_scale,
            created_at=created_at,
            updated_at=updated_at,
        )

        patched_workflow_transition.additional_properties = d
        return patched_workflow_transition

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
