from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.patched_task_execution import PatchedTaskExecution
from ...models.task_execution import TaskExecution
from ...types import Response


def _get_kwargs(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTaskExecution,
) -> Dict[str, Any]:
    url = "{}/task_executions/{uuid}/".format(client.base_url, uuid=uuid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[TaskExecution]:
    if response.status_code == 200:
        response_200 = TaskExecution.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TaskExecution]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTaskExecution,
) -> Response[TaskExecution]:
    """
    Args:
        uuid (str):
        json_body (PatchedTaskExecution): A Task Execution is an execution / run instance of a
            Task.

    Returns:
        Response[TaskExecution]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTaskExecution,
) -> Optional[TaskExecution]:
    """
    Args:
        uuid (str):
        json_body (PatchedTaskExecution): A Task Execution is an execution / run instance of a
            Task.

    Returns:
        Response[TaskExecution]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTaskExecution,
) -> Response[TaskExecution]:
    """
    Args:
        uuid (str):
        json_body (PatchedTaskExecution): A Task Execution is an execution / run instance of a
            Task.

    Returns:
        Response[TaskExecution]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTaskExecution,
) -> Optional[TaskExecution]:
    """
    Args:
        uuid (str):
        json_body (PatchedTaskExecution): A Task Execution is an execution / run instance of a
            Task.

    Returns:
        Response[TaskExecution]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            json_body=json_body,
        )
    ).parsed
