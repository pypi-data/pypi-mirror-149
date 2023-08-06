"""
Type annotations for amplify service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amplify.client import AmplifyClient

    session = get_session()
    async with session.create_client("amplify") as client:
        client: AmplifyClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import JobTypeType, PlatformType, StageType
from .paginator import (
    ListAppsPaginator,
    ListBranchesPaginator,
    ListDomainAssociationsPaginator,
    ListJobsPaginator,
)
from .type_defs import (
    AutoBranchCreationConfigTypeDef,
    CreateAppResultTypeDef,
    CreateBackendEnvironmentResultTypeDef,
    CreateBranchResultTypeDef,
    CreateDeploymentResultTypeDef,
    CreateDomainAssociationResultTypeDef,
    CreateWebhookResultTypeDef,
    CustomRuleTypeDef,
    DeleteAppResultTypeDef,
    DeleteBackendEnvironmentResultTypeDef,
    DeleteBranchResultTypeDef,
    DeleteDomainAssociationResultTypeDef,
    DeleteJobResultTypeDef,
    DeleteWebhookResultTypeDef,
    GenerateAccessLogsResultTypeDef,
    GetAppResultTypeDef,
    GetArtifactUrlResultTypeDef,
    GetBackendEnvironmentResultTypeDef,
    GetBranchResultTypeDef,
    GetDomainAssociationResultTypeDef,
    GetJobResultTypeDef,
    GetWebhookResultTypeDef,
    ListAppsResultTypeDef,
    ListArtifactsResultTypeDef,
    ListBackendEnvironmentsResultTypeDef,
    ListBranchesResultTypeDef,
    ListDomainAssociationsResultTypeDef,
    ListJobsResultTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebhooksResultTypeDef,
    StartDeploymentResultTypeDef,
    StartJobResultTypeDef,
    StopJobResultTypeDef,
    SubDomainSettingTypeDef,
    UpdateAppResultTypeDef,
    UpdateBranchResultTypeDef,
    UpdateDomainAssociationResultTypeDef,
    UpdateWebhookResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AmplifyClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependentServiceFailureException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class AmplifyClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#can_paginate)
        """

    async def create_app(
        self,
        *,
        name: str,
        description: str = ...,
        repository: str = ...,
        platform: PlatformType = ...,
        iamServiceRoleArn: str = ...,
        oauthToken: str = ...,
        accessToken: str = ...,
        environmentVariables: Mapping[str, str] = ...,
        enableBranchAutoBuild: bool = ...,
        enableBranchAutoDeletion: bool = ...,
        enableBasicAuth: bool = ...,
        basicAuthCredentials: str = ...,
        customRules: Sequence["CustomRuleTypeDef"] = ...,
        tags: Mapping[str, str] = ...,
        buildSpec: str = ...,
        customHeaders: str = ...,
        enableAutoBranchCreation: bool = ...,
        autoBranchCreationPatterns: Sequence[str] = ...,
        autoBranchCreationConfig: "AutoBranchCreationConfigTypeDef" = ...
    ) -> CreateAppResultTypeDef:
        """
        Creates a new Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_app)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_app)
        """

    async def create_backend_environment(
        self,
        *,
        appId: str,
        environmentName: str,
        stackName: str = ...,
        deploymentArtifacts: str = ...
    ) -> CreateBackendEnvironmentResultTypeDef:
        """
        Creates a new backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_backend_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_backend_environment)
        """

    async def create_branch(
        self,
        *,
        appId: str,
        branchName: str,
        description: str = ...,
        stage: StageType = ...,
        framework: str = ...,
        enableNotification: bool = ...,
        enableAutoBuild: bool = ...,
        environmentVariables: Mapping[str, str] = ...,
        basicAuthCredentials: str = ...,
        enableBasicAuth: bool = ...,
        enablePerformanceMode: bool = ...,
        tags: Mapping[str, str] = ...,
        buildSpec: str = ...,
        ttl: str = ...,
        displayName: str = ...,
        enablePullRequestPreview: bool = ...,
        pullRequestEnvironmentName: str = ...,
        backendEnvironmentArn: str = ...
    ) -> CreateBranchResultTypeDef:
        """
        Creates a new branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_branch)
        """

    async def create_deployment(
        self, *, appId: str, branchName: str, fileMap: Mapping[str, str] = ...
    ) -> CreateDeploymentResultTypeDef:
        """
        Creates a deployment for a manually deployed Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_deployment)
        """

    async def create_domain_association(
        self,
        *,
        appId: str,
        domainName: str,
        subDomainSettings: Sequence["SubDomainSettingTypeDef"],
        enableAutoSubDomain: bool = ...,
        autoSubDomainCreationPatterns: Sequence[str] = ...,
        autoSubDomainIAMRole: str = ...
    ) -> CreateDomainAssociationResultTypeDef:
        """
        Creates a new domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_domain_association)
        """

    async def create_webhook(
        self, *, appId: str, branchName: str, description: str = ...
    ) -> CreateWebhookResultTypeDef:
        """
        Creates a new webhook on an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.create_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#create_webhook)
        """

    async def delete_app(self, *, appId: str) -> DeleteAppResultTypeDef:
        """
        Deletes an existing Amplify app specified by an app ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_app)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_app)
        """

    async def delete_backend_environment(
        self, *, appId: str, environmentName: str
    ) -> DeleteBackendEnvironmentResultTypeDef:
        """
        Deletes a backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_backend_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_backend_environment)
        """

    async def delete_branch(self, *, appId: str, branchName: str) -> DeleteBranchResultTypeDef:
        """
        Deletes a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_branch)
        """

    async def delete_domain_association(
        self, *, appId: str, domainName: str
    ) -> DeleteDomainAssociationResultTypeDef:
        """
        Deletes a domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_domain_association)
        """

    async def delete_job(
        self, *, appId: str, branchName: str, jobId: str
    ) -> DeleteJobResultTypeDef:
        """
        Deletes a job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_job)
        """

    async def delete_webhook(self, *, webhookId: str) -> DeleteWebhookResultTypeDef:
        """
        Deletes a webhook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.delete_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#delete_webhook)
        """

    async def generate_access_logs(
        self,
        *,
        domainName: str,
        appId: str,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...
    ) -> GenerateAccessLogsResultTypeDef:
        """
        Returns the website access logs for a specific time range using a presigned URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.generate_access_logs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#generate_access_logs)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#generate_presigned_url)
        """

    async def get_app(self, *, appId: str) -> GetAppResultTypeDef:
        """
        Returns an existing Amplify app by appID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_app)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_app)
        """

    async def get_artifact_url(self, *, artifactId: str) -> GetArtifactUrlResultTypeDef:
        """
        Returns the artifact info that corresponds to an artifact id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_artifact_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_artifact_url)
        """

    async def get_backend_environment(
        self, *, appId: str, environmentName: str
    ) -> GetBackendEnvironmentResultTypeDef:
        """
        Returns a backend environment for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_backend_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_backend_environment)
        """

    async def get_branch(self, *, appId: str, branchName: str) -> GetBranchResultTypeDef:
        """
        Returns a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_branch)
        """

    async def get_domain_association(
        self, *, appId: str, domainName: str
    ) -> GetDomainAssociationResultTypeDef:
        """
        Returns the domain information for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_domain_association)
        """

    async def get_job(self, *, appId: str, branchName: str, jobId: str) -> GetJobResultTypeDef:
        """
        Returns a job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_job)
        """

    async def get_webhook(self, *, webhookId: str) -> GetWebhookResultTypeDef:
        """
        Returns the webhook information that corresponds to a specified webhook ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_webhook)
        """

    async def list_apps(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListAppsResultTypeDef:
        """
        Returns a list of the existing Amplify apps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_apps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_apps)
        """

    async def list_artifacts(
        self,
        *,
        appId: str,
        branchName: str,
        jobId: str,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListArtifactsResultTypeDef:
        """
        Returns a list of artifacts for a specified app, branch, and job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_artifacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_artifacts)
        """

    async def list_backend_environments(
        self, *, appId: str, environmentName: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListBackendEnvironmentsResultTypeDef:
        """
        Lists the backend environments for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_backend_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_backend_environments)
        """

    async def list_branches(
        self, *, appId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListBranchesResultTypeDef:
        """
        Lists the branches of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_branches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_branches)
        """

    async def list_domain_associations(
        self, *, appId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDomainAssociationsResultTypeDef:
        """
        Returns the domain associations for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_domain_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_domain_associations)
        """

    async def list_jobs(
        self, *, appId: str, branchName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListJobsResultTypeDef:
        """
        Lists the jobs for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_jobs)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_tags_for_resource)
        """

    async def list_webhooks(
        self, *, appId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListWebhooksResultTypeDef:
        """
        Returns a list of webhooks for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.list_webhooks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#list_webhooks)
        """

    async def start_deployment(
        self, *, appId: str, branchName: str, jobId: str = ..., sourceUrl: str = ...
    ) -> StartDeploymentResultTypeDef:
        """
        Starts a deployment for a manually deployed app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.start_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#start_deployment)
        """

    async def start_job(
        self,
        *,
        appId: str,
        branchName: str,
        jobType: JobTypeType,
        jobId: str = ...,
        jobReason: str = ...,
        commitId: str = ...,
        commitMessage: str = ...,
        commitTime: Union[datetime, str] = ...
    ) -> StartJobResultTypeDef:
        """
        Starts a new job for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.start_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#start_job)
        """

    async def stop_job(self, *, appId: str, branchName: str, jobId: str) -> StopJobResultTypeDef:
        """
        Stops a job that is in progress for a branch of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.stop_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#stop_job)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#untag_resource)
        """

    async def update_app(
        self,
        *,
        appId: str,
        name: str = ...,
        description: str = ...,
        platform: PlatformType = ...,
        iamServiceRoleArn: str = ...,
        environmentVariables: Mapping[str, str] = ...,
        enableBranchAutoBuild: bool = ...,
        enableBranchAutoDeletion: bool = ...,
        enableBasicAuth: bool = ...,
        basicAuthCredentials: str = ...,
        customRules: Sequence["CustomRuleTypeDef"] = ...,
        buildSpec: str = ...,
        customHeaders: str = ...,
        enableAutoBranchCreation: bool = ...,
        autoBranchCreationPatterns: Sequence[str] = ...,
        autoBranchCreationConfig: "AutoBranchCreationConfigTypeDef" = ...,
        repository: str = ...,
        oauthToken: str = ...,
        accessToken: str = ...
    ) -> UpdateAppResultTypeDef:
        """
        Updates an existing Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.update_app)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#update_app)
        """

    async def update_branch(
        self,
        *,
        appId: str,
        branchName: str,
        description: str = ...,
        framework: str = ...,
        stage: StageType = ...,
        enableNotification: bool = ...,
        enableAutoBuild: bool = ...,
        environmentVariables: Mapping[str, str] = ...,
        basicAuthCredentials: str = ...,
        enableBasicAuth: bool = ...,
        enablePerformanceMode: bool = ...,
        buildSpec: str = ...,
        ttl: str = ...,
        displayName: str = ...,
        enablePullRequestPreview: bool = ...,
        pullRequestEnvironmentName: str = ...,
        backendEnvironmentArn: str = ...
    ) -> UpdateBranchResultTypeDef:
        """
        Updates a branch for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.update_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#update_branch)
        """

    async def update_domain_association(
        self,
        *,
        appId: str,
        domainName: str,
        enableAutoSubDomain: bool = ...,
        subDomainSettings: Sequence["SubDomainSettingTypeDef"] = ...,
        autoSubDomainCreationPatterns: Sequence[str] = ...,
        autoSubDomainIAMRole: str = ...
    ) -> UpdateDomainAssociationResultTypeDef:
        """
        Creates a new domain association for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.update_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#update_domain_association)
        """

    async def update_webhook(
        self, *, webhookId: str, branchName: str = ..., description: str = ...
    ) -> UpdateWebhookResultTypeDef:
        """
        Updates a webhook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.update_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#update_webhook)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps"]) -> ListAppsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_branches"]) -> ListBranchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_associations"]
    ) -> ListDomainAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/#get_paginator)
        """

    async def __aenter__(self) -> "AmplifyClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplify.html#Amplify.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplify/client/)
        """
