import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.aws_ecs_execution_method_capability import AwsEcsExecutionMethodCapability
from ..models.current_service_info import CurrentServiceInfo
from ..models.group import Group
from ..models.link import Link
from ..models.name_and_uuid import NameAndUuid
from ..models.patched_task_other_metadata import PatchedTaskOtherMetadata
from ..models.task_execution import TaskExecution
from ..models.unknown_execution_method_capability import UnknownExecutionMethodCapability
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTask")


@attr.s(auto_attribs=True)
class PatchedTask:
    """A Task is a specification for a runnable job, including details on how to
    run the task and how often the task is supposed to run.

        Attributes:
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            infrastructure_website_url (Union[Unset, None, str]):
            max_manual_start_delay_before_alert_seconds (Union[Unset, None, int]):
            max_manual_start_delay_before_abandonment_seconds (Union[Unset, None, int]):
            heartbeat_interval_seconds (Union[Unset, None, int]):
            max_heartbeat_lateness_before_alert_seconds (Union[Unset, None, int]):
            max_heartbeat_lateness_before_abandonment_seconds (Union[Unset, None, int]):
            schedule (Union[Unset, str]):
            scheduled_instance_count (Union[Unset, None, int]):
            is_service (Union[Unset, bool]):
            service_instance_count (Union[Unset, None, int]):
            min_service_instance_count (Union[Unset, None, int]):
            max_concurrency (Union[Unset, None, int]):
            max_age_seconds (Union[Unset, None, int]):
            default_max_retries (Union[Unset, int]):
            project_url (Union[Unset, str]):
            log_query (Union[Unset, str]):
            logs_url (Union[Unset, None, str]):
            links (Union[Unset, List[Link]]):
            run_environment (Union[Unset, None, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            execution_method_capability (Union[AwsEcsExecutionMethodCapability, UnknownExecutionMethodCapability, Unset]):
            alert_methods (Union[Unset, List[NameAndUuid]]):
            other_metadata (Union[Unset, None, PatchedTaskOtherMetadata]):
            latest_task_execution (Union[Unset, None, TaskExecution]): A Task Execution is an execution / run instance of a
                Task.
            current_service_info (Union[Unset, None, CurrentServiceInfo]):
            created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
            created_by_group (Union[Unset, Group]):
            was_auto_created (Union[Unset, None, bool]):
            passive (Union[Unset, bool]):
            enabled (Union[Unset, bool]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    infrastructure_website_url: Union[Unset, None, str] = UNSET
    max_manual_start_delay_before_alert_seconds: Union[Unset, None, int] = UNSET
    max_manual_start_delay_before_abandonment_seconds: Union[Unset, None, int] = UNSET
    heartbeat_interval_seconds: Union[Unset, None, int] = UNSET
    max_heartbeat_lateness_before_alert_seconds: Union[Unset, None, int] = UNSET
    max_heartbeat_lateness_before_abandonment_seconds: Union[Unset, None, int] = UNSET
    schedule: Union[Unset, str] = UNSET
    scheduled_instance_count: Union[Unset, None, int] = UNSET
    is_service: Union[Unset, bool] = UNSET
    service_instance_count: Union[Unset, None, int] = UNSET
    min_service_instance_count: Union[Unset, None, int] = UNSET
    max_concurrency: Union[Unset, None, int] = UNSET
    max_age_seconds: Union[Unset, None, int] = UNSET
    default_max_retries: Union[Unset, int] = UNSET
    project_url: Union[Unset, str] = UNSET
    log_query: Union[Unset, str] = UNSET
    logs_url: Union[Unset, None, str] = UNSET
    links: Union[Unset, List[Link]] = UNSET
    run_environment: Union[Unset, None, NameAndUuid] = UNSET
    execution_method_capability: Union[AwsEcsExecutionMethodCapability, UnknownExecutionMethodCapability, Unset] = UNSET
    alert_methods: Union[Unset, List[NameAndUuid]] = UNSET
    other_metadata: Union[Unset, None, PatchedTaskOtherMetadata] = UNSET
    latest_task_execution: Union[Unset, None, TaskExecution] = UNSET
    current_service_info: Union[Unset, None, CurrentServiceInfo] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    was_auto_created: Union[Unset, None, bool] = UNSET
    passive: Union[Unset, bool] = UNSET
    enabled: Union[Unset, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        uuid = self.uuid
        name = self.name
        description = self.description
        dashboard_url = self.dashboard_url
        infrastructure_website_url = self.infrastructure_website_url
        max_manual_start_delay_before_alert_seconds = self.max_manual_start_delay_before_alert_seconds
        max_manual_start_delay_before_abandonment_seconds = self.max_manual_start_delay_before_abandonment_seconds
        heartbeat_interval_seconds = self.heartbeat_interval_seconds
        max_heartbeat_lateness_before_alert_seconds = self.max_heartbeat_lateness_before_alert_seconds
        max_heartbeat_lateness_before_abandonment_seconds = self.max_heartbeat_lateness_before_abandonment_seconds
        schedule = self.schedule
        scheduled_instance_count = self.scheduled_instance_count
        is_service = self.is_service
        service_instance_count = self.service_instance_count
        min_service_instance_count = self.min_service_instance_count
        max_concurrency = self.max_concurrency
        max_age_seconds = self.max_age_seconds
        default_max_retries = self.default_max_retries
        project_url = self.project_url
        log_query = self.log_query
        logs_url = self.logs_url
        links: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        run_environment: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.run_environment, Unset):
            run_environment = self.run_environment.to_dict() if self.run_environment else None

        execution_method_capability: Union[Dict[str, Any], Unset]
        if isinstance(self.execution_method_capability, Unset):
            execution_method_capability = UNSET

        elif isinstance(self.execution_method_capability, AwsEcsExecutionMethodCapability):
            execution_method_capability = self.execution_method_capability.to_dict()

        else:
            execution_method_capability = self.execution_method_capability.to_dict()

        alert_methods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.alert_methods, Unset):
            alert_methods = []
            for alert_methods_item_data in self.alert_methods:
                alert_methods_item = alert_methods_item_data.to_dict()

                alert_methods.append(alert_methods_item)

        other_metadata: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.other_metadata, Unset):
            other_metadata = self.other_metadata.to_dict() if self.other_metadata else None

        latest_task_execution: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.latest_task_execution, Unset):
            latest_task_execution = self.latest_task_execution.to_dict() if self.latest_task_execution else None

        current_service_info: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.current_service_info, Unset):
            current_service_info = self.current_service_info.to_dict() if self.current_service_info else None

        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        was_auto_created = self.was_auto_created
        passive = self.passive
        enabled = self.enabled
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
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if infrastructure_website_url is not UNSET:
            field_dict["infrastructure_website_url"] = infrastructure_website_url
        if max_manual_start_delay_before_alert_seconds is not UNSET:
            field_dict["max_manual_start_delay_before_alert_seconds"] = max_manual_start_delay_before_alert_seconds
        if max_manual_start_delay_before_abandonment_seconds is not UNSET:
            field_dict[
                "max_manual_start_delay_before_abandonment_seconds"
            ] = max_manual_start_delay_before_abandonment_seconds
        if heartbeat_interval_seconds is not UNSET:
            field_dict["heartbeat_interval_seconds"] = heartbeat_interval_seconds
        if max_heartbeat_lateness_before_alert_seconds is not UNSET:
            field_dict["max_heartbeat_lateness_before_alert_seconds"] = max_heartbeat_lateness_before_alert_seconds
        if max_heartbeat_lateness_before_abandonment_seconds is not UNSET:
            field_dict[
                "max_heartbeat_lateness_before_abandonment_seconds"
            ] = max_heartbeat_lateness_before_abandonment_seconds
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if scheduled_instance_count is not UNSET:
            field_dict["scheduled_instance_count"] = scheduled_instance_count
        if is_service is not UNSET:
            field_dict["is_service"] = is_service
        if service_instance_count is not UNSET:
            field_dict["service_instance_count"] = service_instance_count
        if min_service_instance_count is not UNSET:
            field_dict["min_service_instance_count"] = min_service_instance_count
        if max_concurrency is not UNSET:
            field_dict["max_concurrency"] = max_concurrency
        if max_age_seconds is not UNSET:
            field_dict["max_age_seconds"] = max_age_seconds
        if default_max_retries is not UNSET:
            field_dict["default_max_retries"] = default_max_retries
        if project_url is not UNSET:
            field_dict["project_url"] = project_url
        if log_query is not UNSET:
            field_dict["log_query"] = log_query
        if logs_url is not UNSET:
            field_dict["logs_url"] = logs_url
        if links is not UNSET:
            field_dict["links"] = links
        if run_environment is not UNSET:
            field_dict["run_environment"] = run_environment
        if execution_method_capability is not UNSET:
            field_dict["execution_method_capability"] = execution_method_capability
        if alert_methods is not UNSET:
            field_dict["alert_methods"] = alert_methods
        if other_metadata is not UNSET:
            field_dict["other_metadata"] = other_metadata
        if latest_task_execution is not UNSET:
            field_dict["latest_task_execution"] = latest_task_execution
        if current_service_info is not UNSET:
            field_dict["current_service_info"] = current_service_info
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if was_auto_created is not UNSET:
            field_dict["was_auto_created"] = was_auto_created
        if passive is not UNSET:
            field_dict["passive"] = passive
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
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

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        infrastructure_website_url = d.pop("infrastructure_website_url", UNSET)

        max_manual_start_delay_before_alert_seconds = d.pop("max_manual_start_delay_before_alert_seconds", UNSET)

        max_manual_start_delay_before_abandonment_seconds = d.pop(
            "max_manual_start_delay_before_abandonment_seconds", UNSET
        )

        heartbeat_interval_seconds = d.pop("heartbeat_interval_seconds", UNSET)

        max_heartbeat_lateness_before_alert_seconds = d.pop("max_heartbeat_lateness_before_alert_seconds", UNSET)

        max_heartbeat_lateness_before_abandonment_seconds = d.pop(
            "max_heartbeat_lateness_before_abandonment_seconds", UNSET
        )

        schedule = d.pop("schedule", UNSET)

        scheduled_instance_count = d.pop("scheduled_instance_count", UNSET)

        is_service = d.pop("is_service", UNSET)

        service_instance_count = d.pop("service_instance_count", UNSET)

        min_service_instance_count = d.pop("min_service_instance_count", UNSET)

        max_concurrency = d.pop("max_concurrency", UNSET)

        max_age_seconds = d.pop("max_age_seconds", UNSET)

        default_max_retries = d.pop("default_max_retries", UNSET)

        project_url = d.pop("project_url", UNSET)

        log_query = d.pop("log_query", UNSET)

        logs_url = d.pop("logs_url", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for links_item_data in _links or []:
            links_item = Link.from_dict(links_item_data)

            links.append(links_item)

        _run_environment = d.pop("run_environment", UNSET)
        run_environment: Union[Unset, None, NameAndUuid]
        if _run_environment is None:
            run_environment = None
        elif isinstance(_run_environment, Unset):
            run_environment = UNSET
        else:
            run_environment = NameAndUuid.from_dict(_run_environment)

        def _parse_execution_method_capability(
            data: object,
        ) -> Union[AwsEcsExecutionMethodCapability, UnknownExecutionMethodCapability, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_execution_method_capability_type_0 = AwsEcsExecutionMethodCapability.from_dict(data)

                return componentsschemas_execution_method_capability_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_execution_method_capability_type_1 = UnknownExecutionMethodCapability.from_dict(data)

            return componentsschemas_execution_method_capability_type_1

        execution_method_capability = _parse_execution_method_capability(d.pop("execution_method_capability", UNSET))

        alert_methods = []
        _alert_methods = d.pop("alert_methods", UNSET)
        for alert_methods_item_data in _alert_methods or []:
            alert_methods_item = NameAndUuid.from_dict(alert_methods_item_data)

            alert_methods.append(alert_methods_item)

        _other_metadata = d.pop("other_metadata", UNSET)
        other_metadata: Union[Unset, None, PatchedTaskOtherMetadata]
        if _other_metadata is None:
            other_metadata = None
        elif isinstance(_other_metadata, Unset):
            other_metadata = UNSET
        else:
            other_metadata = PatchedTaskOtherMetadata.from_dict(_other_metadata)

        _latest_task_execution = d.pop("latest_task_execution", UNSET)
        latest_task_execution: Union[Unset, None, TaskExecution]
        if _latest_task_execution is None:
            latest_task_execution = None
        elif isinstance(_latest_task_execution, Unset):
            latest_task_execution = UNSET
        else:
            latest_task_execution = TaskExecution.from_dict(_latest_task_execution)

        _current_service_info = d.pop("current_service_info", UNSET)
        current_service_info: Union[Unset, None, CurrentServiceInfo]
        if _current_service_info is None:
            current_service_info = None
        elif isinstance(_current_service_info, Unset):
            current_service_info = UNSET
        else:
            current_service_info = CurrentServiceInfo.from_dict(_current_service_info)

        created_by_user = d.pop("created_by_user", UNSET)

        _created_by_group = d.pop("created_by_group", UNSET)
        created_by_group: Union[Unset, Group]
        if isinstance(_created_by_group, Unset):
            created_by_group = UNSET
        else:
            created_by_group = Group.from_dict(_created_by_group)

        was_auto_created = d.pop("was_auto_created", UNSET)

        passive = d.pop("passive", UNSET)

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

        patched_task = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            dashboard_url=dashboard_url,
            infrastructure_website_url=infrastructure_website_url,
            max_manual_start_delay_before_alert_seconds=max_manual_start_delay_before_alert_seconds,
            max_manual_start_delay_before_abandonment_seconds=max_manual_start_delay_before_abandonment_seconds,
            heartbeat_interval_seconds=heartbeat_interval_seconds,
            max_heartbeat_lateness_before_alert_seconds=max_heartbeat_lateness_before_alert_seconds,
            max_heartbeat_lateness_before_abandonment_seconds=max_heartbeat_lateness_before_abandonment_seconds,
            schedule=schedule,
            scheduled_instance_count=scheduled_instance_count,
            is_service=is_service,
            service_instance_count=service_instance_count,
            min_service_instance_count=min_service_instance_count,
            max_concurrency=max_concurrency,
            max_age_seconds=max_age_seconds,
            default_max_retries=default_max_retries,
            project_url=project_url,
            log_query=log_query,
            logs_url=logs_url,
            links=links,
            run_environment=run_environment,
            execution_method_capability=execution_method_capability,
            alert_methods=alert_methods,
            other_metadata=other_metadata,
            latest_task_execution=latest_task_execution,
            current_service_info=current_service_info,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            was_auto_created=was_auto_created,
            passive=passive,
            enabled=enabled,
            created_at=created_at,
            updated_at=updated_at,
        )

        patched_task.additional_properties = d
        return patched_task

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
