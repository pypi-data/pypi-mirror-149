"""
Type annotations for cloud9 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloud9.client import Cloud9Client
    from types_aiobotocore_cloud9.paginator import (
        DescribeEnvironmentMembershipsPaginator,
        ListEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("cloud9") as client:
        client: Cloud9Client

        describe_environment_memberships_paginator: DescribeEnvironmentMembershipsPaginator = client.get_paginator("describe_environment_memberships")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import PermissionsType
from .type_defs import (
    DescribeEnvironmentMembershipsResultTypeDef,
    ListEnvironmentsResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("DescribeEnvironmentMembershipsPaginator", "ListEnvironmentsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeEnvironmentMembershipsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Paginator.DescribeEnvironmentMemberships)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/paginators/#describeenvironmentmembershipspaginator)
    """

    def paginate(
        self,
        *,
        userArn: str = ...,
        environmentId: str = ...,
        permissions: Sequence[PermissionsType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeEnvironmentMembershipsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Paginator.DescribeEnvironmentMemberships.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/paginators/#describeenvironmentmembershipspaginator)
        """

class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEnvironmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloud9/paginators/#listenvironmentspaginator)
        """
