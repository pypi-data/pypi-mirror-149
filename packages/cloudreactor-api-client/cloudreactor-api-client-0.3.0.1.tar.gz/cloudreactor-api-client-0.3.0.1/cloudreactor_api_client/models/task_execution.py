import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.aws_ecs_execution_method import AwsEcsExecutionMethod
from ..models.name_and_uuid import NameAndUuid
from ..models.stop_reason_enum import StopReasonEnum
from ..models.task_execution_environment_variables_overrides import TaskExecutionEnvironmentVariablesOverrides
from ..models.task_execution_other_instance_metadata import TaskExecutionOtherInstanceMetadata
from ..models.task_execution_other_runtime_metadata import TaskExecutionOtherRuntimeMetadata
from ..models.task_execution_status import TaskExecutionStatus
from ..models.workflow_task_instance_execution_base import WorkflowTaskInstanceExecutionBase
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskExecution")


@attr.s(auto_attribs=True)
class TaskExecution:
    """A Task Execution is an execution / run instance of a Task.

    Attributes:
        status (TaskExecutionStatus):
        url (Union[Unset, str]):
        uuid (Union[Unset, str]):
        dashboard_url (Union[Unset, str]):
        infrastructure_website_url (Union[Unset, None, str]):
        task (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3. URL.
            When used to indentify an entity in a request method body, only one of
            uuid and name needs to be specified. If both are present, they must
            refer to the same entity or else the response will be a 400 error.
        task_version_number (Union[Unset, None, int]):
        task_version_text (Union[Unset, None, str]):
        task_version_signature (Union[Unset, None, str]):
        commit_url (Union[Unset, None, str]):
        other_instance_metadata (Union[Unset, None, TaskExecutionOtherInstanceMetadata]):
        hostname (Union[Unset, None, str]):
        environment_variables_overrides (Union[Unset, None, TaskExecutionEnvironmentVariablesOverrides]):
        execution_method (Union[Unset, AwsEcsExecutionMethod]): AwsEcsExecutionMethods contain configuration for running
            Tasks in
            AWS ECS.
        started_by (Union[Unset, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        started_at (Union[Unset, datetime.datetime]):
        finished_at (Union[Unset, None, datetime.datetime]):
        marked_done_by (Union[Unset, None, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        marked_done_at (Union[Unset, None, datetime.datetime]):
        marked_outdated_at (Union[Unset, None, datetime.datetime]):
        killed_by (Union[Unset, None, str]): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        kill_started_at (Union[Unset, None, datetime.datetime]):
        kill_finished_at (Union[Unset, None, datetime.datetime]):
        kill_error_code (Union[Unset, None, int]):
        stop_reason (Union[Unset, None, StopReasonEnum]):
        last_heartbeat_at (Union[Unset, None, datetime.datetime]):
        failed_attempts (Union[Unset, int]):
        timed_out_attempts (Union[Unset, int]):
        exit_code (Union[Unset, None, int]):
        last_status_message (Union[Unset, None, str]):
        error_count (Union[Unset, None, int]):
        skipped_count (Union[Unset, None, int]):
        expected_count (Union[Unset, None, int]):
        success_count (Union[Unset, None, int]):
        other_runtime_metadata (Union[Unset, None, TaskExecutionOtherRuntimeMetadata]):
        current_cpu_units (Union[Unset, None, int]):
        mean_cpu_units (Union[Unset, None, int]):
        max_cpu_units (Union[Unset, None, int]):
        current_memory_mb (Union[Unset, None, int]):
        mean_memory_mb (Union[Unset, None, int]):
        max_memory_mb (Union[Unset, None, int]):
        wrapper_version (Union[Unset, None, str]):
        wrapper_log_level (Union[Unset, None, str]):
        deployment (Union[Unset, None, str]):
        process_command (Union[Unset, None, str]):
        is_service (Union[Unset, None, bool]):
        task_max_concurrency (Union[Unset, None, int]):
        max_conflicting_age_seconds (Union[Unset, None, int]):
        prevent_offline_execution (Union[Unset, None, bool]):
        process_timeout_seconds (Union[Unset, None, int]):
        process_termination_grace_period_seconds (Union[Unset, None, int]):
        process_max_retries (Union[Unset, None, int]):
        process_retry_delay_seconds (Union[Unset, None, int]):
        schedule (Union[Unset, None, str]):
        heartbeat_interval_seconds (Union[Unset, None, int]):
        workflow_task_instance_execution (Union[Unset, None, WorkflowTaskInstanceExecutionBase]):
            WorkflowTaskInstanceExecutions hold the execution information
            for a WorkflowTaskInstance (which holds a Task) for a specific
            WorkflowExection (run of a Workflow).
        api_base_url (Union[Unset, str]):
        api_request_timeout_seconds (Union[Unset, None, int]):
        api_retry_delay_seconds (Union[Unset, None, int]):
        api_resume_delay_seconds (Union[Unset, None, int]):
        api_error_timeout_seconds (Union[Unset, None, int]):
        api_task_execution_creation_error_timeout_seconds (Union[Unset, None, int]):
        api_task_execution_creation_conflict_timeout_seconds (Union[Unset, None, int]):
        api_task_execution_creation_conflict_retry_delay_seconds (Union[Unset, None, int]):
        api_final_update_timeout_seconds (Union[Unset, None, int]):
        status_update_interval_seconds (Union[Unset, None, int]):
        status_update_port (Union[Unset, None, int]):
        status_update_message_max_bytes (Union[Unset, None, int]):
        debug_log_tail (Union[Unset, None, str]):
        error_log_tail (Union[Unset, None, str]):
        embedded_mode (Union[Unset, None, bool]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    status: TaskExecutionStatus
    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    dashboard_url: Union[Unset, str] = UNSET
    infrastructure_website_url: Union[Unset, None, str] = UNSET
    task: Union[Unset, NameAndUuid] = UNSET
    task_version_number: Union[Unset, None, int] = UNSET
    task_version_text: Union[Unset, None, str] = UNSET
    task_version_signature: Union[Unset, None, str] = UNSET
    commit_url: Union[Unset, None, str] = UNSET
    other_instance_metadata: Union[Unset, None, TaskExecutionOtherInstanceMetadata] = UNSET
    hostname: Union[Unset, None, str] = UNSET
    environment_variables_overrides: Union[Unset, None, TaskExecutionEnvironmentVariablesOverrides] = UNSET
    execution_method: Union[Unset, AwsEcsExecutionMethod] = UNSET
    started_by: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    marked_done_by: Union[Unset, None, str] = UNSET
    marked_done_at: Union[Unset, None, datetime.datetime] = UNSET
    marked_outdated_at: Union[Unset, None, datetime.datetime] = UNSET
    killed_by: Union[Unset, None, str] = UNSET
    kill_started_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_finished_at: Union[Unset, None, datetime.datetime] = UNSET
    kill_error_code: Union[Unset, None, int] = UNSET
    stop_reason: Union[Unset, None, StopReasonEnum] = UNSET
    last_heartbeat_at: Union[Unset, None, datetime.datetime] = UNSET
    failed_attempts: Union[Unset, int] = UNSET
    timed_out_attempts: Union[Unset, int] = UNSET
    exit_code: Union[Unset, None, int] = UNSET
    last_status_message: Union[Unset, None, str] = UNSET
    error_count: Union[Unset, None, int] = UNSET
    skipped_count: Union[Unset, None, int] = UNSET
    expected_count: Union[Unset, None, int] = UNSET
    success_count: Union[Unset, None, int] = UNSET
    other_runtime_metadata: Union[Unset, None, TaskExecutionOtherRuntimeMetadata] = UNSET
    current_cpu_units: Union[Unset, None, int] = UNSET
    mean_cpu_units: Union[Unset, None, int] = UNSET
    max_cpu_units: Union[Unset, None, int] = UNSET
    current_memory_mb: Union[Unset, None, int] = UNSET
    mean_memory_mb: Union[Unset, None, int] = UNSET
    max_memory_mb: Union[Unset, None, int] = UNSET
    wrapper_version: Union[Unset, None, str] = UNSET
    wrapper_log_level: Union[Unset, None, str] = UNSET
    deployment: Union[Unset, None, str] = UNSET
    process_command: Union[Unset, None, str] = UNSET
    is_service: Union[Unset, None, bool] = UNSET
    task_max_concurrency: Union[Unset, None, int] = UNSET
    max_conflicting_age_seconds: Union[Unset, None, int] = UNSET
    prevent_offline_execution: Union[Unset, None, bool] = UNSET
    process_timeout_seconds: Union[Unset, None, int] = UNSET
    process_termination_grace_period_seconds: Union[Unset, None, int] = UNSET
    process_max_retries: Union[Unset, None, int] = UNSET
    process_retry_delay_seconds: Union[Unset, None, int] = UNSET
    schedule: Union[Unset, None, str] = UNSET
    heartbeat_interval_seconds: Union[Unset, None, int] = UNSET
    workflow_task_instance_execution: Union[Unset, None, WorkflowTaskInstanceExecutionBase] = UNSET
    api_base_url: Union[Unset, str] = UNSET
    api_request_timeout_seconds: Union[Unset, None, int] = UNSET
    api_retry_delay_seconds: Union[Unset, None, int] = UNSET
    api_resume_delay_seconds: Union[Unset, None, int] = UNSET
    api_error_timeout_seconds: Union[Unset, None, int] = UNSET
    api_task_execution_creation_error_timeout_seconds: Union[Unset, None, int] = UNSET
    api_task_execution_creation_conflict_timeout_seconds: Union[Unset, None, int] = UNSET
    api_task_execution_creation_conflict_retry_delay_seconds: Union[Unset, None, int] = UNSET
    api_final_update_timeout_seconds: Union[Unset, None, int] = UNSET
    status_update_interval_seconds: Union[Unset, None, int] = UNSET
    status_update_port: Union[Unset, None, int] = UNSET
    status_update_message_max_bytes: Union[Unset, None, int] = UNSET
    debug_log_tail: Union[Unset, None, str] = UNSET
    error_log_tail: Union[Unset, None, str] = UNSET
    embedded_mode: Union[Unset, None, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        url = self.url
        uuid = self.uuid
        dashboard_url = self.dashboard_url
        infrastructure_website_url = self.infrastructure_website_url
        task: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.task, Unset):
            task = self.task.to_dict()

        task_version_number = self.task_version_number
        task_version_text = self.task_version_text
        task_version_signature = self.task_version_signature
        commit_url = self.commit_url
        other_instance_metadata: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.other_instance_metadata, Unset):
            other_instance_metadata = self.other_instance_metadata.to_dict() if self.other_instance_metadata else None

        hostname = self.hostname
        environment_variables_overrides: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.environment_variables_overrides, Unset):
            environment_variables_overrides = (
                self.environment_variables_overrides.to_dict() if self.environment_variables_overrides else None
            )

        execution_method: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.execution_method, Unset):
            execution_method = self.execution_method.to_dict()

        started_by = self.started_by
        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat() if self.finished_at else None

        marked_done_by = self.marked_done_by
        marked_done_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.marked_done_at, Unset):
            marked_done_at = self.marked_done_at.isoformat() if self.marked_done_at else None

        marked_outdated_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.marked_outdated_at, Unset):
            marked_outdated_at = self.marked_outdated_at.isoformat() if self.marked_outdated_at else None

        killed_by = self.killed_by
        kill_started_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_started_at, Unset):
            kill_started_at = self.kill_started_at.isoformat() if self.kill_started_at else None

        kill_finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.kill_finished_at, Unset):
            kill_finished_at = self.kill_finished_at.isoformat() if self.kill_finished_at else None

        kill_error_code = self.kill_error_code
        stop_reason: Union[Unset, None, str] = UNSET
        if not isinstance(self.stop_reason, Unset):
            stop_reason = self.stop_reason.value if self.stop_reason else None

        last_heartbeat_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_heartbeat_at, Unset):
            last_heartbeat_at = self.last_heartbeat_at.isoformat() if self.last_heartbeat_at else None

        failed_attempts = self.failed_attempts
        timed_out_attempts = self.timed_out_attempts
        exit_code = self.exit_code
        last_status_message = self.last_status_message
        error_count = self.error_count
        skipped_count = self.skipped_count
        expected_count = self.expected_count
        success_count = self.success_count
        other_runtime_metadata: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.other_runtime_metadata, Unset):
            other_runtime_metadata = self.other_runtime_metadata.to_dict() if self.other_runtime_metadata else None

        current_cpu_units = self.current_cpu_units
        mean_cpu_units = self.mean_cpu_units
        max_cpu_units = self.max_cpu_units
        current_memory_mb = self.current_memory_mb
        mean_memory_mb = self.mean_memory_mb
        max_memory_mb = self.max_memory_mb
        wrapper_version = self.wrapper_version
        wrapper_log_level = self.wrapper_log_level
        deployment = self.deployment
        process_command = self.process_command
        is_service = self.is_service
        task_max_concurrency = self.task_max_concurrency
        max_conflicting_age_seconds = self.max_conflicting_age_seconds
        prevent_offline_execution = self.prevent_offline_execution
        process_timeout_seconds = self.process_timeout_seconds
        process_termination_grace_period_seconds = self.process_termination_grace_period_seconds
        process_max_retries = self.process_max_retries
        process_retry_delay_seconds = self.process_retry_delay_seconds
        schedule = self.schedule
        heartbeat_interval_seconds = self.heartbeat_interval_seconds
        workflow_task_instance_execution: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_task_instance_execution, Unset):
            workflow_task_instance_execution = (
                self.workflow_task_instance_execution.to_dict() if self.workflow_task_instance_execution else None
            )

        api_base_url = self.api_base_url
        api_request_timeout_seconds = self.api_request_timeout_seconds
        api_retry_delay_seconds = self.api_retry_delay_seconds
        api_resume_delay_seconds = self.api_resume_delay_seconds
        api_error_timeout_seconds = self.api_error_timeout_seconds
        api_task_execution_creation_error_timeout_seconds = self.api_task_execution_creation_error_timeout_seconds
        api_task_execution_creation_conflict_timeout_seconds = self.api_task_execution_creation_conflict_timeout_seconds
        api_task_execution_creation_conflict_retry_delay_seconds = (
            self.api_task_execution_creation_conflict_retry_delay_seconds
        )
        api_final_update_timeout_seconds = self.api_final_update_timeout_seconds
        status_update_interval_seconds = self.status_update_interval_seconds
        status_update_port = self.status_update_port
        status_update_message_max_bytes = self.status_update_message_max_bytes
        debug_log_tail = self.debug_log_tail
        error_log_tail = self.error_log_tail
        embedded_mode = self.embedded_mode
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
        if infrastructure_website_url is not UNSET:
            field_dict["infrastructure_website_url"] = infrastructure_website_url
        if task is not UNSET:
            field_dict["task"] = task
        if task_version_number is not UNSET:
            field_dict["task_version_number"] = task_version_number
        if task_version_text is not UNSET:
            field_dict["task_version_text"] = task_version_text
        if task_version_signature is not UNSET:
            field_dict["task_version_signature"] = task_version_signature
        if commit_url is not UNSET:
            field_dict["commit_url"] = commit_url
        if other_instance_metadata is not UNSET:
            field_dict["other_instance_metadata"] = other_instance_metadata
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if environment_variables_overrides is not UNSET:
            field_dict["environment_variables_overrides"] = environment_variables_overrides
        if execution_method is not UNSET:
            field_dict["execution_method"] = execution_method
        if started_by is not UNSET:
            field_dict["started_by"] = started_by
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if marked_done_by is not UNSET:
            field_dict["marked_done_by"] = marked_done_by
        if marked_done_at is not UNSET:
            field_dict["marked_done_at"] = marked_done_at
        if marked_outdated_at is not UNSET:
            field_dict["marked_outdated_at"] = marked_outdated_at
        if killed_by is not UNSET:
            field_dict["killed_by"] = killed_by
        if kill_started_at is not UNSET:
            field_dict["kill_started_at"] = kill_started_at
        if kill_finished_at is not UNSET:
            field_dict["kill_finished_at"] = kill_finished_at
        if kill_error_code is not UNSET:
            field_dict["kill_error_code"] = kill_error_code
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if last_heartbeat_at is not UNSET:
            field_dict["last_heartbeat_at"] = last_heartbeat_at
        if failed_attempts is not UNSET:
            field_dict["failed_attempts"] = failed_attempts
        if timed_out_attempts is not UNSET:
            field_dict["timed_out_attempts"] = timed_out_attempts
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if last_status_message is not UNSET:
            field_dict["last_status_message"] = last_status_message
        if error_count is not UNSET:
            field_dict["error_count"] = error_count
        if skipped_count is not UNSET:
            field_dict["skipped_count"] = skipped_count
        if expected_count is not UNSET:
            field_dict["expected_count"] = expected_count
        if success_count is not UNSET:
            field_dict["success_count"] = success_count
        if other_runtime_metadata is not UNSET:
            field_dict["other_runtime_metadata"] = other_runtime_metadata
        if current_cpu_units is not UNSET:
            field_dict["current_cpu_units"] = current_cpu_units
        if mean_cpu_units is not UNSET:
            field_dict["mean_cpu_units"] = mean_cpu_units
        if max_cpu_units is not UNSET:
            field_dict["max_cpu_units"] = max_cpu_units
        if current_memory_mb is not UNSET:
            field_dict["current_memory_mb"] = current_memory_mb
        if mean_memory_mb is not UNSET:
            field_dict["mean_memory_mb"] = mean_memory_mb
        if max_memory_mb is not UNSET:
            field_dict["max_memory_mb"] = max_memory_mb
        if wrapper_version is not UNSET:
            field_dict["wrapper_version"] = wrapper_version
        if wrapper_log_level is not UNSET:
            field_dict["wrapper_log_level"] = wrapper_log_level
        if deployment is not UNSET:
            field_dict["deployment"] = deployment
        if process_command is not UNSET:
            field_dict["process_command"] = process_command
        if is_service is not UNSET:
            field_dict["is_service"] = is_service
        if task_max_concurrency is not UNSET:
            field_dict["task_max_concurrency"] = task_max_concurrency
        if max_conflicting_age_seconds is not UNSET:
            field_dict["max_conflicting_age_seconds"] = max_conflicting_age_seconds
        if prevent_offline_execution is not UNSET:
            field_dict["prevent_offline_execution"] = prevent_offline_execution
        if process_timeout_seconds is not UNSET:
            field_dict["process_timeout_seconds"] = process_timeout_seconds
        if process_termination_grace_period_seconds is not UNSET:
            field_dict["process_termination_grace_period_seconds"] = process_termination_grace_period_seconds
        if process_max_retries is not UNSET:
            field_dict["process_max_retries"] = process_max_retries
        if process_retry_delay_seconds is not UNSET:
            field_dict["process_retry_delay_seconds"] = process_retry_delay_seconds
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if heartbeat_interval_seconds is not UNSET:
            field_dict["heartbeat_interval_seconds"] = heartbeat_interval_seconds
        if workflow_task_instance_execution is not UNSET:
            field_dict["workflow_task_instance_execution"] = workflow_task_instance_execution
        if api_base_url is not UNSET:
            field_dict["api_base_url"] = api_base_url
        if api_request_timeout_seconds is not UNSET:
            field_dict["api_request_timeout_seconds"] = api_request_timeout_seconds
        if api_retry_delay_seconds is not UNSET:
            field_dict["api_retry_delay_seconds"] = api_retry_delay_seconds
        if api_resume_delay_seconds is not UNSET:
            field_dict["api_resume_delay_seconds"] = api_resume_delay_seconds
        if api_error_timeout_seconds is not UNSET:
            field_dict["api_error_timeout_seconds"] = api_error_timeout_seconds
        if api_task_execution_creation_error_timeout_seconds is not UNSET:
            field_dict[
                "api_task_execution_creation_error_timeout_seconds"
            ] = api_task_execution_creation_error_timeout_seconds
        if api_task_execution_creation_conflict_timeout_seconds is not UNSET:
            field_dict[
                "api_task_execution_creation_conflict_timeout_seconds"
            ] = api_task_execution_creation_conflict_timeout_seconds
        if api_task_execution_creation_conflict_retry_delay_seconds is not UNSET:
            field_dict[
                "api_task_execution_creation_conflict_retry_delay_seconds"
            ] = api_task_execution_creation_conflict_retry_delay_seconds
        if api_final_update_timeout_seconds is not UNSET:
            field_dict["api_final_update_timeout_seconds"] = api_final_update_timeout_seconds
        if status_update_interval_seconds is not UNSET:
            field_dict["status_update_interval_seconds"] = status_update_interval_seconds
        if status_update_port is not UNSET:
            field_dict["status_update_port"] = status_update_port
        if status_update_message_max_bytes is not UNSET:
            field_dict["status_update_message_max_bytes"] = status_update_message_max_bytes
        if debug_log_tail is not UNSET:
            field_dict["debug_log_tail"] = debug_log_tail
        if error_log_tail is not UNSET:
            field_dict["error_log_tail"] = error_log_tail
        if embedded_mode is not UNSET:
            field_dict["embedded_mode"] = embedded_mode
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = TaskExecutionStatus(d.pop("status"))

        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        dashboard_url = d.pop("dashboard_url", UNSET)

        infrastructure_website_url = d.pop("infrastructure_website_url", UNSET)

        _task = d.pop("task", UNSET)
        task: Union[Unset, NameAndUuid]
        if isinstance(_task, Unset):
            task = UNSET
        else:
            task = NameAndUuid.from_dict(_task)

        task_version_number = d.pop("task_version_number", UNSET)

        task_version_text = d.pop("task_version_text", UNSET)

        task_version_signature = d.pop("task_version_signature", UNSET)

        commit_url = d.pop("commit_url", UNSET)

        _other_instance_metadata = d.pop("other_instance_metadata", UNSET)
        other_instance_metadata: Union[Unset, None, TaskExecutionOtherInstanceMetadata]
        if _other_instance_metadata is None:
            other_instance_metadata = None
        elif isinstance(_other_instance_metadata, Unset):
            other_instance_metadata = UNSET
        else:
            other_instance_metadata = TaskExecutionOtherInstanceMetadata.from_dict(_other_instance_metadata)

        hostname = d.pop("hostname", UNSET)

        _environment_variables_overrides = d.pop("environment_variables_overrides", UNSET)
        environment_variables_overrides: Union[Unset, None, TaskExecutionEnvironmentVariablesOverrides]
        if _environment_variables_overrides is None:
            environment_variables_overrides = None
        elif isinstance(_environment_variables_overrides, Unset):
            environment_variables_overrides = UNSET
        else:
            environment_variables_overrides = TaskExecutionEnvironmentVariablesOverrides.from_dict(
                _environment_variables_overrides
            )

        _execution_method = d.pop("execution_method", UNSET)
        execution_method: Union[Unset, AwsEcsExecutionMethod]
        if isinstance(_execution_method, Unset):
            execution_method = UNSET
        else:
            execution_method = AwsEcsExecutionMethod.from_dict(_execution_method)

        started_by = d.pop("started_by", UNSET)

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

        marked_done_by = d.pop("marked_done_by", UNSET)

        _marked_done_at = d.pop("marked_done_at", UNSET)
        marked_done_at: Union[Unset, None, datetime.datetime]
        if _marked_done_at is None:
            marked_done_at = None
        elif isinstance(_marked_done_at, Unset):
            marked_done_at = UNSET
        else:
            marked_done_at = isoparse(_marked_done_at)

        _marked_outdated_at = d.pop("marked_outdated_at", UNSET)
        marked_outdated_at: Union[Unset, None, datetime.datetime]
        if _marked_outdated_at is None:
            marked_outdated_at = None
        elif isinstance(_marked_outdated_at, Unset):
            marked_outdated_at = UNSET
        else:
            marked_outdated_at = isoparse(_marked_outdated_at)

        killed_by = d.pop("killed_by", UNSET)

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

        _stop_reason = d.pop("stop_reason", UNSET)
        stop_reason: Union[Unset, None, StopReasonEnum]
        if _stop_reason is None:
            stop_reason = None
        elif isinstance(_stop_reason, Unset):
            stop_reason = UNSET
        else:
            stop_reason = StopReasonEnum(_stop_reason)

        _last_heartbeat_at = d.pop("last_heartbeat_at", UNSET)
        last_heartbeat_at: Union[Unset, None, datetime.datetime]
        if _last_heartbeat_at is None:
            last_heartbeat_at = None
        elif isinstance(_last_heartbeat_at, Unset):
            last_heartbeat_at = UNSET
        else:
            last_heartbeat_at = isoparse(_last_heartbeat_at)

        failed_attempts = d.pop("failed_attempts", UNSET)

        timed_out_attempts = d.pop("timed_out_attempts", UNSET)

        exit_code = d.pop("exit_code", UNSET)

        last_status_message = d.pop("last_status_message", UNSET)

        error_count = d.pop("error_count", UNSET)

        skipped_count = d.pop("skipped_count", UNSET)

        expected_count = d.pop("expected_count", UNSET)

        success_count = d.pop("success_count", UNSET)

        _other_runtime_metadata = d.pop("other_runtime_metadata", UNSET)
        other_runtime_metadata: Union[Unset, None, TaskExecutionOtherRuntimeMetadata]
        if _other_runtime_metadata is None:
            other_runtime_metadata = None
        elif isinstance(_other_runtime_metadata, Unset):
            other_runtime_metadata = UNSET
        else:
            other_runtime_metadata = TaskExecutionOtherRuntimeMetadata.from_dict(_other_runtime_metadata)

        current_cpu_units = d.pop("current_cpu_units", UNSET)

        mean_cpu_units = d.pop("mean_cpu_units", UNSET)

        max_cpu_units = d.pop("max_cpu_units", UNSET)

        current_memory_mb = d.pop("current_memory_mb", UNSET)

        mean_memory_mb = d.pop("mean_memory_mb", UNSET)

        max_memory_mb = d.pop("max_memory_mb", UNSET)

        wrapper_version = d.pop("wrapper_version", UNSET)

        wrapper_log_level = d.pop("wrapper_log_level", UNSET)

        deployment = d.pop("deployment", UNSET)

        process_command = d.pop("process_command", UNSET)

        is_service = d.pop("is_service", UNSET)

        task_max_concurrency = d.pop("task_max_concurrency", UNSET)

        max_conflicting_age_seconds = d.pop("max_conflicting_age_seconds", UNSET)

        prevent_offline_execution = d.pop("prevent_offline_execution", UNSET)

        process_timeout_seconds = d.pop("process_timeout_seconds", UNSET)

        process_termination_grace_period_seconds = d.pop("process_termination_grace_period_seconds", UNSET)

        process_max_retries = d.pop("process_max_retries", UNSET)

        process_retry_delay_seconds = d.pop("process_retry_delay_seconds", UNSET)

        schedule = d.pop("schedule", UNSET)

        heartbeat_interval_seconds = d.pop("heartbeat_interval_seconds", UNSET)

        _workflow_task_instance_execution = d.pop("workflow_task_instance_execution", UNSET)
        workflow_task_instance_execution: Union[Unset, None, WorkflowTaskInstanceExecutionBase]
        if _workflow_task_instance_execution is None:
            workflow_task_instance_execution = None
        elif isinstance(_workflow_task_instance_execution, Unset):
            workflow_task_instance_execution = UNSET
        else:
            workflow_task_instance_execution = WorkflowTaskInstanceExecutionBase.from_dict(
                _workflow_task_instance_execution
            )

        api_base_url = d.pop("api_base_url", UNSET)

        api_request_timeout_seconds = d.pop("api_request_timeout_seconds", UNSET)

        api_retry_delay_seconds = d.pop("api_retry_delay_seconds", UNSET)

        api_resume_delay_seconds = d.pop("api_resume_delay_seconds", UNSET)

        api_error_timeout_seconds = d.pop("api_error_timeout_seconds", UNSET)

        api_task_execution_creation_error_timeout_seconds = d.pop(
            "api_task_execution_creation_error_timeout_seconds", UNSET
        )

        api_task_execution_creation_conflict_timeout_seconds = d.pop(
            "api_task_execution_creation_conflict_timeout_seconds", UNSET
        )

        api_task_execution_creation_conflict_retry_delay_seconds = d.pop(
            "api_task_execution_creation_conflict_retry_delay_seconds", UNSET
        )

        api_final_update_timeout_seconds = d.pop("api_final_update_timeout_seconds", UNSET)

        status_update_interval_seconds = d.pop("status_update_interval_seconds", UNSET)

        status_update_port = d.pop("status_update_port", UNSET)

        status_update_message_max_bytes = d.pop("status_update_message_max_bytes", UNSET)

        debug_log_tail = d.pop("debug_log_tail", UNSET)

        error_log_tail = d.pop("error_log_tail", UNSET)

        embedded_mode = d.pop("embedded_mode", UNSET)

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

        task_execution = cls(
            status=status,
            url=url,
            uuid=uuid,
            dashboard_url=dashboard_url,
            infrastructure_website_url=infrastructure_website_url,
            task=task,
            task_version_number=task_version_number,
            task_version_text=task_version_text,
            task_version_signature=task_version_signature,
            commit_url=commit_url,
            other_instance_metadata=other_instance_metadata,
            hostname=hostname,
            environment_variables_overrides=environment_variables_overrides,
            execution_method=execution_method,
            started_by=started_by,
            started_at=started_at,
            finished_at=finished_at,
            marked_done_by=marked_done_by,
            marked_done_at=marked_done_at,
            marked_outdated_at=marked_outdated_at,
            killed_by=killed_by,
            kill_started_at=kill_started_at,
            kill_finished_at=kill_finished_at,
            kill_error_code=kill_error_code,
            stop_reason=stop_reason,
            last_heartbeat_at=last_heartbeat_at,
            failed_attempts=failed_attempts,
            timed_out_attempts=timed_out_attempts,
            exit_code=exit_code,
            last_status_message=last_status_message,
            error_count=error_count,
            skipped_count=skipped_count,
            expected_count=expected_count,
            success_count=success_count,
            other_runtime_metadata=other_runtime_metadata,
            current_cpu_units=current_cpu_units,
            mean_cpu_units=mean_cpu_units,
            max_cpu_units=max_cpu_units,
            current_memory_mb=current_memory_mb,
            mean_memory_mb=mean_memory_mb,
            max_memory_mb=max_memory_mb,
            wrapper_version=wrapper_version,
            wrapper_log_level=wrapper_log_level,
            deployment=deployment,
            process_command=process_command,
            is_service=is_service,
            task_max_concurrency=task_max_concurrency,
            max_conflicting_age_seconds=max_conflicting_age_seconds,
            prevent_offline_execution=prevent_offline_execution,
            process_timeout_seconds=process_timeout_seconds,
            process_termination_grace_period_seconds=process_termination_grace_period_seconds,
            process_max_retries=process_max_retries,
            process_retry_delay_seconds=process_retry_delay_seconds,
            schedule=schedule,
            heartbeat_interval_seconds=heartbeat_interval_seconds,
            workflow_task_instance_execution=workflow_task_instance_execution,
            api_base_url=api_base_url,
            api_request_timeout_seconds=api_request_timeout_seconds,
            api_retry_delay_seconds=api_retry_delay_seconds,
            api_resume_delay_seconds=api_resume_delay_seconds,
            api_error_timeout_seconds=api_error_timeout_seconds,
            api_task_execution_creation_error_timeout_seconds=api_task_execution_creation_error_timeout_seconds,
            api_task_execution_creation_conflict_timeout_seconds=api_task_execution_creation_conflict_timeout_seconds,
            api_task_execution_creation_conflict_retry_delay_seconds=api_task_execution_creation_conflict_retry_delay_seconds,
            api_final_update_timeout_seconds=api_final_update_timeout_seconds,
            status_update_interval_seconds=status_update_interval_seconds,
            status_update_port=status_update_port,
            status_update_message_max_bytes=status_update_message_max_bytes,
            debug_log_tail=debug_log_tail,
            error_log_tail=error_log_tail,
            embedded_mode=embedded_mode,
            created_at=created_at,
            updated_at=updated_at,
        )

        task_execution.additional_properties = d
        return task_execution

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
