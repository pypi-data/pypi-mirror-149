import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.workflow_execution_run_reason import WorkflowExecutionRunReason
from ..models.workflow_execution_status import WorkflowExecutionStatus
from ..models.workflow_execution_stop_reason import WorkflowExecutionStopReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowExecutionSummary")


@attr.s(auto_attribs=True)
class WorkflowExecutionSummary:
    """A WorkflowExecutionSummary contains a subset of the data inside of a
    WorkflowExecution.

        Attributes:
            status (WorkflowExecutionStatus):
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            dashboard_url (Union[Unset, str]):
            run_reason (Union[Unset, WorkflowExecutionRunReason]):
            started_at (Union[Unset, datetime.datetime]):
            finished_at (Union[Unset, None, datetime.datetime]):
            last_heartbeat_at (Union[Unset, None, datetime.datetime]):
            stop_reason (Union[Unset, WorkflowExecutionStopReason]):
            marked_done_at (Union[Unset, None, datetime.datetime]):
            kill_started_at (Union[Unset, None, datetime.datetime]):
            kill_finished_at (Union[Unset, None, datetime.datetime]):
            kill_error_code (Union[Unset, None, int]):
            failed_attempts (Union[Unset, int]):
            timed_out_attempts (Union[Unset, int]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    status: WorkflowExecutionStatus
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    run_reason: Union[Unset, WorkflowExecutionRunReason] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    last_heartbeat_at: Union[Unset, None, datetime.datetime] = UNSET
    stop_reason: Union[Unset, WorkflowExecutionStopReason] = UNSET
    marked_done_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_started_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_finished_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_error_code: Union[Unset, None, int] = UNSET
    failed_attempts: Union[Unset, int] = UNSET
    timed_out_attempts: Union[Unset, int] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        url = self.url
        uuid = self.uuid
        dashboard_url = self.dashboard_url
        run_reason: Union[Unset, str] = UNSET
        if not isinstance(self.run_reason, Unset):
            run_reason = self.run_reason.value

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat() if self.finished_at else None

        last_heartbeat_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_heartbeat_at, Unset):
            last_heartbeat_at = self.last_heartbeat_at.isoformat() if self.last_heartbeat_at else None

        stop_reason: Union[Unset, str] = UNSET
        if not isinstance(self.stop_reason, Unset):
            stop_reason = self.stop_reason.value

        marked_done_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.marked_done_at, Unset):
            marked_done_at = self.marked_done_at.isoformat() if self.marked_done_at else None

        kill_started_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_started_at, Unset):
            kill_started_at = self.kill_started_at.isoformat() if self.kill_started_at else None

        kill_finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_finished_at, Unset):
            kill_finished_at = self.kill_finished_at.isoformat() if self.kill_finished_at else None

        kill_error_code = self.kill_error_code
        failed_attempts = self.failed_attempts
        timed_out_attempts = self.timed_out_attempts
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
                "status": status,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if dashboard_url is not UNSET:
            field_dict["dashboard_url"] = dashboard_url
        if run_reason is not UNSET:
            field_dict["run_reason"] = run_reason
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if last_heartbeat_at is not UNSET:
            field_dict["last_heartbeat_at"] = last_heartbeat_at
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if marked_done_at is not UNSET:
            field_dict["marked_done_at"] = marked_done_at
        if kill_started_at is not UNSET:
            field_dict["kill_started_at"] = kill_started_at
        if kill_finished_at is not UNSET:
            field_dict["kill_finished_at"] = kill_finished_at
        if kill_error_code is not UNSET:
            field_dict["kill_error_code"] = kill_error_code
        if failed_attempts is not UNSET:
            field_dict["failed_attempts"] = failed_attempts
        if timed_out_attempts is not UNSET:
            field_dict["timed_out_attempts"] = timed_out_attempts
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = WorkflowExecutionStatus(d.pop("status"))

        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        _run_reason = d.pop("run_reason", UNSET)
        run_reason: Union[Unset, WorkflowExecutionRunReason]
        if isinstance(_run_reason, Unset):
            run_reason = UNSET
        else:
            run_reason = WorkflowExecutionRunReason(_run_reason)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _finished_at = d.pop("finished_at", UNSET)
        finished_at: Union[Unset, None, datetime.datetime]
        if _finished_at is None:
            finished_at = None
        elif isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        _last_heartbeat_at = d.pop("last_heartbeat_at", UNSET)
        last_heartbeat_at: Union[Unset, None, datetime.datetime]
        if _last_heartbeat_at is None:
            last_heartbeat_at = None
        elif isinstance(_last_heartbeat_at, Unset):
            last_heartbeat_at = UNSET
        else:
            last_heartbeat_at = isoparse(_last_heartbeat_at)

        _stop_reason = d.pop("stop_reason", UNSET)
        stop_reason: Union[Unset, WorkflowExecutionStopReason]
        if isinstance(_stop_reason, Unset):
            stop_reason = UNSET
        else:
            stop_reason = WorkflowExecutionStopReason(_stop_reason)

        _marked_done_at = d.pop("marked_done_at", UNSET)
        marked_done_at: Union[Unset, None, datetime.datetime]
        if _marked_done_at is None:
            marked_done_at = None
        elif isinstance(_marked_done_at, Unset):
            marked_done_at = UNSET
        else:
            marked_done_at = isoparse(_marked_done_at)

        _kill_started_at = d.pop("kill_started_at", UNSET)
        kill_started_at: Union[Unset, None, datetime.datetime]
        if _kill_started_at is None:
            kill_started_at = None
        elif isinstance(_kill_started_at, Unset):
            kill_started_at = UNSET
        else:
            kill_started_at = isoparse(_kill_started_at)

        _kill_finished_at = d.pop("kill_finished_at", UNSET)
        kill_finished_at: Union[Unset, None, datetime.datetime]
        if _kill_finished_at is None:
            kill_finished_at = None
        elif isinstance(_kill_finished_at, Unset):
            kill_finished_at = UNSET
        else:
            kill_finished_at = isoparse(_kill_finished_at)

        kill_error_code = d.pop("kill_error_code", UNSET)

        failed_attempts = d.pop("failed_attempts", UNSET)

        timed_out_attempts = d.pop("timed_out_attempts", UNSET)

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

        workflow_execution_summary = cls(
            status=status,
            url=url,
            uuid=uuid,
            dashboard_url=dashboard_url,
            run_reason=run_reason,
            started_at=started_at,
            finished_at=finished_at,
            last_heartbeat_at=last_heartbeat_at,
            stop_reason=stop_reason,
            marked_done_at=marked_done_at,
            kill_started_at=kill_started_at,
            kill_finished_at=kill_finished_at,
            kill_error_code=kill_error_code,
            failed_attempts=failed_attempts,
            timed_out_attempts=timed_out_attempts,
            created_at=created_at,
            updated_at=updated_at,
        )

        workflow_execution_summary.additional_properties = d
        return workflow_execution_summary

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
