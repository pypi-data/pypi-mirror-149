"""
Main interface for cloudcontrol service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudcontrol import (
        Client,
        CloudControlApiClient,
        ResourceRequestSuccessWaiter,
    )

    session = Session()
    client: CloudControlApiClient = session.client("cloudcontrol")

    resource_request_success_waiter: ResourceRequestSuccessWaiter = client.get_waiter("resource_request_success")
    ```
"""
from .client import CloudControlApiClient
from .waiter import ResourceRequestSuccessWaiter

Client = CloudControlApiClient


__all__ = ("Client", "CloudControlApiClient", "ResourceRequestSuccessWaiter")
