import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.alert_method_method_details import AlertMethodMethodDetails
from ..models.group import Group
from ..models.name_and_uuid import NameAndUuid
from ..models.notification_severity import NotificationSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlertMethod")


@attr.s(auto_attribs=True)
class AlertMethod:
    """An AlertMethod specifies one or more configured methods of notifying
    users or external sources of events that trigger when one or more
    conditions are satisfied.

        Attributes:
            name (str):
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            description (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            enabled (Union[Unset, bool]):
            method_details (Union[Unset, AlertMethodMethodDetails]):
            notify_on_success (Union[Unset, bool]):
            notify_on_failure (Union[Unset, bool]):
            notify_on_timeout (Union[Unset, bool]):
            error_severity_on_missing_execution (Union[Unset, NotificationSeverity]):
            error_severity_on_missing_heartbeat (Union[Unset, NotificationSeverity]):
            error_severity_on_service_down (Union[Unset, NotificationSeverity]):
            created_by_user (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
            created_by_group (Union[Unset, Group]):
            run_environment (Union[Unset, None, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    name: str
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    method_details: Union[Unset, AlertMethodMethodDetails] = UNSET
    notify_on_success: Union[Unset, bool] = UNSET
    notify_on_failure: Union[Unset, bool] = UNSET
    notify_on_timeout: Union[Unset, bool] = UNSET
    error_severity_on_missing_execution: Union[Unset, NotificationSeverity] = UNSET
    error_severity_on_missing_heartbeat: Union[Unset, NotificationSeverity] = UNSET
    error_severity_on_service_down: Union[Unset, NotificationSeverity] = UNSET
    created_by_user: Union[Unset, str] = UNSET
    created_by_group: Union[Unset, Group] = UNSET
    run_environment: Union[Unset, None, NameAndUuid] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        url = self.url
        uuid = self.uuid
        description = self.description
        dashboard_url = self.dashboard_url
        enabled = self.enabled
        method_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.method_details, Unset):
            method_details = self.method_details.to_dict()

        notify_on_success = self.notify_on_success
        notify_on_failure = self.notify_on_failure
        notify_on_timeout = self.notify_on_timeout
        error_severity_on_missing_execution: Union[Unset, str] = UNSET
        if not isinstance(self.error_severity_on_missing_execution, Unset):
            error_severity_on_missing_execution = self.error_severity_on_missing_execution.value

        error_severity_on_missing_heartbeat: Union[Unset, str] = UNSET
        if not isinstance(self.error_severity_on_missing_heartbeat, Unset):
            error_severity_on_missing_heartbeat = self.error_severity_on_missing_heartbeat.value

        error_severity_on_service_down: Union[Unset, str] = UNSET
        if not isinstance(self.error_severity_on_service_down, Unset):
            error_severity_on_service_down = self.error_severity_on_service_down.value

        created_by_user = self.created_by_user
        created_by_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.created_by_group, Unset):
            created_by_group = self.created_by_group.to_dict()

        run_environment: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.run_environment, Unset):
            run_environment = self.run_environment.to_dict() if self.run_environment else None

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

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
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if method_details is not UNSET:
            field_dict["method_details"] = method_details
        if notify_on_success is not UNSET:
            field_dict["notify_on_success"] = notify_on_success
        if notify_on_failure is not UNSET:
            field_dict["notify_on_failure"] = notify_on_failure
        if notify_on_timeout is not UNSET:
            field_dict["notify_on_timeout"] = notify_on_timeout
        if error_severity_on_missing_execution is not UNSET:
            field_dict["error_severity_on_missing_execution"] = error_severity_on_missing_execution
        if error_severity_on_missing_heartbeat is not UNSET:
            field_dict["error_severity_on_missing_heartbeat"] = error_severity_on_missing_heartbeat
        if error_severity_on_service_down is not UNSET:
            field_dict["error_severity_on_service_down"] = error_severity_on_service_down
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if created_by_group is not UNSET:
            field_dict["created_by_group"] = created_by_group
        if run_environment is not UNSET:
            field_dict["run_environment"] = run_environment
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        enabled = d.pop("enabled", UNSET)

        _method_details = d.pop("method_details", UNSET)
        method_details: Union[Unset, AlertMethodMethodDetails]
        if isinstance(_method_details, Unset):
            method_details = UNSET
        else:
            method_details = AlertMethodMethodDetails.from_dict(_method_details)

        notify_on_success = d.pop("notify_on_success", UNSET)

        notify_on_failure = d.pop("notify_on_failure", UNSET)

        notify_on_timeout = d.pop("notify_on_timeout", UNSET)

        _error_severity_on_missing_execution = d.pop("error_severity_on_missing_execution", UNSET)
        error_severity_on_missing_execution: Union[Unset, NotificationSeverity]
        if isinstance(_error_severity_on_missing_execution, Unset):
            error_severity_on_missing_execution = UNSET
        else:
            error_severity_on_missing_execution = NotificationSeverity(_error_severity_on_missing_execution)

        _error_severity_on_missing_heartbeat = d.pop("error_severity_on_missing_heartbeat", UNSET)
        error_severity_on_missing_heartbeat: Union[Unset, NotificationSeverity]
        if isinstance(_error_severity_on_missing_heartbeat, Unset):
            error_severity_on_missing_heartbeat = UNSET
        else:
            error_severity_on_missing_heartbeat = NotificationSeverity(_error_severity_on_missing_heartbeat)

        _error_severity_on_service_down = d.pop("error_severity_on_service_down", UNSET)
        error_severity_on_service_down: Union[Unset, NotificationSeverity]
        if isinstance(_error_severity_on_service_down, Unset):
            error_severity_on_service_down = UNSET
        else:
            error_severity_on_service_down = NotificationSeverity(_error_severity_on_service_down)

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

        alert_method = cls(
            name=name,
            url=url,
            uuid=uuid,
            description=description,
            dashboard_url=dashboard_url,
            enabled=enabled,
            method_details=method_details,
            notify_on_success=notify_on_success,
            notify_on_failure=notify_on_failure,
            notify_on_timeout=notify_on_timeout,
            error_severity_on_missing_execution=error_severity_on_missing_execution,
            error_severity_on_missing_heartbeat=error_severity_on_missing_heartbeat,
            error_severity_on_service_down=error_severity_on_service_down,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            run_environment=run_environment,
            created_at=created_at,
            updated_at=updated_at,
        )

        alert_method.additional_properties = d
        return alert_method

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
