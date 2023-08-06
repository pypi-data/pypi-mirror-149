"""
Main interface for efs service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_efs import (
        Client,
        DescribeFileSystemsPaginator,
        DescribeMountTargetsPaginator,
        DescribeTagsPaginator,
        EFSClient,
    )

    session = get_session()
    async with session.create_client("efs") as client:
        client: EFSClient
        ...


    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    describe_mount_targets_paginator: DescribeMountTargetsPaginator = client.get_paginator("describe_mount_targets")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```
"""
from .client import EFSClient
from .paginator import (
    DescribeFileSystemsPaginator,
    DescribeMountTargetsPaginator,
    DescribeTagsPaginator,
)

Client = EFSClient

__all__ = (
    "Client",
    "DescribeFileSystemsPaginator",
    "DescribeMountTargetsPaginator",
    "DescribeTagsPaginator",
    "EFSClient",
)
