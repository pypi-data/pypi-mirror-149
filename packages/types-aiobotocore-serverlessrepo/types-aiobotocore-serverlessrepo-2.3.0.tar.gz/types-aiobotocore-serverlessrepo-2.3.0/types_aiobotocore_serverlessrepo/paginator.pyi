"""
Type annotations for serverlessrepo service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_serverlessrepo.client import ServerlessApplicationRepositoryClient
    from types_aiobotocore_serverlessrepo.paginator import (
        ListApplicationDependenciesPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = get_session()
    with session.create_client("serverlessrepo") as client:
        client: ServerlessApplicationRepositoryClient

        list_application_dependencies_paginator: ListApplicationDependenciesPaginator = client.get_paginator("list_application_dependencies")
        list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationDependenciesResponseTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "ListApplicationDependenciesPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationDependenciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationdependenciespaginator)
    """

    def paginate(
        self,
        *,
        ApplicationId: str,
        SemanticVersion: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListApplicationDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationDependencies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationdependenciespaginator)
        """

class ListApplicationVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationversionspaginator)
    """

    def paginate(
        self, *, ApplicationId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplicationVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationversionspaginator)
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/paginators/#listapplicationspaginator)
        """
