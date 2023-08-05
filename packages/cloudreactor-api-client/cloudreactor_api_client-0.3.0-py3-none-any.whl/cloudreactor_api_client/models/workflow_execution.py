import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.name_and_uuid import NameAndUuid
from ..models.workflow_execution_run_reason import WorkflowExecutionRunReason
from ..models.workflow_execution_status import WorkflowExecutionStatus
from ..models.workflow_execution_stop_reason import WorkflowExecutionStopReason
from ..models.workflow_execution_workflow_snapshot import WorkflowExecutionWorkflowSnapshot
from ..models.workflow_task_instance_execution import WorkflowTaskInstanceExecution
from ..models.workflow_transition_evaluation import WorkflowTransitionEvaluation
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowExecution")


@attr.s(auto_attribs=True)
class WorkflowExecution:
    """A WorkflowExecution holds data on a specific execution (run) of a Workflow.

    Attributes:
        workflow (NameAndUuid): Identifies an entity in three ways: 1. UUID; 2. Name; and 3. URL.
            When used to indentify an entity in a request method body, only one of
            uuid and name needs to be specified. If both are present, they must
            refer to the same entity or else the response will be a 400 error.
        status (WorkflowExecutionStatus):
        url (Union[Unset, str]):
        uuid (Union[Unset, str]):
        dashboard_url (Union[Unset, str]):
        run_reason (Union[Unset, WorkflowExecutionRunReason]):
        started_at (Union[Unset, datetime.datetime]):
        started_by (Union[Unset, None, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        finished_at (Union[Unset, None, datetime.datetime]):
        last_heartbeat_at (Union[Unset, None, datetime.datetime]):
        stop_reason (Union[Unset, WorkflowExecutionStopReason]):
        marked_done_at (Union[Unset, None, datetime.datetime]):
        marked_done_by (Union[Unset, None, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        kill_started_at (Union[Unset, None, datetime.datetime]):
        killed_by (Union[Unset, None, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        kill_finished_at (Union[Unset, None, datetime.datetime]):
        kill_error_code (Union[Unset, None, int]):
        failed_attempts (Union[Unset, int]):
        timed_out_attempts (Union[Unset, int]):
        workflow_snapshot (Union[Unset, WorkflowExecutionWorkflowSnapshot]):
        workflow_task_instance_executions (Union[Unset, List[WorkflowTaskInstanceExecution]]):
        workflow_transition_evaluations (Union[Unset, List[WorkflowTransitionEvaluation]]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    workflow: NameAndUuid
    status: WorkflowExecutionStatus
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    run_reason: Union[Unset, WorkflowExecutionRunReason] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    started_by: Union[Unset, None, str] = UNSET
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    last_heartbeat_at: Union[Unset, None, datetime.datetime] = UNSET
    stop_reason: Union[Unset, WorkflowExecutionStopReason] = UNSET
    marked_done_at: Union[Unset, None, datetime.datetime] = UNSET
    marked_done_by: Union[Unset, None, str] = UNSET
    kill_started_at: Union[Unset, None, datetime.datetime] = UNSET
    killed_by: Union[Unset, None, str] = UNSET
    kill_finished_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_error_code: Union[Unset, None, int] = UNSET
    failed_attempts: Union[Unset, int] = UNSET
    timed_out_attempts: Union[Unset, int] = UNSET
    workflow_snapshot: Union[Unset, WorkflowExecutionWorkflowSnapshot] = UNSET
    workflow_task_instance_executions: Union[Unset, List[WorkflowTaskInstanceExecution]] = UNSET
    workflow_transition_evaluations: Union[Unset, List[WorkflowTransitionEvaluation]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow = self.workflow.to_dict()

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

        started_by = self.started_by
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

        marked_done_by = self.marked_done_by
        kill_started_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_started_at, Unset):
            kill_started_at = self.kill_started_at.isoformat() if self.kill_started_at else None

        killed_by = self.killed_by
        kill_finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_finished_at, Unset):
            kill_finished_at = self.kill_finished_at.isoformat() if self.kill_finished_at else None

        kill_error_code = self.kill_error_code
        failed_attempts = self.failed_attempts
        timed_out_attempts = self.timed_out_attempts
        workflow_snapshot: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_snapshot, Unset):
            workflow_snapshot = self.workflow_snapshot.to_dict()

        workflow_task_instance_executions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_task_instance_executions, Unset):
            workflow_task_instance_executions = []
            for workflow_task_instance_executions_item_data in self.workflow_task_instance_executions:
                workflow_task_instance_executions_item = workflow_task_instance_executions_item_data.to_dict()

                workflow_task_instance_executions.append(workflow_task_instance_executions_item)

        workflow_transition_evaluations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workflow_transition_evaluations, Unset):
            workflow_transition_evaluations = []
            for workflow_transition_evaluations_item_data in self.workflow_transition_evaluations:
                workflow_transition_evaluations_item = workflow_transition_evaluations_item_data.to_dict()

                workflow_transition_evaluations.append(workflow_transition_evaluations_item)

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
                "workflow": workflow,
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
        if started_by is not UNSET:
            field_dict["started_by"] = started_by
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if last_heartbeat_at is not UNSET:
            field_dict["last_heartbeat_at"] = last_heartbeat_at
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if marked_done_at is not UNSET:
            field_dict["marked_done_at"] = marked_done_at
        if marked_done_by is not UNSET:
            field_dict["marked_done_by"] = marked_done_by
        if kill_started_at is not UNSET:
            field_dict["kill_started_at"] = kill_started_at
        if killed_by is not UNSET:
            field_dict["killed_by"] = killed_by
        if kill_finished_at is not UNSET:
            field_dict["kill_finished_at"] = kill_finished_at
        if kill_error_code is not UNSET:
            field_dict["kill_error_code"] = kill_error_code
        if failed_attempts is not UNSET:
            field_dict["failed_attempts"] = failed_attempts
        if timed_out_attempts is not UNSET:
            field_dict["timed_out_attempts"] = timed_out_attempts
        if workflow_snapshot is not UNSET:
            field_dict["workflow_snapshot"] = workflow_snapshot
        if workflow_task_instance_executions is not UNSET:
            field_dict["workflow_task_instance_executions"] = workflow_task_instance_executions
        if workflow_transition_evaluations is not UNSET:
            field_dict["workflow_transition_evaluations"] = workflow_transition_evaluations
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow = NameAndUuid.from_dict(d.pop("workflow"))

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

        started_by = d.pop("started_by", UNSET)

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

        marked_done_by = d.pop("marked_done_by", UNSET)

        _kill_started_at = d.pop("kill_started_at", UNSET)
        kill_started_at: Union[Unset, None, datetime.datetime]
        if _kill_started_at is None:
            kill_started_at = None
        elif isinstance(_kill_started_at, Unset):
            kill_started_at = UNSET
        else:
            kill_started_at = isoparse(_kill_started_at)

        killed_by = d.pop("killed_by", UNSET)

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

        _workflow_snapshot = d.pop("workflow_snapshot", UNSET)
        workflow_snapshot: Union[Unset, WorkflowExecutionWorkflowSnapshot]
        if isinstance(_workflow_snapshot, Unset):
            workflow_snapshot = UNSET
        else:
            workflow_snapshot = WorkflowExecutionWorkflowSnapshot.from_dict(_workflow_snapshot)

        workflow_task_instance_executions = []
        _workflow_task_instance_executions = d.pop("workflow_task_instance_executions", UNSET)
        for workflow_task_instance_executions_item_data in _workflow_task_instance_executions or []:
            workflow_task_instance_executions_item = WorkflowTaskInstanceExecution.from_dict(
                workflow_task_instance_executions_item_data
            )

            workflow_task_instance_executions.append(workflow_task_instance_executions_item)

        workflow_transition_evaluations = []
        _workflow_transition_evaluations = d.pop("workflow_transition_evaluations", UNSET)
        for workflow_transition_evaluations_item_data in _workflow_transition_evaluations or []:
            workflow_transition_evaluations_item = WorkflowTransitionEvaluation.from_dict(
                workflow_transition_evaluations_item_data
            )

            workflow_transition_evaluations.append(workflow_transition_evaluations_item)

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

        workflow_execution = cls(
            workflow=workflow,
            status=status,
            url=url,
            uuid=uuid,
            dashboard_url=dashboard_url,
            run_reason=run_reason,
            started_at=started_at,
            started_by=started_by,
            finished_at=finished_at,
            last_heartbeat_at=last_heartbeat_at,
            stop_reason=stop_reason,
            marked_done_at=marked_done_at,
            marked_done_by=marked_done_by,
            kill_started_at=kill_started_at,
            killed_by=killed_by,
            kill_finished_at=kill_finished_at,
            kill_error_code=kill_error_code,
            failed_attempts=failed_attempts,
            timed_out_attempts=timed_out_attempts,
            workflow_snapshot=workflow_snapshot,
            workflow_task_instance_executions=workflow_task_instance_executions,
            workflow_transition_evaluations=workflow_transition_evaluations,
            created_at=created_at,
            updated_at=updated_at,
        )

        workflow_execution.additional_properties = d
        return workflow_execution

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
