"""
Main interface for s3control service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3control import (
        Client,
        ListAccessPointsForObjectLambdaPaginator,
        S3ControlClient,
    )

    session = get_session()
    async with session.create_client("s3control") as client:
        client: S3ControlClient
        ...


    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    ```
"""
from .client import S3ControlClient
from .paginator import ListAccessPointsForObjectLambdaPaginator

Client = S3ControlClient


__all__ = ("Client", "ListAccessPointsForObjectLambdaPaginator", "S3ControlClient")
