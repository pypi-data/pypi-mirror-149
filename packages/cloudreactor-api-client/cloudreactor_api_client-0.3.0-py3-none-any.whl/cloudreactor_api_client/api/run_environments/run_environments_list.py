from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.paginated_run_environment_list import PaginatedRunEnvironmentList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    created_by_group_id: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/run_environments/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["created_by_group__id"] = created_by_group_id

    params["limit"] = limit

    params["name"] = name

    params["offset"] = offset

    params["ordering"] = ordering

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


def _parse_response(*, response: httpx.Response) -> Optional[PaginatedRunEnvironmentList]:
    if response.status_code == 200:
        response_200 = PaginatedRunEnvironmentList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaginatedRunEnvironmentList]:
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
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedRunEnvironmentList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedRunEnvironmentList]
    """

    kwargs = _get_kwargs(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
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
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedRunEnvironmentList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedRunEnvironmentList]
    """

    return sync_detailed(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
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
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedRunEnvironmentList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedRunEnvironmentList]
    """

    kwargs = _get_kwargs(
        client=client,
        created_by_group_id=created_by_group_id,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
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
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedRunEnvironmentList]:
    """
    Args:
        created_by_group_id (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedRunEnvironmentList]
    """

    return (
        await asyncio_detailed(
            client=client,
            created_by_group_id=created_by_group_id,
            limit=limit,
            name=name,
            offset=offset,
            ordering=ordering,
            search=search,
        )
    ).parsed
