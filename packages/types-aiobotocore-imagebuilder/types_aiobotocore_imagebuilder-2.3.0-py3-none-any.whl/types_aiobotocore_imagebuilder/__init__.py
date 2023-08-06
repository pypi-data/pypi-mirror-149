"""
Main interface for imagebuilder service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_imagebuilder import (
        Client,
        imagebuilderClient,
    )

    session = get_session()
    async with session.create_client("imagebuilder") as client:
        client: imagebuilderClient
        ...

    ```
"""
from .client import imagebuilderClient

Client = imagebuilderClient


__all__ = ("Client", "imagebuilderClient")
