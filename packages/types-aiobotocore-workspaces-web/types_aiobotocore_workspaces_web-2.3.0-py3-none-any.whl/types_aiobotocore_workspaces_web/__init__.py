"""
Main interface for workspaces-web service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_web import (
        Client,
        WorkSpacesWebClient,
    )

    session = get_session()
    async with session.create_client("workspaces-web") as client:
        client: WorkSpacesWebClient
        ...

    ```
"""
from .client import WorkSpacesWebClient

Client = WorkSpacesWebClient


__all__ = ("Client", "WorkSpacesWebClient")
