"""
Type annotations for apigateway service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigateway.client import APIGatewayClient

    session = get_session()
    async with session.create_client("apigateway") as client:
        client: APIGatewayClient
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import (
    ApiKeySourceTypeType,
    AuthorizerTypeType,
    CacheClusterSizeType,
    ConnectionTypeType,
    ContentHandlingStrategyType,
    DocumentationPartTypeType,
    GatewayResponseTypeType,
    IntegrationTypeType,
    LocationStatusTypeType,
    PutModeType,
    SecurityPolicyType,
)
from .paginator import (
    GetApiKeysPaginator,
    GetAuthorizersPaginator,
    GetBasePathMappingsPaginator,
    GetClientCertificatesPaginator,
    GetDeploymentsPaginator,
    GetDocumentationPartsPaginator,
    GetDocumentationVersionsPaginator,
    GetDomainNamesPaginator,
    GetGatewayResponsesPaginator,
    GetModelsPaginator,
    GetRequestValidatorsPaginator,
    GetResourcesPaginator,
    GetRestApisPaginator,
    GetSdkTypesPaginator,
    GetUsagePaginator,
    GetUsagePlanKeysPaginator,
    GetUsagePlansPaginator,
    GetVpcLinksPaginator,
)
from .type_defs import (
    AccountTypeDef,
    ApiKeyIdsTypeDef,
    ApiKeyResponseMetadataTypeDef,
    ApiKeysTypeDef,
    ApiStageTypeDef,
    AuthorizerResponseMetadataTypeDef,
    AuthorizersTypeDef,
    BasePathMappingResponseMetadataTypeDef,
    BasePathMappingsTypeDef,
    CanarySettingsTypeDef,
    ClientCertificateResponseMetadataTypeDef,
    ClientCertificatesTypeDef,
    DeploymentCanarySettingsTypeDef,
    DeploymentResponseMetadataTypeDef,
    DeploymentsTypeDef,
    DocumentationPartIdsTypeDef,
    DocumentationPartLocationTypeDef,
    DocumentationPartResponseMetadataTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionResponseMetadataTypeDef,
    DocumentationVersionsTypeDef,
    DomainNameResponseMetadataTypeDef,
    DomainNamesTypeDef,
    EndpointConfigurationTypeDef,
    ExportResponseTypeDef,
    GatewayResponseResponseMetadataTypeDef,
    GatewayResponsesTypeDef,
    IntegrationResponseMetadataTypeDef,
    IntegrationResponseResponseMetadataTypeDef,
    MethodResponseMetadataTypeDef,
    MethodResponseResponseMetadataTypeDef,
    ModelResponseMetadataTypeDef,
    ModelsTypeDef,
    MutualTlsAuthenticationInputTypeDef,
    PatchOperationTypeDef,
    QuotaSettingsTypeDef,
    RequestValidatorResponseMetadataTypeDef,
    RequestValidatorsTypeDef,
    ResourceResponseMetadataTypeDef,
    ResourcesTypeDef,
    RestApiResponseMetadataTypeDef,
    RestApisTypeDef,
    SdkResponseTypeDef,
    SdkTypeResponseMetadataTypeDef,
    SdkTypesTypeDef,
    StageKeyTypeDef,
    StageResponseMetadataTypeDef,
    StagesTypeDef,
    TagsTypeDef,
    TemplateTypeDef,
    TestInvokeAuthorizerResponseTypeDef,
    TestInvokeMethodResponseTypeDef,
    ThrottleSettingsTypeDef,
    TlsConfigTypeDef,
    UsagePlanKeyResponseMetadataTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlanResponseMetadataTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinkResponseMetadataTypeDef,
    VpcLinksTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("APIGatewayClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class APIGatewayClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        APIGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#can_paginate)
        """

    async def create_api_key(
        self,
        *,
        name: str = ...,
        description: str = ...,
        enabled: bool = ...,
        generateDistinctId: bool = ...,
        value: str = ...,
        stageKeys: Sequence["StageKeyTypeDef"] = ...,
        customerId: str = ...,
        tags: Mapping[str, str] = ...
    ) -> ApiKeyResponseMetadataTypeDef:
        """
        Create an  ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_api_key)
        """

    async def create_authorizer(
        self,
        *,
        restApiId: str,
        name: str,
        type: AuthorizerTypeType,
        providerARNs: Sequence[str] = ...,
        authType: str = ...,
        authorizerUri: str = ...,
        authorizerCredentials: str = ...,
        identitySource: str = ...,
        identityValidationExpression: str = ...,
        authorizerResultTtlInSeconds: int = ...
    ) -> AuthorizerResponseMetadataTypeDef:
        """
        Adds a new  Authorizer resource to an existing  RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_authorizer)
        """

    async def create_base_path_mapping(
        self, *, domainName: str, restApiId: str, basePath: str = ..., stage: str = ...
    ) -> BasePathMappingResponseMetadataTypeDef:
        """
        Creates a new  BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_base_path_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_base_path_mapping)
        """

    async def create_deployment(
        self,
        *,
        restApiId: str,
        stageName: str = ...,
        stageDescription: str = ...,
        description: str = ...,
        cacheClusterEnabled: bool = ...,
        cacheClusterSize: CacheClusterSizeType = ...,
        variables: Mapping[str, str] = ...,
        canarySettings: "DeploymentCanarySettingsTypeDef" = ...,
        tracingEnabled: bool = ...
    ) -> DeploymentResponseMetadataTypeDef:
        """
        Creates a  Deployment resource, which makes a specified  RestApi callable over
        the internet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_deployment)
        """

    async def create_documentation_part(
        self, *, restApiId: str, location: "DocumentationPartLocationTypeDef", properties: str
    ) -> DocumentationPartResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/CreateDocumentationPart).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_documentation_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_documentation_part)
        """

    async def create_documentation_version(
        self,
        *,
        restApiId: str,
        documentationVersion: str,
        stageName: str = ...,
        description: str = ...
    ) -> DocumentationVersionResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/CreateDocumentationVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_documentation_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_documentation_version)
        """

    async def create_domain_name(
        self,
        *,
        domainName: str,
        certificateName: str = ...,
        certificateBody: str = ...,
        certificatePrivateKey: str = ...,
        certificateChain: str = ...,
        certificateArn: str = ...,
        regionalCertificateName: str = ...,
        regionalCertificateArn: str = ...,
        endpointConfiguration: "EndpointConfigurationTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        securityPolicy: SecurityPolicyType = ...,
        mutualTlsAuthentication: "MutualTlsAuthenticationInputTypeDef" = ...,
        ownershipVerificationCertificateArn: str = ...
    ) -> DomainNameResponseMetadataTypeDef:
        """
        Creates a new domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_domain_name)
        """

    async def create_model(
        self,
        *,
        restApiId: str,
        name: str,
        contentType: str,
        description: str = ...,
        schema: str = ...
    ) -> ModelResponseMetadataTypeDef:
        """
        Adds a new  Model resource to an existing  RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_model)
        """

    async def create_request_validator(
        self,
        *,
        restApiId: str,
        name: str = ...,
        validateRequestBody: bool = ...,
        validateRequestParameters: bool = ...
    ) -> RequestValidatorResponseMetadataTypeDef:
        """
        Creates a  ReqeustValidator of a given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_request_validator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_request_validator)
        """

    async def create_resource(
        self, *, restApiId: str, parentId: str, pathPart: str
    ) -> ResourceResponseMetadataTypeDef:
        """
        Creates a  Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_resource)
        """

    async def create_rest_api(
        self,
        *,
        name: str,
        description: str = ...,
        version: str = ...,
        cloneFrom: str = ...,
        binaryMediaTypes: Sequence[str] = ...,
        minimumCompressionSize: int = ...,
        apiKeySource: ApiKeySourceTypeType = ...,
        endpointConfiguration: "EndpointConfigurationTypeDef" = ...,
        policy: str = ...,
        tags: Mapping[str, str] = ...,
        disableExecuteApiEndpoint: bool = ...
    ) -> RestApiResponseMetadataTypeDef:
        """
        Creates a new  RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_rest_api)
        """

    async def create_stage(
        self,
        *,
        restApiId: str,
        stageName: str,
        deploymentId: str,
        description: str = ...,
        cacheClusterEnabled: bool = ...,
        cacheClusterSize: CacheClusterSizeType = ...,
        variables: Mapping[str, str] = ...,
        documentationVersion: str = ...,
        canarySettings: "CanarySettingsTypeDef" = ...,
        tracingEnabled: bool = ...,
        tags: Mapping[str, str] = ...
    ) -> StageResponseMetadataTypeDef:
        """
        Creates a new  Stage resource that references a pre-existing  Deployment for the
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_stage)
        """

    async def create_usage_plan(
        self,
        *,
        name: str,
        description: str = ...,
        apiStages: Sequence["ApiStageTypeDef"] = ...,
        throttle: "ThrottleSettingsTypeDef" = ...,
        quota: "QuotaSettingsTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> UsagePlanResponseMetadataTypeDef:
        """
        Creates a usage plan with the throttle and quota limits, as well as the
        associated API stages, specified in the payload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_usage_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_usage_plan)
        """

    async def create_usage_plan_key(
        self, *, usagePlanId: str, keyId: str, keyType: str
    ) -> UsagePlanKeyResponseMetadataTypeDef:
        """
        Creates a usage plan key for adding an existing API key to a usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_usage_plan_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_usage_plan_key)
        """

    async def create_vpc_link(
        self,
        *,
        name: str,
        targetArns: Sequence[str],
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> VpcLinkResponseMetadataTypeDef:
        """
        Creates a VPC link, under the caller's account in a selected region, in an
        asynchronous operation that typically takes 2-4 minutes to complete and become
        operational.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.create_vpc_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#create_vpc_link)
        """

    async def delete_api_key(self, *, apiKey: str) -> None:
        """
        Deletes the  ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_api_key)
        """

    async def delete_authorizer(self, *, restApiId: str, authorizerId: str) -> None:
        """
        Deletes an existing  Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_authorizer)
        """

    async def delete_base_path_mapping(self, *, domainName: str, basePath: str) -> None:
        """
        Deletes the  BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_base_path_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_base_path_mapping)
        """

    async def delete_client_certificate(self, *, clientCertificateId: str) -> None:
        """
        Deletes the  ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_client_certificate)
        """

    async def delete_deployment(self, *, restApiId: str, deploymentId: str) -> None:
        """
        Deletes a  Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_deployment)
        """

    async def delete_documentation_part(self, *, restApiId: str, documentationPartId: str) -> None:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/DeleteDocumentationPart).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_documentation_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_documentation_part)
        """

    async def delete_documentation_version(
        self, *, restApiId: str, documentationVersion: str
    ) -> None:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/DeleteDocumentationVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_documentation_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_documentation_version)
        """

    async def delete_domain_name(self, *, domainName: str) -> None:
        """
        Deletes the  DomainName resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_domain_name)
        """

    async def delete_gateway_response(
        self, *, restApiId: str, responseType: GatewayResponseTypeType
    ) -> None:
        """
        Clears any customization of a  GatewayResponse of a specified response type on
        the given  RestApi and resets it with the default settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_gateway_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_gateway_response)
        """

    async def delete_integration(self, *, restApiId: str, resourceId: str, httpMethod: str) -> None:
        """
        Represents a delete integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_integration)
        """

    async def delete_integration_response(
        self, *, restApiId: str, resourceId: str, httpMethod: str, statusCode: str
    ) -> None:
        """
        Represents a delete integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_integration_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_integration_response)
        """

    async def delete_method(self, *, restApiId: str, resourceId: str, httpMethod: str) -> None:
        """
        Deletes an existing  Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_method)
        """

    async def delete_method_response(
        self, *, restApiId: str, resourceId: str, httpMethod: str, statusCode: str
    ) -> None:
        """
        Deletes an existing  MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_method_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_method_response)
        """

    async def delete_model(self, *, restApiId: str, modelName: str) -> None:
        """
        Deletes a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_model)
        """

    async def delete_request_validator(self, *, restApiId: str, requestValidatorId: str) -> None:
        """
        Deletes a  RequestValidator of a given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_request_validator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_request_validator)
        """

    async def delete_resource(self, *, restApiId: str, resourceId: str) -> None:
        """
        Deletes a  Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_resource)
        """

    async def delete_rest_api(self, *, restApiId: str) -> None:
        """
        Deletes the specified API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_rest_api)
        """

    async def delete_stage(self, *, restApiId: str, stageName: str) -> None:
        """
        Deletes a  Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_stage)
        """

    async def delete_usage_plan(self, *, usagePlanId: str) -> None:
        """
        Deletes a usage plan of a given plan Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_usage_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_usage_plan)
        """

    async def delete_usage_plan_key(self, *, usagePlanId: str, keyId: str) -> None:
        """
        Deletes a usage plan key and remove the underlying API key from the associated
        usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_usage_plan_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_usage_plan_key)
        """

    async def delete_vpc_link(self, *, vpcLinkId: str) -> None:
        """
        Deletes an existing  VpcLink of a specified identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.delete_vpc_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#delete_vpc_link)
        """

    async def flush_stage_authorizers_cache(self, *, restApiId: str, stageName: str) -> None:
        """
        Flushes all authorizer cache entries on a stage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.flush_stage_authorizers_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#flush_stage_authorizers_cache)
        """

    async def flush_stage_cache(self, *, restApiId: str, stageName: str) -> None:
        """
        Flushes a stage's cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.flush_stage_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#flush_stage_cache)
        """

    async def generate_client_certificate(
        self, *, description: str = ..., tags: Mapping[str, str] = ...
    ) -> ClientCertificateResponseMetadataTypeDef:
        """
        Generates a  ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.generate_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#generate_client_certificate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#generate_presigned_url)
        """

    async def get_account(self) -> AccountTypeDef:
        """
        Gets information about the current  Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_account)
        """

    async def get_api_key(
        self, *, apiKey: str, includeValue: bool = ...
    ) -> ApiKeyResponseMetadataTypeDef:
        """
        Gets information about the current  ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_api_key)
        """

    async def get_api_keys(
        self,
        *,
        position: str = ...,
        limit: int = ...,
        nameQuery: str = ...,
        customerId: str = ...,
        includeValues: bool = ...
    ) -> ApiKeysTypeDef:
        """
        Gets information about the current  ApiKeys resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_api_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_api_keys)
        """

    async def get_authorizer(
        self, *, restApiId: str, authorizerId: str
    ) -> AuthorizerResponseMetadataTypeDef:
        """
        Describe an existing  Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_authorizer)
        """

    async def get_authorizers(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> AuthorizersTypeDef:
        """
        Describe an existing  Authorizers resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_authorizers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_authorizers)
        """

    async def get_base_path_mapping(
        self, *, domainName: str, basePath: str
    ) -> BasePathMappingResponseMetadataTypeDef:
        """
        Describe a  BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_base_path_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_base_path_mapping)
        """

    async def get_base_path_mappings(
        self, *, domainName: str, position: str = ..., limit: int = ...
    ) -> BasePathMappingsTypeDef:
        """
        Represents a collection of  BasePathMapping resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_base_path_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_base_path_mappings)
        """

    async def get_client_certificate(
        self, *, clientCertificateId: str
    ) -> ClientCertificateResponseMetadataTypeDef:
        """
        Gets information about the current  ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_client_certificate)
        """

    async def get_client_certificates(
        self, *, position: str = ..., limit: int = ...
    ) -> ClientCertificatesTypeDef:
        """
        Gets a collection of  ClientCertificate resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_client_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_client_certificates)
        """

    async def get_deployment(
        self, *, restApiId: str, deploymentId: str, embed: Sequence[str] = ...
    ) -> DeploymentResponseMetadataTypeDef:
        """
        Gets information about a  Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_deployment)
        """

    async def get_deployments(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> DeploymentsTypeDef:
        """
        Gets information about a  Deployments collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_deployments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_deployments)
        """

    async def get_documentation_part(
        self, *, restApiId: str, documentationPartId: str
    ) -> DocumentationPartResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetDocumentationPart).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_documentation_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_part)
        """

    async def get_documentation_parts(
        self,
        *,
        restApiId: str,
        type: DocumentationPartTypeType = ...,
        nameQuery: str = ...,
        path: str = ...,
        position: str = ...,
        limit: int = ...,
        locationStatus: LocationStatusTypeType = ...
    ) -> DocumentationPartsTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetDocumentationParts).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_documentation_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_parts)
        """

    async def get_documentation_version(
        self, *, restApiId: str, documentationVersion: str
    ) -> DocumentationVersionResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetDocumentationVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_documentation_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_version)
        """

    async def get_documentation_versions(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> DocumentationVersionsTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetDocumentationVersions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_documentation_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_documentation_versions)
        """

    async def get_domain_name(self, *, domainName: str) -> DomainNameResponseMetadataTypeDef:
        """
        Represents a domain name that is contained in a simpler, more intuitive URL that
        can be called.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_domain_name)
        """

    async def get_domain_names(
        self, *, position: str = ..., limit: int = ...
    ) -> DomainNamesTypeDef:
        """
        Represents a collection of  DomainName resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_domain_names)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_domain_names)
        """

    async def get_export(
        self,
        *,
        restApiId: str,
        stageName: str,
        exportType: str,
        parameters: Mapping[str, str] = ...,
        accepts: str = ...
    ) -> ExportResponseTypeDef:
        """
        Exports a deployed version of a  RestApi in a specified format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_export)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_export)
        """

    async def get_gateway_response(
        self, *, restApiId: str, responseType: GatewayResponseTypeType
    ) -> GatewayResponseResponseMetadataTypeDef:
        """
        Gets a  GatewayResponse of a specified response type on the given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_gateway_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_gateway_response)
        """

    async def get_gateway_responses(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> GatewayResponsesTypeDef:
        """
        Gets the  GatewayResponses collection on the given  RestApi.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_gateway_responses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_gateway_responses)
        """

    async def get_integration(
        self, *, restApiId: str, resourceId: str, httpMethod: str
    ) -> IntegrationResponseMetadataTypeDef:
        """
        Get the integration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_integration)
        """

    async def get_integration_response(
        self, *, restApiId: str, resourceId: str, httpMethod: str, statusCode: str
    ) -> IntegrationResponseResponseMetadataTypeDef:
        """
        Represents a get integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_integration_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_integration_response)
        """

    async def get_method(
        self, *, restApiId: str, resourceId: str, httpMethod: str
    ) -> MethodResponseMetadataTypeDef:
        """
        Describe an existing  Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_method)
        """

    async def get_method_response(
        self, *, restApiId: str, resourceId: str, httpMethod: str, statusCode: str
    ) -> MethodResponseResponseMetadataTypeDef:
        """
        Describes a  MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_method_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_method_response)
        """

    async def get_model(
        self, *, restApiId: str, modelName: str, flatten: bool = ...
    ) -> ModelResponseMetadataTypeDef:
        """
        Describes an existing model defined for a  RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_model)
        """

    async def get_model_template(self, *, restApiId: str, modelName: str) -> TemplateTypeDef:
        """
        Generates a sample mapping template that can be used to transform a payload into
        the structure of a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_model_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_model_template)
        """

    async def get_models(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> ModelsTypeDef:
        """
        Describes existing  Models defined for a  RestApi resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_models)
        """

    async def get_request_validator(
        self, *, restApiId: str, requestValidatorId: str
    ) -> RequestValidatorResponseMetadataTypeDef:
        """
        Gets a  RequestValidator of a given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_request_validator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_request_validator)
        """

    async def get_request_validators(
        self, *, restApiId: str, position: str = ..., limit: int = ...
    ) -> RequestValidatorsTypeDef:
        """
        Gets the  RequestValidators collection of a given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_request_validators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_request_validators)
        """

    async def get_resource(
        self, *, restApiId: str, resourceId: str, embed: Sequence[str] = ...
    ) -> ResourceResponseMetadataTypeDef:
        """
        Lists information about a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_resource)
        """

    async def get_resources(
        self, *, restApiId: str, position: str = ..., limit: int = ..., embed: Sequence[str] = ...
    ) -> ResourcesTypeDef:
        """
        Lists information about a collection of  Resource resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_resources)
        """

    async def get_rest_api(self, *, restApiId: str) -> RestApiResponseMetadataTypeDef:
        """
        Lists the  RestApi resource in the collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_rest_api)
        """

    async def get_rest_apis(self, *, position: str = ..., limit: int = ...) -> RestApisTypeDef:
        """
        Lists the  RestApis resources for your collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_rest_apis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_rest_apis)
        """

    async def get_sdk(
        self, *, restApiId: str, stageName: str, sdkType: str, parameters: Mapping[str, str] = ...
    ) -> SdkResponseTypeDef:
        """
        Generates a client SDK for a  RestApi and  Stage .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_sdk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk)
        """

    async def get_sdk_type(self, *, id: str) -> SdkTypeResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetSdkType).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_sdk_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk_type)
        """

    async def get_sdk_types(self, *, position: str = ..., limit: int = ...) -> SdkTypesTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/GetSdkTypes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_sdk_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_sdk_types)
        """

    async def get_stage(self, *, restApiId: str, stageName: str) -> StageResponseMetadataTypeDef:
        """
        Gets information about a  Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_stage)
        """

    async def get_stages(self, *, restApiId: str, deploymentId: str = ...) -> StagesTypeDef:
        """
        Gets information about one or more  Stage resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_stages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_stages)
        """

    async def get_tags(
        self, *, resourceArn: str, position: str = ..., limit: int = ...
    ) -> TagsTypeDef:
        """
        Gets the  Tags collection for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_tags)
        """

    async def get_usage(
        self,
        *,
        usagePlanId: str,
        startDate: str,
        endDate: str,
        keyId: str = ...,
        position: str = ...,
        limit: int = ...
    ) -> UsageTypeDef:
        """
        Gets the usage data of a usage plan in a specified time interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage)
        """

    async def get_usage_plan(self, *, usagePlanId: str) -> UsagePlanResponseMetadataTypeDef:
        """
        Gets a usage plan of a given plan identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_usage_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan)
        """

    async def get_usage_plan_key(
        self, *, usagePlanId: str, keyId: str
    ) -> UsagePlanKeyResponseMetadataTypeDef:
        """
        Gets a usage plan key of a given key identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_usage_plan_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan_key)
        """

    async def get_usage_plan_keys(
        self, *, usagePlanId: str, position: str = ..., limit: int = ..., nameQuery: str = ...
    ) -> UsagePlanKeysTypeDef:
        """
        Gets all the usage plan keys representing the API keys added to a specified
        usage plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_usage_plan_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plan_keys)
        """

    async def get_usage_plans(
        self, *, position: str = ..., keyId: str = ..., limit: int = ...
    ) -> UsagePlansTypeDef:
        """
        Gets all the usage plans of the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_usage_plans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_usage_plans)
        """

    async def get_vpc_link(self, *, vpcLinkId: str) -> VpcLinkResponseMetadataTypeDef:
        """
        Gets a specified VPC link under the caller's account in a region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_vpc_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_vpc_link)
        """

    async def get_vpc_links(self, *, position: str = ..., limit: int = ...) -> VpcLinksTypeDef:
        """
        Gets the  VpcLinks collection under the caller's account in a selected region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_vpc_links)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_vpc_links)
        """

    async def import_api_keys(
        self,
        *,
        body: Union[str, bytes, IO[Any], StreamingBody],
        format: Literal["csv"],
        failOnWarnings: bool = ...
    ) -> ApiKeyIdsTypeDef:
        """
        Import API keys from an external source, such as a CSV-formatted file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.import_api_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_api_keys)
        """

    async def import_documentation_parts(
        self,
        *,
        restApiId: str,
        body: Union[str, bytes, IO[Any], StreamingBody],
        mode: PutModeType = ...,
        failOnWarnings: bool = ...
    ) -> DocumentationPartIdsTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/ImportDocumentationParts).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.import_documentation_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_documentation_parts)
        """

    async def import_rest_api(
        self,
        *,
        body: Union[str, bytes, IO[Any], StreamingBody],
        failOnWarnings: bool = ...,
        parameters: Mapping[str, str] = ...
    ) -> RestApiResponseMetadataTypeDef:
        """
        A feature of the API Gateway control service for creating a new API from an
        external API definition file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.import_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#import_rest_api)
        """

    async def put_gateway_response(
        self,
        *,
        restApiId: str,
        responseType: GatewayResponseTypeType,
        statusCode: str = ...,
        responseParameters: Mapping[str, str] = ...,
        responseTemplates: Mapping[str, str] = ...
    ) -> GatewayResponseResponseMetadataTypeDef:
        """
        Creates a customization of a  GatewayResponse of a specified response type and
        status code on the given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_gateway_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_gateway_response)
        """

    async def put_integration(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        type: IntegrationTypeType,
        integrationHttpMethod: str = ...,
        uri: str = ...,
        connectionType: ConnectionTypeType = ...,
        connectionId: str = ...,
        credentials: str = ...,
        requestParameters: Mapping[str, str] = ...,
        requestTemplates: Mapping[str, str] = ...,
        passthroughBehavior: str = ...,
        cacheNamespace: str = ...,
        cacheKeyParameters: Sequence[str] = ...,
        contentHandling: ContentHandlingStrategyType = ...,
        timeoutInMillis: int = ...,
        tlsConfig: "TlsConfigTypeDef" = ...
    ) -> IntegrationResponseMetadataTypeDef:
        """
        Sets up a method's integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_integration)
        """

    async def put_integration_response(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        statusCode: str,
        selectionPattern: str = ...,
        responseParameters: Mapping[str, str] = ...,
        responseTemplates: Mapping[str, str] = ...,
        contentHandling: ContentHandlingStrategyType = ...
    ) -> IntegrationResponseResponseMetadataTypeDef:
        """
        Represents a put integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_integration_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_integration_response)
        """

    async def put_method(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        authorizationType: str,
        authorizerId: str = ...,
        apiKeyRequired: bool = ...,
        operationName: str = ...,
        requestParameters: Mapping[str, bool] = ...,
        requestModels: Mapping[str, str] = ...,
        requestValidatorId: str = ...,
        authorizationScopes: Sequence[str] = ...
    ) -> MethodResponseMetadataTypeDef:
        """
        Add a method to an existing  Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_method)
        """

    async def put_method_response(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        statusCode: str,
        responseParameters: Mapping[str, bool] = ...,
        responseModels: Mapping[str, str] = ...
    ) -> MethodResponseResponseMetadataTypeDef:
        """
        Adds a  MethodResponse to an existing  Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_method_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_method_response)
        """

    async def put_rest_api(
        self,
        *,
        restApiId: str,
        body: Union[str, bytes, IO[Any], StreamingBody],
        mode: PutModeType = ...,
        failOnWarnings: bool = ...,
        parameters: Mapping[str, str] = ...
    ) -> RestApiResponseMetadataTypeDef:
        """
        A feature of the API Gateway control service for updating an existing API with
        an input of external API definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.put_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#put_rest_api)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> None:
        """
        Adds or updates a tag on a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#tag_resource)
        """

    async def test_invoke_authorizer(
        self,
        *,
        restApiId: str,
        authorizerId: str,
        headers: Mapping[str, str] = ...,
        multiValueHeaders: Mapping[str, Sequence[str]] = ...,
        pathWithQueryString: str = ...,
        body: str = ...,
        stageVariables: Mapping[str, str] = ...,
        additionalContext: Mapping[str, str] = ...
    ) -> TestInvokeAuthorizerResponseTypeDef:
        """
        Simulate the execution of an  Authorizer in your  RestApi with headers,
        parameters, and an incoming request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.test_invoke_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#test_invoke_authorizer)
        """

    async def test_invoke_method(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        pathWithQueryString: str = ...,
        body: str = ...,
        headers: Mapping[str, str] = ...,
        multiValueHeaders: Mapping[str, Sequence[str]] = ...,
        clientCertificateId: str = ...,
        stageVariables: Mapping[str, str] = ...
    ) -> TestInvokeMethodResponseTypeDef:
        """
        Simulate the execution of a  Method in your  RestApi with headers, parameters,
        and an incoming request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.test_invoke_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#test_invoke_method)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> None:
        """
        Removes a tag from a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#untag_resource)
        """

    async def update_account(
        self, *, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> AccountTypeDef:
        """
        Changes information about the current  Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_account)
        """

    async def update_api_key(
        self, *, apiKey: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> ApiKeyResponseMetadataTypeDef:
        """
        Changes information about an  ApiKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_api_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_api_key)
        """

    async def update_authorizer(
        self,
        *,
        restApiId: str,
        authorizerId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> AuthorizerResponseMetadataTypeDef:
        """
        Updates an existing  Authorizer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_authorizer)
        """

    async def update_base_path_mapping(
        self,
        *,
        domainName: str,
        basePath: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> BasePathMappingResponseMetadataTypeDef:
        """
        Changes information about the  BasePathMapping resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_base_path_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_base_path_mapping)
        """

    async def update_client_certificate(
        self, *, clientCertificateId: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> ClientCertificateResponseMetadataTypeDef:
        """
        Changes information about an  ClientCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_client_certificate)
        """

    async def update_deployment(
        self,
        *,
        restApiId: str,
        deploymentId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> DeploymentResponseMetadataTypeDef:
        """
        Changes information about a  Deployment resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_deployment)
        """

    async def update_documentation_part(
        self,
        *,
        restApiId: str,
        documentationPartId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> DocumentationPartResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/UpdateDocumentationPart).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_documentation_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_documentation_part)
        """

    async def update_documentation_version(
        self,
        *,
        restApiId: str,
        documentationVersion: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> DocumentationVersionResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/apigateway-2015-07-09/UpdateDocumentationVersion).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_documentation_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_documentation_version)
        """

    async def update_domain_name(
        self, *, domainName: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> DomainNameResponseMetadataTypeDef:
        """
        Changes information about the  DomainName resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_domain_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_domain_name)
        """

    async def update_gateway_response(
        self,
        *,
        restApiId: str,
        responseType: GatewayResponseTypeType,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> GatewayResponseResponseMetadataTypeDef:
        """
        Updates a  GatewayResponse of a specified response type on the given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_gateway_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_gateway_response)
        """

    async def update_integration(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> IntegrationResponseMetadataTypeDef:
        """
        Represents an update integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_integration)
        """

    async def update_integration_response(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        statusCode: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> IntegrationResponseResponseMetadataTypeDef:
        """
        Represents an update integration response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_integration_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_integration_response)
        """

    async def update_method(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> MethodResponseMetadataTypeDef:
        """
        Updates an existing  Method resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_method)
        """

    async def update_method_response(
        self,
        *,
        restApiId: str,
        resourceId: str,
        httpMethod: str,
        statusCode: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> MethodResponseResponseMetadataTypeDef:
        """
        Updates an existing  MethodResponse resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_method_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_method_response)
        """

    async def update_model(
        self,
        *,
        restApiId: str,
        modelName: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> ModelResponseMetadataTypeDef:
        """
        Changes information about a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_model)
        """

    async def update_request_validator(
        self,
        *,
        restApiId: str,
        requestValidatorId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> RequestValidatorResponseMetadataTypeDef:
        """
        Updates a  RequestValidator of a given  RestApi .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_request_validator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_request_validator)
        """

    async def update_resource(
        self,
        *,
        restApiId: str,
        resourceId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> ResourceResponseMetadataTypeDef:
        """
        Changes information about a  Resource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_resource)
        """

    async def update_rest_api(
        self, *, restApiId: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> RestApiResponseMetadataTypeDef:
        """
        Changes information about the specified API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_rest_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_rest_api)
        """

    async def update_stage(
        self,
        *,
        restApiId: str,
        stageName: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> StageResponseMetadataTypeDef:
        """
        Changes information about a  Stage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_stage)
        """

    async def update_usage(
        self,
        *,
        usagePlanId: str,
        keyId: str,
        patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> UsageTypeDef:
        """
        Grants a temporary extension to the remaining quota of a usage plan associated
        with a specified API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_usage)
        """

    async def update_usage_plan(
        self, *, usagePlanId: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> UsagePlanResponseMetadataTypeDef:
        """
        Updates a usage plan of a given plan Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_usage_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_usage_plan)
        """

    async def update_vpc_link(
        self, *, vpcLinkId: str, patchOperations: Sequence["PatchOperationTypeDef"] = ...
    ) -> VpcLinkResponseMetadataTypeDef:
        """
        Updates an existing  VpcLink of a specified identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.update_vpc_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#update_vpc_link)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_api_keys"]) -> GetApiKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_authorizers"]) -> GetAuthorizersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_base_path_mappings"]
    ) -> GetBasePathMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_client_certificates"]
    ) -> GetClientCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_deployments"]) -> GetDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_documentation_parts"]
    ) -> GetDocumentationPartsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_documentation_versions"]
    ) -> GetDocumentationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domain_names"]) -> GetDomainNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_gateway_responses"]
    ) -> GetGatewayResponsesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_models"]) -> GetModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_request_validators"]
    ) -> GetRequestValidatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_resources"]) -> GetResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_rest_apis"]) -> GetRestApisPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_sdk_types"]) -> GetSdkTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_usage"]) -> GetUsagePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_usage_plan_keys"]
    ) -> GetUsagePlanKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_usage_plans"]) -> GetUsagePlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_vpc_links"]) -> GetVpcLinksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/#get_paginator)
        """

    async def __aenter__(self) -> "APIGatewayClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway.html#APIGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigateway/client/)
        """
