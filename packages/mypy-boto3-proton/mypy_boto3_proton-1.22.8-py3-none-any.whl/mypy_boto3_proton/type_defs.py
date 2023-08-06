"""
Type annotations for proton service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_proton/type_defs/)

Usage::

    ```python
    from mypy_boto3_proton.type_defs import AcceptEnvironmentAccountConnectionInputRequestTypeDef

    data: AcceptEnvironmentAccountConnectionInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    DeploymentStatusType,
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    ProvisionedResourceEngineType,
    RepositoryProviderType,
    RepositorySyncStatusType,
    ResourceDeploymentStatusType,
    ResourceSyncStatusType,
    ServiceStatusType,
    TemplateTypeType,
    TemplateVersionStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    "AcceptEnvironmentAccountConnectionOutputTypeDef",
    "AccountSettingsTypeDef",
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    "CancelEnvironmentDeploymentOutputTypeDef",
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    "CancelServiceInstanceDeploymentOutputTypeDef",
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    "CancelServicePipelineDeploymentOutputTypeDef",
    "CompatibleEnvironmentTemplateInputTypeDef",
    "CompatibleEnvironmentTemplateTypeDef",
    "CreateEnvironmentAccountConnectionInputRequestTypeDef",
    "CreateEnvironmentAccountConnectionOutputTypeDef",
    "CreateEnvironmentInputRequestTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateEnvironmentTemplateInputRequestTypeDef",
    "CreateEnvironmentTemplateOutputTypeDef",
    "CreateEnvironmentTemplateVersionInputRequestTypeDef",
    "CreateEnvironmentTemplateVersionOutputTypeDef",
    "CreateRepositoryInputRequestTypeDef",
    "CreateRepositoryOutputTypeDef",
    "CreateServiceInputRequestTypeDef",
    "CreateServiceOutputTypeDef",
    "CreateServiceTemplateInputRequestTypeDef",
    "CreateServiceTemplateOutputTypeDef",
    "CreateServiceTemplateVersionInputRequestTypeDef",
    "CreateServiceTemplateVersionOutputTypeDef",
    "CreateTemplateSyncConfigInputRequestTypeDef",
    "CreateTemplateSyncConfigOutputTypeDef",
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    "DeleteEnvironmentAccountConnectionOutputTypeDef",
    "DeleteEnvironmentInputRequestTypeDef",
    "DeleteEnvironmentOutputTypeDef",
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    "DeleteEnvironmentTemplateOutputTypeDef",
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    "DeleteEnvironmentTemplateVersionOutputTypeDef",
    "DeleteRepositoryInputRequestTypeDef",
    "DeleteRepositoryOutputTypeDef",
    "DeleteServiceInputRequestTypeDef",
    "DeleteServiceOutputTypeDef",
    "DeleteServiceTemplateInputRequestTypeDef",
    "DeleteServiceTemplateOutputTypeDef",
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    "DeleteServiceTemplateVersionOutputTypeDef",
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    "DeleteTemplateSyncConfigOutputTypeDef",
    "EnvironmentAccountConnectionSummaryTypeDef",
    "EnvironmentAccountConnectionTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentTemplateFilterTypeDef",
    "EnvironmentTemplateSummaryTypeDef",
    "EnvironmentTemplateTypeDef",
    "EnvironmentTemplateVersionSummaryTypeDef",
    "EnvironmentTemplateVersionTypeDef",
    "EnvironmentTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    "GetEnvironmentAccountConnectionOutputTypeDef",
    "GetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    "GetEnvironmentInputRequestTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetEnvironmentTemplateInputRequestTypeDef",
    "GetEnvironmentTemplateOutputTypeDef",
    "GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    "GetEnvironmentTemplateVersionOutputTypeDef",
    "GetRepositoryInputRequestTypeDef",
    "GetRepositoryOutputTypeDef",
    "GetRepositorySyncStatusInputRequestTypeDef",
    "GetRepositorySyncStatusOutputTypeDef",
    "GetServiceInputRequestTypeDef",
    "GetServiceInputServiceCreatedWaitTypeDef",
    "GetServiceInputServiceDeletedWaitTypeDef",
    "GetServiceInputServicePipelineDeployedWaitTypeDef",
    "GetServiceInputServiceUpdatedWaitTypeDef",
    "GetServiceInstanceInputRequestTypeDef",
    "GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    "GetServiceInstanceOutputTypeDef",
    "GetServiceOutputTypeDef",
    "GetServiceTemplateInputRequestTypeDef",
    "GetServiceTemplateOutputTypeDef",
    "GetServiceTemplateVersionInputRequestTypeDef",
    "GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    "GetServiceTemplateVersionOutputTypeDef",
    "GetTemplateSyncConfigInputRequestTypeDef",
    "GetTemplateSyncConfigOutputTypeDef",
    "GetTemplateSyncStatusInputRequestTypeDef",
    "GetTemplateSyncStatusOutputTypeDef",
    "ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    "ListEnvironmentAccountConnectionsInputRequestTypeDef",
    "ListEnvironmentAccountConnectionsOutputTypeDef",
    "ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    "ListEnvironmentOutputsInputRequestTypeDef",
    "ListEnvironmentOutputsOutputTypeDef",
    "ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    "ListEnvironmentProvisionedResourcesInputRequestTypeDef",
    "ListEnvironmentProvisionedResourcesOutputTypeDef",
    "ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    "ListEnvironmentTemplateVersionsInputRequestTypeDef",
    "ListEnvironmentTemplateVersionsOutputTypeDef",
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    "ListEnvironmentTemplatesInputRequestTypeDef",
    "ListEnvironmentTemplatesOutputTypeDef",
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsInputRequestTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    "ListRepositoriesInputRequestTypeDef",
    "ListRepositoriesOutputTypeDef",
    "ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    "ListRepositorySyncDefinitionsInputRequestTypeDef",
    "ListRepositorySyncDefinitionsOutputTypeDef",
    "ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    "ListServiceInstanceOutputsInputRequestTypeDef",
    "ListServiceInstanceOutputsOutputTypeDef",
    "ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    "ListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    "ListServiceInstanceProvisionedResourcesOutputTypeDef",
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    "ListServiceInstancesInputRequestTypeDef",
    "ListServiceInstancesOutputTypeDef",
    "ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    "ListServicePipelineOutputsInputRequestTypeDef",
    "ListServicePipelineOutputsOutputTypeDef",
    "ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    "ListServicePipelineProvisionedResourcesInputRequestTypeDef",
    "ListServicePipelineProvisionedResourcesOutputTypeDef",
    "ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    "ListServiceTemplateVersionsInputRequestTypeDef",
    "ListServiceTemplateVersionsOutputTypeDef",
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    "ListServiceTemplatesInputRequestTypeDef",
    "ListServiceTemplatesOutputTypeDef",
    "ListServicesInputListServicesPaginateTypeDef",
    "ListServicesInputRequestTypeDef",
    "ListServicesOutputTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    "OutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProvisionedResourceTypeDef",
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    "RejectEnvironmentAccountConnectionOutputTypeDef",
    "RepositoryBranchInputTypeDef",
    "RepositoryBranchTypeDef",
    "RepositorySummaryTypeDef",
    "RepositorySyncAttemptTypeDef",
    "RepositorySyncDefinitionTypeDef",
    "RepositorySyncEventTypeDef",
    "RepositoryTypeDef",
    "ResourceSyncAttemptTypeDef",
    "ResourceSyncEventTypeDef",
    "ResponseMetadataTypeDef",
    "RevisionTypeDef",
    "S3ObjectSourceTypeDef",
    "ServiceInstanceSummaryTypeDef",
    "ServiceInstanceTypeDef",
    "ServicePipelineTypeDef",
    "ServiceSummaryTypeDef",
    "ServiceTemplateSummaryTypeDef",
    "ServiceTemplateTypeDef",
    "ServiceTemplateVersionSummaryTypeDef",
    "ServiceTemplateVersionTypeDef",
    "ServiceTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagTypeDef",
    "TemplateSyncConfigTypeDef",
    "TemplateVersionSourceInputTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    "UpdateEnvironmentAccountConnectionOutputTypeDef",
    "UpdateEnvironmentInputRequestTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateEnvironmentTemplateInputRequestTypeDef",
    "UpdateEnvironmentTemplateOutputTypeDef",
    "UpdateEnvironmentTemplateVersionInputRequestTypeDef",
    "UpdateEnvironmentTemplateVersionOutputTypeDef",
    "UpdateServiceInputRequestTypeDef",
    "UpdateServiceInstanceInputRequestTypeDef",
    "UpdateServiceInstanceOutputTypeDef",
    "UpdateServiceOutputTypeDef",
    "UpdateServicePipelineInputRequestTypeDef",
    "UpdateServicePipelineOutputTypeDef",
    "UpdateServiceTemplateInputRequestTypeDef",
    "UpdateServiceTemplateOutputTypeDef",
    "UpdateServiceTemplateVersionInputRequestTypeDef",
    "UpdateServiceTemplateVersionOutputTypeDef",
    "UpdateTemplateSyncConfigInputRequestTypeDef",
    "UpdateTemplateSyncConfigOutputTypeDef",
    "WaiterConfigTypeDef",
)

AcceptEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

AcceptEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "AcceptEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "pipelineProvisioningRepository": "RepositoryBranchTypeDef",
        "pipelineServiceRoleArn": str,
    },
    total=False,
)

CancelEnvironmentDeploymentInputRequestTypeDef = TypedDict(
    "CancelEnvironmentDeploymentInputRequestTypeDef",
    {
        "environmentName": str,
    },
)

CancelEnvironmentDeploymentOutputTypeDef = TypedDict(
    "CancelEnvironmentDeploymentOutputTypeDef",
    {
        "environment": "EnvironmentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelServiceInstanceDeploymentInputRequestTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)

CancelServiceInstanceDeploymentOutputTypeDef = TypedDict(
    "CancelServiceInstanceDeploymentOutputTypeDef",
    {
        "serviceInstance": "ServiceInstanceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelServicePipelineDeploymentInputRequestTypeDef = TypedDict(
    "CancelServicePipelineDeploymentInputRequestTypeDef",
    {
        "serviceName": str,
    },
)

CancelServicePipelineDeploymentOutputTypeDef = TypedDict(
    "CancelServicePipelineDeploymentOutputTypeDef",
    {
        "pipeline": "ServicePipelineTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompatibleEnvironmentTemplateInputTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateInputTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

CompatibleEnvironmentTemplateTypeDef = TypedDict(
    "CompatibleEnvironmentTemplateTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "environmentName": str,
        "managementAccountId": str,
        "roleArn": str,
    },
)
_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "clientToken": str,
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateEnvironmentAccountConnectionInputRequestTypeDef(
    _RequiredCreateEnvironmentAccountConnectionInputRequestTypeDef,
    _OptionalCreateEnvironmentAccountConnectionInputRequestTypeDef,
):
    pass


CreateEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "CreateEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentInputRequestTypeDef",
    {
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": "RepositoryBranchInputTypeDef",
        "tags": Sequence["TagTypeDef"],
        "templateMinorVersion": str,
    },
    total=False,
)


class CreateEnvironmentInputRequestTypeDef(
    _RequiredCreateEnvironmentInputRequestTypeDef, _OptionalCreateEnvironmentInputRequestTypeDef
):
    pass


CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "environment": "EnvironmentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateEnvironmentTemplateInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateInputRequestTypeDef,
):
    pass


CreateEnvironmentTemplateOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": "EnvironmentTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "source": "TemplateVersionSourceInputTypeDef",
        "templateName": str,
    },
)
_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredCreateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalCreateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass


CreateEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "CreateEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": "EnvironmentTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateRepositoryInputRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryInputRequestTypeDef",
    {
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)
_OptionalCreateRepositoryInputRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryInputRequestTypeDef",
    {
        "encryptionKey": str,
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateRepositoryInputRequestTypeDef(
    _RequiredCreateRepositoryInputRequestTypeDef, _OptionalCreateRepositoryInputRequestTypeDef
):
    pass


CreateRepositoryOutputTypeDef = TypedDict(
    "CreateRepositoryOutputTypeDef",
    {
        "repository": "RepositoryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateServiceInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceInputRequestTypeDef",
    {
        "name": str,
        "spec": str,
        "templateMajorVersion": str,
        "templateName": str,
    },
)
_OptionalCreateServiceInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceInputRequestTypeDef",
    {
        "branchName": str,
        "description": str,
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "tags": Sequence["TagTypeDef"],
        "templateMinorVersion": str,
    },
    total=False,
)


class CreateServiceInputRequestTypeDef(
    _RequiredCreateServiceInputRequestTypeDef, _OptionalCreateServiceInputRequestTypeDef
):
    pass


CreateServiceOutputTypeDef = TypedDict(
    "CreateServiceOutputTypeDef",
    {
        "service": "ServiceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateServiceTemplateInputRequestTypeDef(
    _RequiredCreateServiceTemplateInputRequestTypeDef,
    _OptionalCreateServiceTemplateInputRequestTypeDef,
):
    pass


CreateServiceTemplateOutputTypeDef = TypedDict(
    "CreateServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": "ServiceTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence["CompatibleEnvironmentTemplateInputTypeDef"],
        "source": "TemplateVersionSourceInputTypeDef",
        "templateName": str,
    },
)
_OptionalCreateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalCreateServiceTemplateVersionInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "majorVersion": str,
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateServiceTemplateVersionInputRequestTypeDef(
    _RequiredCreateServiceTemplateVersionInputRequestTypeDef,
    _OptionalCreateServiceTemplateVersionInputRequestTypeDef,
):
    pass


CreateServiceTemplateVersionOutputTypeDef = TypedDict(
    "CreateServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": "ServiceTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalCreateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)


class CreateTemplateSyncConfigInputRequestTypeDef(
    _RequiredCreateTemplateSyncConfigInputRequestTypeDef,
    _OptionalCreateTemplateSyncConfigInputRequestTypeDef,
):
    pass


CreateTemplateSyncConfigOutputTypeDef = TypedDict(
    "CreateTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": "TemplateSyncConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

DeleteEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "DeleteEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentOutputTypeDef = TypedDict(
    "DeleteEnvironmentOutputTypeDef",
    {
        "environment": "EnvironmentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteEnvironmentTemplateOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": "EnvironmentTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "DeleteEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": "EnvironmentTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteRepositoryInputRequestTypeDef = TypedDict(
    "DeleteRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

DeleteRepositoryOutputTypeDef = TypedDict(
    "DeleteRepositoryOutputTypeDef",
    {
        "repository": "RepositoryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceInputRequestTypeDef = TypedDict(
    "DeleteServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceOutputTypeDef = TypedDict(
    "DeleteServiceOutputTypeDef",
    {
        "service": "ServiceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceTemplateInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

DeleteServiceTemplateOutputTypeDef = TypedDict(
    "DeleteServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": "ServiceTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "DeleteServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

DeleteServiceTemplateVersionOutputTypeDef = TypedDict(
    "DeleteServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": "ServiceTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "DeleteTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

DeleteTemplateSyncConfigOutputTypeDef = TypedDict(
    "DeleteTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": "TemplateSyncConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnvironmentAccountConnectionSummaryTypeDef = TypedDict(
    "EnvironmentAccountConnectionSummaryTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)

EnvironmentAccountConnectionTypeDef = TypedDict(
    "EnvironmentAccountConnectionTypeDef",
    {
        "arn": str,
        "environmentAccountId": str,
        "environmentName": str,
        "id": str,
        "lastModifiedAt": datetime,
        "managementAccountId": str,
        "requestedAt": datetime,
        "roleArn": str,
        "status": EnvironmentAccountConnectionStatusType,
    },
)

_RequiredEnvironmentSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalEnvironmentSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentSummaryTypeDef",
    {
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
    },
    total=False,
)


class EnvironmentSummaryTypeDef(
    _RequiredEnvironmentSummaryTypeDef, _OptionalEnvironmentSummaryTypeDef
):
    pass


EnvironmentTemplateFilterTypeDef = TypedDict(
    "EnvironmentTemplateFilterTypeDef",
    {
        "majorVersion": str,
        "templateName": str,
    },
)

_RequiredEnvironmentTemplateSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalEnvironmentTemplateSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateSummaryTypeDef",
    {
        "description": str,
        "displayName": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)


class EnvironmentTemplateSummaryTypeDef(
    _RequiredEnvironmentTemplateSummaryTypeDef, _OptionalEnvironmentTemplateSummaryTypeDef
):
    pass


_RequiredEnvironmentTemplateTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalEnvironmentTemplateTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)


class EnvironmentTemplateTypeDef(
    _RequiredEnvironmentTemplateTypeDef, _OptionalEnvironmentTemplateTypeDef
):
    pass


_RequiredEnvironmentTemplateVersionSummaryTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalEnvironmentTemplateVersionSummaryTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateVersionSummaryTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "statusMessage": str,
    },
    total=False,
)


class EnvironmentTemplateVersionSummaryTypeDef(
    _RequiredEnvironmentTemplateVersionSummaryTypeDef,
    _OptionalEnvironmentTemplateVersionSummaryTypeDef,
):
    pass


_RequiredEnvironmentTemplateVersionTypeDef = TypedDict(
    "_RequiredEnvironmentTemplateVersionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalEnvironmentTemplateVersionTypeDef = TypedDict(
    "_OptionalEnvironmentTemplateVersionTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "statusMessage": str,
    },
    total=False,
)


class EnvironmentTemplateVersionTypeDef(
    _RequiredEnvironmentTemplateVersionTypeDef, _OptionalEnvironmentTemplateVersionTypeDef
):
    pass


_RequiredEnvironmentTypeDef = TypedDict(
    "_RequiredEnvironmentTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalEnvironmentTypeDef = TypedDict(
    "_OptionalEnvironmentTypeDef",
    {
        "deploymentStatusMessage": str,
        "description": str,
        "environmentAccountConnectionId": str,
        "environmentAccountId": str,
        "protonServiceRoleArn": str,
        "provisioning": Literal["CUSTOMER_MANAGED"],
        "provisioningRepository": "RepositoryBranchTypeDef",
        "spec": str,
    },
    total=False,
)


class EnvironmentTypeDef(_RequiredEnvironmentTypeDef, _OptionalEnvironmentTypeDef):
    pass


GetAccountSettingsOutputTypeDef = TypedDict(
    "GetAccountSettingsOutputTypeDef",
    {
        "accountSettings": "AccountSettingsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

GetEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "GetEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetEnvironmentInputEnvironmentDeployedWaitTypeDef(
    _RequiredGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
    _OptionalGetEnvironmentInputEnvironmentDeployedWaitTypeDef,
):
    pass


GetEnvironmentInputRequestTypeDef = TypedDict(
    "GetEnvironmentInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "environment": "EnvironmentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetEnvironmentTemplateOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": "EnvironmentTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetEnvironmentTemplateVersionInputEnvironmentTemplateVersionRegisteredWaitTypeDef,
):
    pass


GetEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

GetEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "GetEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": "EnvironmentTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRepositoryInputRequestTypeDef = TypedDict(
    "GetRepositoryInputRequestTypeDef",
    {
        "name": str,
        "provider": RepositoryProviderType,
    },
)

GetRepositoryOutputTypeDef = TypedDict(
    "GetRepositoryOutputTypeDef",
    {
        "repository": "RepositoryTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRepositorySyncStatusInputRequestTypeDef = TypedDict(
    "GetRepositorySyncStatusInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)

GetRepositorySyncStatusOutputTypeDef = TypedDict(
    "GetRepositorySyncStatusOutputTypeDef",
    {
        "latestSync": "RepositorySyncAttemptTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceInputRequestTypeDef = TypedDict(
    "GetServiceInputRequestTypeDef",
    {
        "name": str,
    },
)

_RequiredGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceCreatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceCreatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceCreatedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceInputServiceCreatedWaitTypeDef(
    _RequiredGetServiceInputServiceCreatedWaitTypeDef,
    _OptionalGetServiceInputServiceCreatedWaitTypeDef,
):
    pass


_RequiredGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceDeletedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceDeletedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceInputServiceDeletedWaitTypeDef(
    _RequiredGetServiceInputServiceDeletedWaitTypeDef,
    _OptionalGetServiceInputServiceDeletedWaitTypeDef,
):
    pass


_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServicePipelineDeployedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceInputServicePipelineDeployedWaitTypeDef(
    _RequiredGetServiceInputServicePipelineDeployedWaitTypeDef,
    _OptionalGetServiceInputServicePipelineDeployedWaitTypeDef,
):
    pass


_RequiredGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "name": str,
    },
)
_OptionalGetServiceInputServiceUpdatedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInputServiceUpdatedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceInputServiceUpdatedWaitTypeDef(
    _RequiredGetServiceInputServiceUpdatedWaitTypeDef,
    _OptionalGetServiceInputServiceUpdatedWaitTypeDef,
):
    pass


GetServiceInstanceInputRequestTypeDef = TypedDict(
    "GetServiceInstanceInputRequestTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)

_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "name": str,
        "serviceName": str,
    },
)
_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef = TypedDict(
    "_OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceInstanceInputServiceInstanceDeployedWaitTypeDef(
    _RequiredGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
    _OptionalGetServiceInstanceInputServiceInstanceDeployedWaitTypeDef,
):
    pass


GetServiceInstanceOutputTypeDef = TypedDict(
    "GetServiceInstanceOutputTypeDef",
    {
        "serviceInstance": "ServiceInstanceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceOutputTypeDef = TypedDict(
    "GetServiceOutputTypeDef",
    {
        "service": "ServiceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceTemplateInputRequestTypeDef = TypedDict(
    "GetServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)

GetServiceTemplateOutputTypeDef = TypedDict(
    "GetServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": "ServiceTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "GetServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)

_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef = TypedDict(
    "_OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef(
    _RequiredGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
    _OptionalGetServiceTemplateVersionInputServiceTemplateVersionRegisteredWaitTypeDef,
):
    pass


GetServiceTemplateVersionOutputTypeDef = TypedDict(
    "GetServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": "ServiceTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "GetTemplateSyncConfigInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)

GetTemplateSyncConfigOutputTypeDef = TypedDict(
    "GetTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": "TemplateSyncConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTemplateSyncStatusInputRequestTypeDef = TypedDict(
    "GetTemplateSyncStatusInputRequestTypeDef",
    {
        "templateName": str,
        "templateType": TemplateTypeType,
        "templateVersion": str,
    },
)

GetTemplateSyncStatusOutputTypeDef = TypedDict(
    "GetTemplateSyncStatusOutputTypeDef",
    {
        "desiredState": "RevisionTypeDef",
        "latestSuccessfulSync": "ResourceSyncAttemptTypeDef",
        "latestSync": "ResourceSyncAttemptTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef",
    {
        "environmentName": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputListEnvironmentAccountConnectionsPaginateTypeDef,
):
    pass


_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "requestedBy": EnvironmentAccountConnectionRequesterAccountTypeType,
    },
)
_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentAccountConnectionsInputRequestTypeDef",
    {
        "environmentName": str,
        "maxResults": int,
        "nextToken": str,
        "statuses": Sequence[EnvironmentAccountConnectionStatusType],
    },
    total=False,
)


class ListEnvironmentAccountConnectionsInputRequestTypeDef(
    _RequiredListEnvironmentAccountConnectionsInputRequestTypeDef,
    _OptionalListEnvironmentAccountConnectionsInputRequestTypeDef,
):
    pass


ListEnvironmentAccountConnectionsOutputTypeDef = TypedDict(
    "ListEnvironmentAccountConnectionsOutputTypeDef",
    {
        "environmentAccountConnections": List["EnvironmentAccountConnectionSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef(
    _RequiredListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
    _OptionalListEnvironmentOutputsInputListEnvironmentOutputsPaginateTypeDef,
):
    pass


_RequiredListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentOutputsInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListEnvironmentOutputsInputRequestTypeDef(
    _RequiredListEnvironmentOutputsInputRequestTypeDef,
    _OptionalListEnvironmentOutputsInputRequestTypeDef,
):
    pass


ListEnvironmentOutputsOutputTypeDef = TypedDict(
    "ListEnvironmentOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List["OutputTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputListEnvironmentProvisionedResourcesPaginateTypeDef,
):
    pass


_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "environmentName": str,
    },
)
_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListEnvironmentProvisionedResourcesInputRequestTypeDef(
    _RequiredListEnvironmentProvisionedResourcesInputRequestTypeDef,
    _OptionalListEnvironmentProvisionedResourcesInputRequestTypeDef,
):
    pass


ListEnvironmentProvisionedResourcesOutputTypeDef = TypedDict(
    "ListEnvironmentProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List["ProvisionedResourceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputListEnvironmentTemplateVersionsPaginateTypeDef,
):
    pass


_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListEnvironmentTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListEnvironmentTemplateVersionsInputRequestTypeDef(
    _RequiredListEnvironmentTemplateVersionsInputRequestTypeDef,
    _OptionalListEnvironmentTemplateVersionsInputRequestTypeDef,
):
    pass


ListEnvironmentTemplateVersionsOutputTypeDef = TypedDict(
    "ListEnvironmentTemplateVersionsOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List["EnvironmentTemplateVersionSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputListEnvironmentTemplatesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEnvironmentTemplatesInputRequestTypeDef = TypedDict(
    "ListEnvironmentTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListEnvironmentTemplatesOutputTypeDef = TypedDict(
    "ListEnvironmentTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "templates": List["EnvironmentTemplateSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentsInputListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsInputListEnvironmentsPaginateTypeDef",
    {
        "environmentTemplates": Sequence["EnvironmentTemplateFilterTypeDef"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEnvironmentsInputRequestTypeDef = TypedDict(
    "ListEnvironmentsInputRequestTypeDef",
    {
        "environmentTemplates": Sequence["EnvironmentTemplateFilterTypeDef"],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListEnvironmentsOutputTypeDef = TypedDict(
    "ListEnvironmentsOutputTypeDef",
    {
        "environments": List["EnvironmentSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRepositoriesInputListRepositoriesPaginateTypeDef = TypedDict(
    "ListRepositoriesInputListRepositoriesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRepositoriesInputRequestTypeDef = TypedDict(
    "ListRepositoriesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListRepositoriesOutputTypeDef = TypedDict(
    "ListRepositoriesOutputTypeDef",
    {
        "nextToken": str,
        "repositories": List["RepositorySummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)
_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef(
    _RequiredListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
    _OptionalListRepositorySyncDefinitionsInputListRepositorySyncDefinitionsPaginateTypeDef,
):
    pass


_RequiredListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_RequiredListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "syncType": Literal["TEMPLATE_SYNC"],
    },
)
_OptionalListRepositorySyncDefinitionsInputRequestTypeDef = TypedDict(
    "_OptionalListRepositorySyncDefinitionsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListRepositorySyncDefinitionsInputRequestTypeDef(
    _RequiredListRepositorySyncDefinitionsInputRequestTypeDef,
    _OptionalListRepositorySyncDefinitionsInputRequestTypeDef,
):
    pass


ListRepositorySyncDefinitionsOutputTypeDef = TypedDict(
    "ListRepositorySyncDefinitionsOutputTypeDef",
    {
        "nextToken": str,
        "syncDefinitions": List["RepositorySyncDefinitionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef(
    _RequiredListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
    _OptionalListServiceInstanceOutputsInputListServiceInstanceOutputsPaginateTypeDef,
):
    pass


_RequiredListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceOutputsInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListServiceInstanceOutputsInputRequestTypeDef(
    _RequiredListServiceInstanceOutputsInputRequestTypeDef,
    _OptionalListServiceInstanceOutputsInputRequestTypeDef,
):
    pass


ListServiceInstanceOutputsOutputTypeDef = TypedDict(
    "ListServiceInstanceOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List["OutputTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputListServiceInstanceProvisionedResourcesPaginateTypeDef,
):
    pass


_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "serviceInstanceName": str,
        "serviceName": str,
    },
)
_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListServiceInstanceProvisionedResourcesInputRequestTypeDef(
    _RequiredListServiceInstanceProvisionedResourcesInputRequestTypeDef,
    _OptionalListServiceInstanceProvisionedResourcesInputRequestTypeDef,
):
    pass


ListServiceInstanceProvisionedResourcesOutputTypeDef = TypedDict(
    "ListServiceInstanceProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List["ProvisionedResourceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceInstancesInputListServiceInstancesPaginateTypeDef = TypedDict(
    "ListServiceInstancesInputListServiceInstancesPaginateTypeDef",
    {
        "serviceName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServiceInstancesInputRequestTypeDef = TypedDict(
    "ListServiceInstancesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "serviceName": str,
    },
    total=False,
)

ListServiceInstancesOutputTypeDef = TypedDict(
    "ListServiceInstancesOutputTypeDef",
    {
        "nextToken": str,
        "serviceInstances": List["ServiceInstanceSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef(
    _RequiredListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
    _OptionalListServicePipelineOutputsInputListServicePipelineOutputsPaginateTypeDef,
):
    pass


_RequiredListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineOutputsInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineOutputsInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineOutputsInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListServicePipelineOutputsInputRequestTypeDef(
    _RequiredListServicePipelineOutputsInputRequestTypeDef,
    _OptionalListServicePipelineOutputsInputRequestTypeDef,
):
    pass


ListServicePipelineOutputsOutputTypeDef = TypedDict(
    "ListServicePipelineOutputsOutputTypeDef",
    {
        "nextToken": str,
        "outputs": List["OutputTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputListServicePipelineProvisionedResourcesPaginateTypeDef,
):
    pass


_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "serviceName": str,
    },
)
_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef = TypedDict(
    "_OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListServicePipelineProvisionedResourcesInputRequestTypeDef(
    _RequiredListServicePipelineProvisionedResourcesInputRequestTypeDef,
    _OptionalListServicePipelineProvisionedResourcesInputRequestTypeDef,
):
    pass


ListServicePipelineProvisionedResourcesOutputTypeDef = TypedDict(
    "ListServicePipelineProvisionedResourcesOutputTypeDef",
    {
        "nextToken": str,
        "provisionedResources": List["ProvisionedResourceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef",
    {
        "majorVersion": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef(
    _RequiredListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
    _OptionalListServiceTemplateVersionsInputListServiceTemplateVersionsPaginateTypeDef,
):
    pass


_RequiredListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListServiceTemplateVersionsInputRequestTypeDef",
    {
        "templateName": str,
    },
)
_OptionalListServiceTemplateVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListServiceTemplateVersionsInputRequestTypeDef",
    {
        "majorVersion": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListServiceTemplateVersionsInputRequestTypeDef(
    _RequiredListServiceTemplateVersionsInputRequestTypeDef,
    _OptionalListServiceTemplateVersionsInputRequestTypeDef,
):
    pass


ListServiceTemplateVersionsOutputTypeDef = TypedDict(
    "ListServiceTemplateVersionsOutputTypeDef",
    {
        "nextToken": str,
        "templateVersions": List["ServiceTemplateVersionSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef = TypedDict(
    "ListServiceTemplatesInputListServiceTemplatesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServiceTemplatesInputRequestTypeDef = TypedDict(
    "ListServiceTemplatesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListServiceTemplatesOutputTypeDef = TypedDict(
    "ListServiceTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "templates": List["ServiceTemplateSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListServicesInputListServicesPaginateTypeDef = TypedDict(
    "ListServicesInputListServicesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListServicesInputRequestTypeDef = TypedDict(
    "ListServicesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListServicesOutputTypeDef = TypedDict(
    "ListServicesOutputTypeDef",
    {
        "nextToken": str,
        "services": List["ServiceSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "nextToken": str,
        "tags": List["TagTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "resourceArn": str,
        "status": ResourceDeploymentStatusType,
    },
)
_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef = TypedDict(
    "_OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef",
    {
        "deploymentId": str,
        "outputs": Sequence["OutputTypeDef"],
        "statusMessage": str,
    },
    total=False,
)


class NotifyResourceDeploymentStatusChangeInputRequestTypeDef(
    _RequiredNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
    _OptionalNotifyResourceDeploymentStatusChangeInputRequestTypeDef,
):
    pass


OutputTypeDef = TypedDict(
    "OutputTypeDef",
    {
        "key": str,
        "valueString": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ProvisionedResourceTypeDef = TypedDict(
    "ProvisionedResourceTypeDef",
    {
        "identifier": str,
        "name": str,
        "provisioningEngine": ProvisionedResourceEngineType,
    },
    total=False,
)

RejectEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
    },
)

RejectEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "RejectEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RepositoryBranchInputTypeDef = TypedDict(
    "RepositoryBranchInputTypeDef",
    {
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

RepositoryBranchTypeDef = TypedDict(
    "RepositoryBranchTypeDef",
    {
        "arn": str,
        "branch": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

RepositorySummaryTypeDef = TypedDict(
    "RepositorySummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)

RepositorySyncAttemptTypeDef = TypedDict(
    "RepositorySyncAttemptTypeDef",
    {
        "events": List["RepositorySyncEventTypeDef"],
        "startedAt": datetime,
        "status": RepositorySyncStatusType,
    },
)

RepositorySyncDefinitionTypeDef = TypedDict(
    "RepositorySyncDefinitionTypeDef",
    {
        "branch": str,
        "directory": str,
        "parent": str,
        "target": str,
    },
)

_RequiredRepositorySyncEventTypeDef = TypedDict(
    "_RequiredRepositorySyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
    },
)
_OptionalRepositorySyncEventTypeDef = TypedDict(
    "_OptionalRepositorySyncEventTypeDef",
    {
        "externalId": str,
    },
    total=False,
)


class RepositorySyncEventTypeDef(
    _RequiredRepositorySyncEventTypeDef, _OptionalRepositorySyncEventTypeDef
):
    pass


_RequiredRepositoryTypeDef = TypedDict(
    "_RequiredRepositoryTypeDef",
    {
        "arn": str,
        "connectionArn": str,
        "name": str,
        "provider": RepositoryProviderType,
    },
)
_OptionalRepositoryTypeDef = TypedDict(
    "_OptionalRepositoryTypeDef",
    {
        "encryptionKey": str,
    },
    total=False,
)


class RepositoryTypeDef(_RequiredRepositoryTypeDef, _OptionalRepositoryTypeDef):
    pass


ResourceSyncAttemptTypeDef = TypedDict(
    "ResourceSyncAttemptTypeDef",
    {
        "events": List["ResourceSyncEventTypeDef"],
        "initialRevision": "RevisionTypeDef",
        "startedAt": datetime,
        "status": ResourceSyncStatusType,
        "target": str,
        "targetRevision": "RevisionTypeDef",
    },
)

_RequiredResourceSyncEventTypeDef = TypedDict(
    "_RequiredResourceSyncEventTypeDef",
    {
        "event": str,
        "time": datetime,
        "type": str,
    },
)
_OptionalResourceSyncEventTypeDef = TypedDict(
    "_OptionalResourceSyncEventTypeDef",
    {
        "externalId": str,
    },
    total=False,
)


class ResourceSyncEventTypeDef(
    _RequiredResourceSyncEventTypeDef, _OptionalResourceSyncEventTypeDef
):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

RevisionTypeDef = TypedDict(
    "RevisionTypeDef",
    {
        "branch": str,
        "directory": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "sha": str,
    },
)

S3ObjectSourceTypeDef = TypedDict(
    "S3ObjectSourceTypeDef",
    {
        "bucket": str,
        "key": str,
    },
)

_RequiredServiceInstanceSummaryTypeDef = TypedDict(
    "_RequiredServiceInstanceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "serviceName": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServiceInstanceSummaryTypeDef = TypedDict(
    "_OptionalServiceInstanceSummaryTypeDef",
    {
        "deploymentStatusMessage": str,
    },
    total=False,
)


class ServiceInstanceSummaryTypeDef(
    _RequiredServiceInstanceSummaryTypeDef, _OptionalServiceInstanceSummaryTypeDef
):
    pass


_RequiredServiceInstanceTypeDef = TypedDict(
    "_RequiredServiceInstanceTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "environmentName": str,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "name": str,
        "serviceName": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServiceInstanceTypeDef = TypedDict(
    "_OptionalServiceInstanceTypeDef",
    {
        "deploymentStatusMessage": str,
        "spec": str,
    },
    total=False,
)


class ServiceInstanceTypeDef(_RequiredServiceInstanceTypeDef, _OptionalServiceInstanceTypeDef):
    pass


_RequiredServicePipelineTypeDef = TypedDict(
    "_RequiredServicePipelineTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "deploymentStatus": DeploymentStatusType,
        "lastDeploymentAttemptedAt": datetime,
        "lastDeploymentSucceededAt": datetime,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
        "templateName": str,
    },
)
_OptionalServicePipelineTypeDef = TypedDict(
    "_OptionalServicePipelineTypeDef",
    {
        "deploymentStatusMessage": str,
        "spec": str,
    },
    total=False,
)


class ServicePipelineTypeDef(_RequiredServicePipelineTypeDef, _OptionalServicePipelineTypeDef):
    pass


_RequiredServiceSummaryTypeDef = TypedDict(
    "_RequiredServiceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
        "templateName": str,
    },
)
_OptionalServiceSummaryTypeDef = TypedDict(
    "_OptionalServiceSummaryTypeDef",
    {
        "description": str,
        "statusMessage": str,
    },
    total=False,
)


class ServiceSummaryTypeDef(_RequiredServiceSummaryTypeDef, _OptionalServiceSummaryTypeDef):
    pass


_RequiredServiceTemplateSummaryTypeDef = TypedDict(
    "_RequiredServiceTemplateSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalServiceTemplateSummaryTypeDef = TypedDict(
    "_OptionalServiceTemplateSummaryTypeDef",
    {
        "description": str,
        "displayName": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)


class ServiceTemplateSummaryTypeDef(
    _RequiredServiceTemplateSummaryTypeDef, _OptionalServiceTemplateSummaryTypeDef
):
    pass


_RequiredServiceTemplateTypeDef = TypedDict(
    "_RequiredServiceTemplateTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
    },
)
_OptionalServiceTemplateTypeDef = TypedDict(
    "_OptionalServiceTemplateTypeDef",
    {
        "description": str,
        "displayName": str,
        "encryptionKey": str,
        "pipelineProvisioning": Literal["CUSTOMER_MANAGED"],
        "recommendedVersion": str,
    },
    total=False,
)


class ServiceTemplateTypeDef(_RequiredServiceTemplateTypeDef, _OptionalServiceTemplateTypeDef):
    pass


_RequiredServiceTemplateVersionSummaryTypeDef = TypedDict(
    "_RequiredServiceTemplateVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalServiceTemplateVersionSummaryTypeDef = TypedDict(
    "_OptionalServiceTemplateVersionSummaryTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "statusMessage": str,
    },
    total=False,
)


class ServiceTemplateVersionSummaryTypeDef(
    _RequiredServiceTemplateVersionSummaryTypeDef, _OptionalServiceTemplateVersionSummaryTypeDef
):
    pass


_RequiredServiceTemplateVersionTypeDef = TypedDict(
    "_RequiredServiceTemplateVersionTypeDef",
    {
        "arn": str,
        "compatibleEnvironmentTemplates": List["CompatibleEnvironmentTemplateTypeDef"],
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "majorVersion": str,
        "minorVersion": str,
        "status": TemplateVersionStatusType,
        "templateName": str,
    },
)
_OptionalServiceTemplateVersionTypeDef = TypedDict(
    "_OptionalServiceTemplateVersionTypeDef",
    {
        "description": str,
        "recommendedMinorVersion": str,
        "schema": str,
        "statusMessage": str,
    },
    total=False,
)


class ServiceTemplateVersionTypeDef(
    _RequiredServiceTemplateVersionTypeDef, _OptionalServiceTemplateVersionTypeDef
):
    pass


_RequiredServiceTypeDef = TypedDict(
    "_RequiredServiceTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "lastModifiedAt": datetime,
        "name": str,
        "spec": str,
        "status": ServiceStatusType,
        "templateName": str,
    },
)
_OptionalServiceTypeDef = TypedDict(
    "_OptionalServiceTypeDef",
    {
        "branchName": str,
        "description": str,
        "pipeline": "ServicePipelineTypeDef",
        "repositoryConnectionArn": str,
        "repositoryId": str,
        "statusMessage": str,
    },
    total=False,
)


class ServiceTypeDef(_RequiredServiceTypeDef, _OptionalServiceTypeDef):
    pass


TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence["TagTypeDef"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredTemplateSyncConfigTypeDef = TypedDict(
    "_RequiredTemplateSyncConfigTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalTemplateSyncConfigTypeDef = TypedDict(
    "_OptionalTemplateSyncConfigTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)


class TemplateSyncConfigTypeDef(
    _RequiredTemplateSyncConfigTypeDef, _OptionalTemplateSyncConfigTypeDef
):
    pass


TemplateVersionSourceInputTypeDef = TypedDict(
    "TemplateVersionSourceInputTypeDef",
    {
        "s3": "S3ObjectSourceTypeDef",
    },
    total=False,
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateAccountSettingsInputRequestTypeDef = TypedDict(
    "UpdateAccountSettingsInputRequestTypeDef",
    {
        "pipelineProvisioningRepository": "RepositoryBranchInputTypeDef",
        "pipelineServiceRoleArn": str,
    },
    total=False,
)

UpdateAccountSettingsOutputTypeDef = TypedDict(
    "UpdateAccountSettingsOutputTypeDef",
    {
        "accountSettings": "AccountSettingsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEnvironmentAccountConnectionInputRequestTypeDef = TypedDict(
    "UpdateEnvironmentAccountConnectionInputRequestTypeDef",
    {
        "id": str,
        "roleArn": str,
    },
)

UpdateEnvironmentAccountConnectionOutputTypeDef = TypedDict(
    "UpdateEnvironmentAccountConnectionOutputTypeDef",
    {
        "environmentAccountConnection": "EnvironmentAccountConnectionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
    },
)
_OptionalUpdateEnvironmentInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentInputRequestTypeDef",
    {
        "description": str,
        "environmentAccountConnectionId": str,
        "protonServiceRoleArn": str,
        "provisioningRepository": "RepositoryBranchInputTypeDef",
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)


class UpdateEnvironmentInputRequestTypeDef(
    _RequiredUpdateEnvironmentInputRequestTypeDef, _OptionalUpdateEnvironmentInputRequestTypeDef
):
    pass


UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "environment": "EnvironmentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateEnvironmentTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)


class UpdateEnvironmentTemplateInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateInputRequestTypeDef,
):
    pass


UpdateEnvironmentTemplateOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateOutputTypeDef",
    {
        "environmentTemplate": "EnvironmentTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef",
    {
        "description": str,
        "status": TemplateVersionStatusType,
    },
    total=False,
)


class UpdateEnvironmentTemplateVersionInputRequestTypeDef(
    _RequiredUpdateEnvironmentTemplateVersionInputRequestTypeDef,
    _OptionalUpdateEnvironmentTemplateVersionInputRequestTypeDef,
):
    pass


UpdateEnvironmentTemplateVersionOutputTypeDef = TypedDict(
    "UpdateEnvironmentTemplateVersionOutputTypeDef",
    {
        "environmentTemplateVersion": "EnvironmentTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateServiceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInputRequestTypeDef",
    {
        "description": str,
        "spec": str,
    },
    total=False,
)


class UpdateServiceInputRequestTypeDef(
    _RequiredUpdateServiceInputRequestTypeDef, _OptionalUpdateServiceInputRequestTypeDef
):
    pass


_RequiredUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceInstanceInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "name": str,
        "serviceName": str,
    },
)
_OptionalUpdateServiceInstanceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceInstanceInputRequestTypeDef",
    {
        "spec": str,
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)


class UpdateServiceInstanceInputRequestTypeDef(
    _RequiredUpdateServiceInstanceInputRequestTypeDef,
    _OptionalUpdateServiceInstanceInputRequestTypeDef,
):
    pass


UpdateServiceInstanceOutputTypeDef = TypedDict(
    "UpdateServiceInstanceOutputTypeDef",
    {
        "serviceInstance": "ServiceInstanceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServiceOutputTypeDef = TypedDict(
    "UpdateServiceOutputTypeDef",
    {
        "service": "ServiceTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServicePipelineInputRequestTypeDef",
    {
        "deploymentType": DeploymentUpdateTypeType,
        "serviceName": str,
        "spec": str,
    },
)
_OptionalUpdateServicePipelineInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServicePipelineInputRequestTypeDef",
    {
        "templateMajorVersion": str,
        "templateMinorVersion": str,
    },
    total=False,
)


class UpdateServicePipelineInputRequestTypeDef(
    _RequiredUpdateServicePipelineInputRequestTypeDef,
    _OptionalUpdateServicePipelineInputRequestTypeDef,
):
    pass


UpdateServicePipelineOutputTypeDef = TypedDict(
    "UpdateServicePipelineOutputTypeDef",
    {
        "pipeline": "ServicePipelineTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateInputRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalUpdateServiceTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateInputRequestTypeDef",
    {
        "description": str,
        "displayName": str,
    },
    total=False,
)


class UpdateServiceTemplateInputRequestTypeDef(
    _RequiredUpdateServiceTemplateInputRequestTypeDef,
    _OptionalUpdateServiceTemplateInputRequestTypeDef,
):
    pass


UpdateServiceTemplateOutputTypeDef = TypedDict(
    "UpdateServiceTemplateOutputTypeDef",
    {
        "serviceTemplate": "ServiceTemplateTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "majorVersion": str,
        "minorVersion": str,
        "templateName": str,
    },
)
_OptionalUpdateServiceTemplateVersionInputRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceTemplateVersionInputRequestTypeDef",
    {
        "compatibleEnvironmentTemplates": Sequence["CompatibleEnvironmentTemplateInputTypeDef"],
        "description": str,
        "status": TemplateVersionStatusType,
    },
    total=False,
)


class UpdateServiceTemplateVersionInputRequestTypeDef(
    _RequiredUpdateServiceTemplateVersionInputRequestTypeDef,
    _OptionalUpdateServiceTemplateVersionInputRequestTypeDef,
):
    pass


UpdateServiceTemplateVersionOutputTypeDef = TypedDict(
    "UpdateServiceTemplateVersionOutputTypeDef",
    {
        "serviceTemplateVersion": "ServiceTemplateVersionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "branch": str,
        "repositoryName": str,
        "repositoryProvider": RepositoryProviderType,
        "templateName": str,
        "templateType": TemplateTypeType,
    },
)
_OptionalUpdateTemplateSyncConfigInputRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateSyncConfigInputRequestTypeDef",
    {
        "subdirectory": str,
    },
    total=False,
)


class UpdateTemplateSyncConfigInputRequestTypeDef(
    _RequiredUpdateTemplateSyncConfigInputRequestTypeDef,
    _OptionalUpdateTemplateSyncConfigInputRequestTypeDef,
):
    pass


UpdateTemplateSyncConfigOutputTypeDef = TypedDict(
    "UpdateTemplateSyncConfigOutputTypeDef",
    {
        "templateSyncConfig": "TemplateSyncConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)
