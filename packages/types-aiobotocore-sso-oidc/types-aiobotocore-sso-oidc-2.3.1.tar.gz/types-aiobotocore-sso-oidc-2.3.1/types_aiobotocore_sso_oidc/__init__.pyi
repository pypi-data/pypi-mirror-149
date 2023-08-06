"""
Main interface for sso-oidc service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sso_oidc import (
        Client,
        SSOOIDCClient,
    )

    session = get_session()
    async with session.create_client("sso-oidc") as client:
        client: SSOOIDCClient
        ...

    ```
"""
from .client import SSOOIDCClient

Client = SSOOIDCClient

__all__ = ("Client", "SSOOIDCClient")
