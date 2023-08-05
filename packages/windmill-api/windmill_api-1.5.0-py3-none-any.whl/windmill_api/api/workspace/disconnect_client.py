from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    workspace: str,
    client_name: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/oauth/disconnect/{client_name}".format(
        client.base_url, workspace=workspace, client_name=client_name
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    workspace: str,
    client_name: str,
    *,
    client: Client,
) -> Response[Any]:
    """disconnect client

    Args:
        workspace (str):
        client_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client_name=client_name,
        client=client,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    client_name: str,
    *,
    client: Client,
) -> Response[Any]:
    """disconnect client

    Args:
        workspace (str):
        client_name (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client_name=client_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
