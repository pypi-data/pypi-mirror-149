from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.paginated_alert_method_list import PaginatedAlertMethodList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/alert_methods/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["created_by_group__id"] = created_by_group_id

    params["limit"] = limit

    params["name"] = name

    params["offset"] = offset

    params["ordering"] = ordering

    params["run_environment__uuid"] = run_environment_uuid

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PaginatedAlertMethodList]:
    if response.status_code == 200:
        response_200 = PaginatedAlertMethodList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaginatedAlertMethodList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedAlertMethodList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedAlertMethodList]
    """

    kwargs = _get_kwargs(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        run_environment_uuid=run_environment_uuid,
        search=search,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedAlertMethodList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedAlertMethodList]
    """

    return sync_detailed(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        run_environment_uuid=run_environment_uuid,
        search=search,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedAlertMethodList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedAlertMethodList]
    """

    kwargs = _get_kwargs(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        run_environment_uuid=run_environment_uuid,
        search=search,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedAlertMethodList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedAlertMethodList]
    """

    return (
        await asyncio_detailed(
            client=client,
            created_by_group_id=created_by_group_id,
            limit=limit,
            name=name,
            offset=offset,
            ordering=ordering,
            run_environment_uuid=run_environment_uuid,
            search=search,
        )
    ).parsed
