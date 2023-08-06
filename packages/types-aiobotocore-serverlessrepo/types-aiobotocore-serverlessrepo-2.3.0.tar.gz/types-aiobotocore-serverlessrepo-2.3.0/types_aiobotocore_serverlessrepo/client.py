"""
Type annotations for serverlessrepo service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_serverlessrepo.client import ServerlessApplicationRepositoryClient

    session = get_session()
    async with session.create_client("serverlessrepo") as client:
        client: ServerlessApplicationRepositoryClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListApplicationDependenciesPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)
from .type_defs import (
    ApplicationPolicyStatementTypeDef,
    CreateApplicationResponseTypeDef,
    CreateApplicationVersionResponseTypeDef,
    CreateCloudFormationChangeSetResponseTypeDef,
    CreateCloudFormationTemplateResponseTypeDef,
    GetApplicationPolicyResponseTypeDef,
    GetApplicationResponseTypeDef,
    GetCloudFormationTemplateResponseTypeDef,
    ListApplicationDependenciesResponseTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ParameterValueTypeDef,
    PutApplicationPolicyResponseTypeDef,
    RollbackConfigurationTypeDef,
    TagTypeDef,
    UpdateApplicationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServerlessApplicationRepositoryClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class ServerlessApplicationRepositoryClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ServerlessApplicationRepositoryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#can_paginate)
        """

    async def create_application(
        self,
        *,
        Author: str,
        Description: str,
        Name: str,
        HomePageUrl: str = ...,
        Labels: Sequence[str] = ...,
        LicenseBody: str = ...,
        LicenseUrl: str = ...,
        ReadmeBody: str = ...,
        ReadmeUrl: str = ...,
        SemanticVersion: str = ...,
        SourceCodeArchiveUrl: str = ...,
        SourceCodeUrl: str = ...,
        SpdxLicenseId: str = ...,
        TemplateBody: str = ...,
        TemplateUrl: str = ...
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an application, optionally including an AWS SAM file to create the first
        application version in the same call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#create_application)
        """

    async def create_application_version(
        self,
        *,
        ApplicationId: str,
        SemanticVersion: str,
        SourceCodeArchiveUrl: str = ...,
        SourceCodeUrl: str = ...,
        TemplateBody: str = ...,
        TemplateUrl: str = ...
    ) -> CreateApplicationVersionResponseTypeDef:
        """
        Creates an application version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.create_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#create_application_version)
        """

    async def create_cloud_formation_change_set(
        self,
        *,
        ApplicationId: str,
        StackName: str,
        Capabilities: Sequence[str] = ...,
        ChangeSetName: str = ...,
        ClientToken: str = ...,
        Description: str = ...,
        NotificationArns: Sequence[str] = ...,
        ParameterOverrides: Sequence["ParameterValueTypeDef"] = ...,
        ResourceTypes: Sequence[str] = ...,
        RollbackConfiguration: "RollbackConfigurationTypeDef" = ...,
        SemanticVersion: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        TemplateId: str = ...
    ) -> CreateCloudFormationChangeSetResponseTypeDef:
        """
        Creates an AWS CloudFormation change set for the given application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.create_cloud_formation_change_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#create_cloud_formation_change_set)
        """

    async def create_cloud_formation_template(
        self, *, ApplicationId: str, SemanticVersion: str = ...
    ) -> CreateCloudFormationTemplateResponseTypeDef:
        """
        Creates an AWS CloudFormation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.create_cloud_formation_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#create_cloud_formation_template)
        """

    async def delete_application(self, *, ApplicationId: str) -> None:
        """
        Deletes the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#delete_application)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#generate_presigned_url)
        """

    async def get_application(
        self, *, ApplicationId: str, SemanticVersion: str = ...
    ) -> GetApplicationResponseTypeDef:
        """
        Gets the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_application)
        """

    async def get_application_policy(
        self, *, ApplicationId: str
    ) -> GetApplicationPolicyResponseTypeDef:
        """
        Retrieves the policy for the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_application_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_application_policy)
        """

    async def get_cloud_formation_template(
        self, *, ApplicationId: str, TemplateId: str
    ) -> GetCloudFormationTemplateResponseTypeDef:
        """
        Gets the specified AWS CloudFormation template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_cloud_formation_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_cloud_formation_template)
        """

    async def list_application_dependencies(
        self,
        *,
        ApplicationId: str,
        MaxItems: int = ...,
        NextToken: str = ...,
        SemanticVersion: str = ...
    ) -> ListApplicationDependenciesResponseTypeDef:
        """
        Retrieves the list of applications nested in the containing application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.list_application_dependencies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#list_application_dependencies)
        """

    async def list_application_versions(
        self, *, ApplicationId: str, MaxItems: int = ..., NextToken: str = ...
    ) -> ListApplicationVersionsResponseTypeDef:
        """
        Lists versions for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.list_application_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#list_application_versions)
        """

    async def list_applications(
        self, *, MaxItems: int = ..., NextToken: str = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists applications owned by the requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#list_applications)
        """

    async def put_application_policy(
        self, *, ApplicationId: str, Statements: Sequence["ApplicationPolicyStatementTypeDef"]
    ) -> PutApplicationPolicyResponseTypeDef:
        """
        Sets the permission policy for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.put_application_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#put_application_policy)
        """

    async def unshare_application(self, *, ApplicationId: str, OrganizationId: str) -> None:
        """
        Unshares an application from an AWS Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.unshare_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#unshare_application)
        """

    async def update_application(
        self,
        *,
        ApplicationId: str,
        Author: str = ...,
        Description: str = ...,
        HomePageUrl: str = ...,
        Labels: Sequence[str] = ...,
        ReadmeBody: str = ...,
        ReadmeUrl: str = ...
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#update_application)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_dependencies"]
    ) -> ListApplicationDependenciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_versions"]
    ) -> ListApplicationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/#get_paginator)
        """

    async def __aenter__(self) -> "ServerlessApplicationRepositoryClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/serverlessrepo.html#ServerlessApplicationRepository.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_serverlessrepo/client/)
        """
