from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.workflow_execution import WorkflowExecution
from ...types import Response


def _get_kwargs(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: WorkflowExecution,
) -> Dict[str, Any]:
    url = "{}/workflow_executions/{uuid}/".format(client.base_url, uuid=uuid)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[WorkflowExecution]:
    if response.status_code == 200:
        response_200 = WorkflowExecution.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[WorkflowExecution]:
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
    json_body: WorkflowExecution,
) -> Response[WorkflowExecution]:
    """
    Args:
        uuid (str):
        json_body (WorkflowExecution): A WorkflowExecution holds data on a specific execution
            (run) of a Workflow.

    Returns:
        Response[WorkflowExecution]
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
    json_body: WorkflowExecution,
) -> Optional[WorkflowExecution]:
    """
    Args:
        uuid (str):
        json_body (WorkflowExecution): A WorkflowExecution holds data on a specific execution
            (run) of a Workflow.

    Returns:
        Response[WorkflowExecution]
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
    json_body: WorkflowExecution,
) -> Response[WorkflowExecution]:
    """
    Args:
        uuid (str):
        json_body (WorkflowExecution): A WorkflowExecution holds data on a specific execution
            (run) of a Workflow.

    Returns:
        Response[WorkflowExecution]
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
    json_body: WorkflowExecution,
) -> Optional[WorkflowExecution]:
    """
    Args:
        uuid (str):
        json_body (WorkflowExecution): A WorkflowExecution holds data on a specific execution
            (run) of a Workflow.

    Returns:
        Response[WorkflowExecution]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            json_body=json_body,
        )
    ).parsed
