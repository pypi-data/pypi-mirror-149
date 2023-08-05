import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.group import Group
from ..models.name_and_uuid import NameAndUuid
from ..models.workflow_execution_summary import WorkflowExecutionSummary
from ..models.workflow_task_instance import WorkflowTaskInstance
from ..models.workflow_transition import WorkflowTransition
from ..types import UNSET, Unset

T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """Workflows are Tasks arranged in a directed graph. Configured Tasks
    are held by WorkflowTaskInstances, and WorkflowTransitions connect
    WorkflowTaskInstances together.

        Attributes:
            name (str):
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            description (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            schedule (Union[Unset, str]):
            max_concurrency (Union[Unset, None, int]):
            max_age_seconds (Union[Unset, None, int]):
            default_max_retries (Union[Unset, int]):
            latest_workflow_execution (Union[Unset, None, WorkflowExecutionSummary]): A WorkflowExecutionSummary contains a
                subset of the data inside of a
                WorkflowExecution.
            created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
            created_by_group (Union[Unset, Group]):
            run_environment (Union[Unset, None, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            enabled (Union[Unset, bool]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
            alert_methods (Union[Unset, List[NameAndUuid]]):
            workflow_task_instances (Union[Unset, List[WorkflowTaskInstance]]):
            workflow_transitions (Union[Unset, List[WorkflowTransition]]):
    """

    name: str
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    schedule: Union[Unset, str] = UNSET
    max_concurrency: Union[Unset, None, int] = UNSET
    max_age_seconds: Union[Unset, None, int] = UNSET
    default_max_retries: Union[Unset, int] = UNSET
    latest_workflow_execution: Union[Unset, None, WorkflowExecutionSummary] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    run_environment: Union[Unset, None, NameAndUuid] = UNSET
    enabled: Union[Unset, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    alert_methods: Union[Unset, List[NameAndUuid]] = UNSET
    workflow_task_instances: Union[Unset, List[WorkflowTaskInstance]] = UNSET
    workflow_transitions: Union[Unset, List[WorkflowTransition]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        url = self.url
        uuid = self.uuid
        description = self.description
        dashboard_url = self.dashboard_url
        schedule = self.schedule
        max_concurrency = self.max_concurrency
        max_age_seconds = self.max_age_seconds
        default_max_retries = self.default_max_retries
        latest_workflow_execution: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.latest_workflow_execution, Unset):
            latest_workflow_execution = (
                self.latest_workflow_execution.to_dict() if self.latest_workflow_execution else None
            )

        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        run_environment: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.run_environment, Unset):
            run_environment = self.run_environment.to_dict() if self.run_environment else None

        enabled = self.enabled
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        alert_methods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.alert_methods, Unset):
            alert_methods = []
            for alert_methods_item_data in self.alert_methods:
                alert_methods_item = alert_methods_item_data.to_dict()

                alert_methods.append(alert_methods_item)

        workflow_task_instances: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_task_instances, Unset):
            workflow_task_instances = []
            for workflow_task_instances_item_data in self.workflow_task_instances:
                workflow_task_instances_item = workflow_task_instances_item_data.to_dict()

                workflow_task_instances.append(workflow_task_instances_item)

        workflow_transitions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_transitions, Unset):
            workflow_transitions = []
            for workflow_transitions_item_data in self.workflow_transitions:
                workflow_transitions_item = workflow_transitions_item_data.to_dict()

                workflow_transitions.append(workflow_transitions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if max_concurrency is not UNSET:
            field_dict["max_concurrency"] = max_concurrency
        if max_age_seconds is not UNSET:
            field_dict["max_age_seconds"] = max_age_seconds
        if default_max_retries is not UNSET:
            field_dict["default_max_retries"] = default_max_retries
        if latest_workflow_execution is not UNSET:
            field_dict["latest_workflow_execution"] = latest_workflow_execution
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if run_environment is not UNSET:
            field_dict["run_environment"] = run_environment
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if alert_methods is not UNSET:
            field_dict["alert_methods"] = alert_methods
        if workflow_task_instances is not UNSET:
            field_dict["workflow_task_instances"] = workflow_task_instances
        if workflow_transitions is not UNSET:
            field_dict["workflow_transitions"] = workflow_transitions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        schedule = d.pop("schedule", UNSET)

        max_concurrency = d.pop("max_concurrency", UNSET)

        max_age_seconds = d.pop("max_age_seconds", UNSET)

        default_max_retries = d.pop("default_max_retries", UNSET)

        _latest_workflow_execution = d.pop("latest_workflow_execution", UNSET)
        latest_workflow_execution: Union[Unset, None, WorkflowExecutionSummary]
        if _latest_workflow_execution is None:
            latest_workflow_execution = None
        elif isinstance(_latest_workflow_execution, Unset):
            latest_workflow_execution = UNSET
        else:
            latest_workflow_execution = WorkflowExecutionSummary.from_dict(_latest_workflow_execution)

        created_by_user = d.pop("created_by_user", UNSET)

        _created_by_group = d.pop("created_by_group", UNSET)
        created_by_group: Union[Unset, Group]
        if isinstance(_created_by_group, Unset):
            created_by_group = UNSET
        else:
            created_by_group = Group.from_dict(_created_by_group)

        _run_environment = d.pop("run_environment", UNSET)
        run_environment: Union[Unset, None, NameAndUuid]
        if _run_environment is None:
            run_environment = None
        elif isinstance(_run_environment, Unset):
            run_environment = UNSET
        else:
            run_environment = NameAndUuid.from_dict(_run_environment)

        enabled = d.pop("enabled", UNSET)

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

        alert_methods = []
        _alert_methods = d.pop("alert_methods", UNSET)
        for alert_methods_item_data in _alert_methods or []:
            alert_methods_item = NameAndUuid.from_dict(alert_methods_item_data)

            alert_methods.append(alert_methods_item)

        workflow_task_instances = []
        _workflow_task_instances = d.pop("workflow_task_instances", UNSET)
        for workflow_task_instances_item_data in _workflow_task_instances or []:
            workflow_task_instances_item = WorkflowTaskInstance.from_dict(workflow_task_instances_item_data)

            workflow_task_instances.append(workflow_task_instances_item)

        workflow_transitions = []
        _workflow_transitions = d.pop("workflow_transitions", UNSET)
        for workflow_transitions_item_data in _workflow_transitions or []:
            workflow_transitions_item = WorkflowTransition.from_dict(workflow_transitions_item_data)

            workflow_transitions.append(workflow_transitions_item)

        workflow = cls(
            name=name,
            url=url,
            uuid=uuid,
            description=description,
            dashboard_url=dashboard_url,
            schedule=schedule,
            max_concurrency=max_concurrency,
            max_age_seconds=max_age_seconds,
            default_max_retries=default_max_retries,
            latest_workflow_execution=latest_workflow_execution,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            run_environment=run_environment,
            enabled=enabled,
            created_at=created_at,
            updated_at=updated_at,
            alert_methods=alert_methods,
            workflow_task_instances=workflow_task_instances,
            workflow_transitions=workflow_transitions,
        )

        workflow.additional_properties = d
        return workflow

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
