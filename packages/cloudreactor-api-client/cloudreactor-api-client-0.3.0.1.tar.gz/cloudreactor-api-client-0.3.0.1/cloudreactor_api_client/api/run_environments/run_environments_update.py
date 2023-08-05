from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.run_environment import RunEnvironment
from ...types import Response


def _get_kwargs(
    uuid: str,
    *,
    client: AuthenticatedClient,
    json_body: RunEnvironment,
) -> Dict[str, Any]:
    url = "{}/run_environments/{uuid}/".format(client.base_url, uuid=uuid)

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


def _parse_response(*, response: httpx.Response) -> Optional[RunEnvironment]:
    if response.status_code == 200:
        response_200 = RunEnvironment.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RunEnvironment]:
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
    json_body: RunEnvironment,
) -> Response[RunEnvironment]:
    """
    Args:
        uuid (str):
        json_body (RunEnvironment): RunEnvironments contain common settings for running a set of
            related Tasks. Usually RunEnvironments group Tasks in the same
            deployment environment (e.g. staging or production).
            Task and Workflows belong to a RunEnvironment but can override
            the RunEnvironment's settings.

    Returns:
        Response[RunEnvironment]
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
    json_body: RunEnvironment,
) -> Optional[RunEnvironment]:
    """
    Args:
        uuid (str):
        json_body (RunEnvironment): RunEnvironments contain common settings for running a set of
            related Tasks. Usually RunEnvironments group Tasks in the same
            deployment environment (e.g. staging or production).
            Task and Workflows belong to a RunEnvironment but can override
            the RunEnvironment's settings.

    Returns:
        Response[RunEnvironment]
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
    json_body: RunEnvironment,
) -> Response[RunEnvironment]:
    """
    Args:
        uuid (str):
        json_body (RunEnvironment): RunEnvironments contain common settings for running a set of
            related Tasks. Usually RunEnvironments group Tasks in the same
            deployment environment (e.g. staging or production).
            Task and Workflows belong to a RunEnvironment but can override
            the RunEnvironment's settings.

    Returns:
        Response[RunEnvironment]
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
    json_body: RunEnvironment,
) -> Optional[RunEnvironment]:
    """
    Args:
        uuid (str):
        json_body (RunEnvironment): RunEnvironments contain common settings for running a set of
            related Tasks. Usually RunEnvironments group Tasks in the same
            deployment environment (e.g. staging or production).
            Task and Workflows belong to a RunEnvironment but can override
            the RunEnvironment's settings.

    Returns:
        Response[RunEnvironment]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            json_body=json_body,
        )
    ).parsed
