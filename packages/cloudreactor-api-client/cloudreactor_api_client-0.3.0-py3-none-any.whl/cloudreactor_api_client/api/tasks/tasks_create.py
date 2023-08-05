from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.task import Task
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: Task,
) -> Dict[str, Any]:
    url = "{}/tasks/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Task]:
    if response.status_code == 201:
        response_201 = Task.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[Task]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Task,
) -> Response[Task]:
    """
    Args:
        json_body (Task): A Task is a specification for a runnable job, including details on how
            to
            run the task and how often the task is supposed to run.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: Task,
) -> Optional[Task]:
    """
    Args:
        json_body (Task): A Task is a specification for a runnable job, including details on how
            to
            run the task and how often the task is supposed to run.

    Returns:
        Response[Task]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Task,
) -> Response[Task]:
    """
    Args:
        json_body (Task): A Task is a specification for a runnable job, including details on how
            to
            run the task and how often the task is supposed to run.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: Task,
) -> Optional[Task]:
    """
    Args:
        json_body (Task): A Task is a specification for a runnable job, including details on how
            to
            run the task and how often the task is supposed to run.

    Returns:
        Response[Task]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
