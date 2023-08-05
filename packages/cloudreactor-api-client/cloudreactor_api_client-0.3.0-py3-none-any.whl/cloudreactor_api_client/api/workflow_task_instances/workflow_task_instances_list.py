from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.paginated_workflow_task_instance_list import PaginatedWorkflowTaskInstanceList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_name: Union[Unset, None, str] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
    workflow_created_by_group_id: Union[Unset, None, int] = UNSET,
    workflow_run_environment_uuid: Union[Unset, None, str] = UNSET,
    workflow_uuid: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/workflow_task_instances/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["description"] = description

    params["limit"] = limit

    params["name"] = name

    params["offset"] = offset

    params["ordering"] = ordering

    params["search"] = search

    params["task__name"] = task_name

    params["task__uuid"] = task_uuid

    params["workflow__created_by_group__id"] = workflow_created_by_group_id

    params["workflow__run_environment__uuid"] = workflow_run_environment_uuid

    params["workflow__uuid"] = workflow_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PaginatedWorkflowTaskInstanceList]:
    if response.status_code == 200:
        response_200 = PaginatedWorkflowTaskInstanceList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaginatedWorkflowTaskInstanceList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_name: Union[Unset, None, str] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
    workflow_created_by_group_id: Union[Unset, None, int] = UNSET,
    workflow_run_environment_uuid: Union[Unset, None, str] = UNSET,
    workflow_uuid: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedWorkflowTaskInstanceList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_name (Union[Unset, None, str]):
        task_uuid (Union[Unset, None, str]):
        workflow_created_by_group_id (Union[Unset, None, int]):
        workflow_run_environment_uuid (Union[Unset, None, str]):
        workflow_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedWorkflowTaskInstanceList]
    """

    kwargs = _get_kwargs(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        search=search,
        task_name=task_name,
        task_uuid=task_uuid,
        workflow_created_by_group_id=workflow_created_by_group_id,
        workflow_run_environment_uuid=workflow_run_environment_uuid,
        workflow_uuid=workflow_uuid,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_name: Union[Unset, None, str] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
    workflow_created_by_group_id: Union[Unset, None, int] = UNSET,
    workflow_run_environment_uuid: Union[Unset, None, str] = UNSET,
    workflow_uuid: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedWorkflowTaskInstanceList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_name (Union[Unset, None, str]):
        task_uuid (Union[Unset, None, str]):
        workflow_created_by_group_id (Union[Unset, None, int]):
        workflow_run_environment_uuid (Union[Unset, None, str]):
        workflow_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedWorkflowTaskInstanceList]
    """

    return sync_detailed(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        search=search,
        task_name=task_name,
        task_uuid=task_uuid,
        workflow_created_by_group_id=workflow_created_by_group_id,
        workflow_run_environment_uuid=workflow_run_environment_uuid,
        workflow_uuid=workflow_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_name: Union[Unset, None, str] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
    workflow_created_by_group_id: Union[Unset, None, int] = UNSET,
    workflow_run_environment_uuid: Union[Unset, None, str] = UNSET,
    workflow_uuid: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedWorkflowTaskInstanceList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_name (Union[Unset, None, str]):
        task_uuid (Union[Unset, None, str]):
        workflow_created_by_group_id (Union[Unset, None, int]):
        workflow_run_environment_uuid (Union[Unset, None, str]):
        workflow_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedWorkflowTaskInstanceList]
    """

    kwargs = _get_kwargs(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        search=search,
        task_name=task_name,
        task_uuid=task_uuid,
        workflow_created_by_group_id=workflow_created_by_group_id,
        workflow_run_environment_uuid=workflow_run_environment_uuid,
        workflow_uuid=workflow_uuid,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    task_name: Union[Unset, None, str] = UNSET,
    task_uuid: Union[Unset, None, str] = UNSET,
    workflow_created_by_group_id: Union[Unset, None, int] = UNSET,
    workflow_run_environment_uuid: Union[Unset, None, str] = UNSET,
    workflow_uuid: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedWorkflowTaskInstanceList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):
        task_name (Union[Unset, None, str]):
        task_uuid (Union[Unset, None, str]):
        workflow_created_by_group_id (Union[Unset, None, int]):
        workflow_run_environment_uuid (Union[Unset, None, str]):
        workflow_uuid (Union[Unset, None, str]):

    Returns:
        Response[PaginatedWorkflowTaskInstanceList]
    """

    return (
        await asyncio_detailed(
            client=client,
            description=description,
            limit=limit,
            name=name,
            offset=offset,
            ordering=ordering,
            search=search,
            task_name=task_name,
            task_uuid=task_uuid,
            workflow_created_by_group_id=workflow_created_by_group_id,
            workflow_run_environment_uuid=workflow_run_environment_uuid,
            workflow_uuid=workflow_uuid,
        )
    ).parsed
