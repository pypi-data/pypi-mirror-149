from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.email_notification_profile import EmailNotificationProfile
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: EmailNotificationProfile,
) -> Dict[str, Any]:
    url = "{}/email_notification_profiles/".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[EmailNotificationProfile]:
    if response.status_code == 201:
        response_201 = EmailNotificationProfile.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[EmailNotificationProfile]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: EmailNotificationProfile,
) -> Response[EmailNotificationProfile]:
    """
    Args:
        json_body (EmailNotificationProfile): An EmailProfile contains settings for emailing
            notifications.

    Returns:
        Response[EmailNotificationProfile]
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
    json_body: EmailNotificationProfile,
) -> Optional[EmailNotificationProfile]:
    """
    Args:
        json_body (EmailNotificationProfile): An EmailProfile contains settings for emailing
            notifications.

    Returns:
        Response[EmailNotificationProfile]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: EmailNotificationProfile,
) -> Response[EmailNotificationProfile]:
    """
    Args:
        json_body (EmailNotificationProfile): An EmailProfile contains settings for emailing
            notifications.

    Returns:
        Response[EmailNotificationProfile]
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
    json_body: EmailNotificationProfile,
) -> Optional[EmailNotificationProfile]:
    """
    Args:
        json_body (EmailNotificationProfile): An EmailProfile contains settings for emailing
            notifications.

    Returns:
        Response[EmailNotificationProfile]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
