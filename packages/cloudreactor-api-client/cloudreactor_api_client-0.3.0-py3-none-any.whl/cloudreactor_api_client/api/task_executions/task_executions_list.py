from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.paginated_task_execution_list import PaginatedTaskExecutionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_created_by_group_id: Union[Unset, None, int] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/task_executions/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["offset"] = offset

    params["ordering"] = ordering

    params["search"] = search

    params["task__created_by_group__id"] = task_created_by_group_id

    params["task__uuid"] = task_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PaginatedTaskExecutionList]:
    if response.status_code == 200:
        response_200 = PaginatedTaskExecutionList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaginatedTaskExecutionList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_created_by_group_id: Union[Unset, None, int] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedTaskExecutionList]:
    """
    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_created_by_group_id (Union[Unset, None, int]):
        task_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskExecutionList]
    """

    kwargs = _get_kwargs(
        client=client,
        limit=limit,
        offset=offset,
        ordering=ordering,
        search=search,
        task_created_by_group_id=task_created_by_group_id,
        task_uuid=task_uuid,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_created_by_group_id: Union[Unset, None, int] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedTaskExecutionList]:
    """
    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_created_by_group_id (Union[Unset, None, int]):
        task_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskExecutionList]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        ordering=ordering,
        search=search,
        task_created_by_group_id=task_created_by_group_id,
        task_uuid=task_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_created_by_group_id: Union[Unset, None, int] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedTaskExecutionList]:
    """
    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_created_by_group_id (Union[Unset, None, int]):
        task_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskExecutionList]
    """

    kwargs = _get_kwargs(
        client=client,
        limit=limit,
        offset=offset,
        ordering=ordering,
        search=search,
        task_created_by_group_id=task_created_by_group_id,
        task_uuid=task_uuid,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_created_by_group_id: Union[Unset, None, int] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedTaskExecutionList]:
    """
    Args:
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_created_by_group_id (Union[Unset, None, int]):
        task_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskExecutionList]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            ordering=ordering,
            search=search,
            task_created_by_group_id=task_created_by_group_id,
            task_uuid=task_uuid,
        )
    ).parsed
