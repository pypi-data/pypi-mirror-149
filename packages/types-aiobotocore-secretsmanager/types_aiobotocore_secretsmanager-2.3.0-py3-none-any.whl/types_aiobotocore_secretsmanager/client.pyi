"""
Type annotations for secretsmanager service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_secretsmanager.client import SecretsManagerClient

    session = get_session()
    async with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import SortOrderTypeType
from .paginator import ListSecretsPaginator
from .type_defs import (
    CancelRotateSecretResponseTypeDef,
    CreateSecretResponseTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteSecretResponseTypeDef,
    DescribeSecretResponseTypeDef,
    FilterTypeDef,
    GetRandomPasswordResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSecretValueResponseTypeDef,
    ListSecretsResponseTypeDef,
    ListSecretVersionIdsResponseTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSecretValueResponseTypeDef,
    RemoveRegionsFromReplicationResponseTypeDef,
    ReplicaRegionTypeTypeDef,
    ReplicateSecretToRegionsResponseTypeDef,
    RestoreSecretResponseTypeDef,
    RotateSecretResponseTypeDef,
    RotationRulesTypeTypeDef,
    StopReplicationToReplicaResponseTypeDef,
    TagTypeDef,
    UpdateSecretResponseTypeDef,
    UpdateSecretVersionStageResponseTypeDef,
    ValidateResourcePolicyResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SecretsManagerClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DecryptionFailure: Type[BotocoreClientError]
    EncryptionFailure: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    PublicPolicyException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class SecretsManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecretsManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#can_paginate)
        """
    async def cancel_rotate_secret(self, *, SecretId: str) -> CancelRotateSecretResponseTypeDef:
        """
        Turns off automatic rotation, and if a rotation is currently in progress,
        cancels the rotation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.cancel_rotate_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#cancel_rotate_secret)
        """
    async def create_secret(
        self,
        *,
        Name: str,
        ClientRequestToken: str = ...,
        Description: str = ...,
        KmsKeyId: str = ...,
        SecretBinary: Union[str, bytes, IO[Any], StreamingBody] = ...,
        SecretString: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        AddReplicaRegions: Sequence["ReplicaRegionTypeTypeDef"] = ...,
        ForceOverwriteReplicaSecret: bool = ...
    ) -> CreateSecretResponseTypeDef:
        """
        Creates a new secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.create_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#create_secret)
        """
    async def delete_resource_policy(self, *, SecretId: str) -> DeleteResourcePolicyResponseTypeDef:
        """
        Deletes the resource-based permission policy attached to the secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#delete_resource_policy)
        """
    async def delete_secret(
        self,
        *,
        SecretId: str,
        RecoveryWindowInDays: int = ...,
        ForceDeleteWithoutRecovery: bool = ...
    ) -> DeleteSecretResponseTypeDef:
        """
        Deletes a secret and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.delete_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#delete_secret)
        """
    async def describe_secret(self, *, SecretId: str) -> DescribeSecretResponseTypeDef:
        """
        Retrieves the details of a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.describe_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#describe_secret)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#generate_presigned_url)
        """
    async def get_random_password(
        self,
        *,
        PasswordLength: int = ...,
        ExcludeCharacters: str = ...,
        ExcludeNumbers: bool = ...,
        ExcludePunctuation: bool = ...,
        ExcludeUppercase: bool = ...,
        ExcludeLowercase: bool = ...,
        IncludeSpace: bool = ...,
        RequireEachIncludedType: bool = ...
    ) -> GetRandomPasswordResponseTypeDef:
        """
        Generates a random password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_random_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_random_password)
        """
    async def get_resource_policy(self, *, SecretId: str) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the JSON text of the resource-based policy document attached to the
        secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_resource_policy)
        """
    async def get_secret_value(
        self, *, SecretId: str, VersionId: str = ..., VersionStage: str = ...
    ) -> GetSecretValueResponseTypeDef:
        """
        Retrieves the contents of the encrypted fields `SecretString` or `SecretBinary`
        from the specified version of a secret, whichever contains content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_secret_value)
        """
    async def list_secret_version_ids(
        self,
        *,
        SecretId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        IncludeDeprecated: bool = ...
    ) -> ListSecretVersionIdsResponseTypeDef:
        """
        Lists the versions for a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.list_secret_version_ids)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#list_secret_version_ids)
        """
    async def list_secrets(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortOrder: SortOrderTypeType = ...
    ) -> ListSecretsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.list_secrets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#list_secrets)
        """
    async def put_resource_policy(
        self, *, SecretId: str, ResourcePolicy: str, BlockPublicPolicy: bool = ...
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a resource-based permission policy to a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#put_resource_policy)
        """
    async def put_secret_value(
        self,
        *,
        SecretId: str,
        ClientRequestToken: str = ...,
        SecretBinary: Union[str, bytes, IO[Any], StreamingBody] = ...,
        SecretString: str = ...,
        VersionStages: Sequence[str] = ...
    ) -> PutSecretValueResponseTypeDef:
        """
        Creates a new version with a new encrypted secret value and attaches it to the
        secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.put_secret_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#put_secret_value)
        """
    async def remove_regions_from_replication(
        self, *, SecretId: str, RemoveReplicaRegions: Sequence[str]
    ) -> RemoveRegionsFromReplicationResponseTypeDef:
        """
        For a secret that is replicated to other Regions, deletes the secret replicas
        from the Regions you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.remove_regions_from_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#remove_regions_from_replication)
        """
    async def replicate_secret_to_regions(
        self,
        *,
        SecretId: str,
        AddReplicaRegions: Sequence["ReplicaRegionTypeTypeDef"],
        ForceOverwriteReplicaSecret: bool = ...
    ) -> ReplicateSecretToRegionsResponseTypeDef:
        """
        Replicates the secret to a new Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.replicate_secret_to_regions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#replicate_secret_to_regions)
        """
    async def restore_secret(self, *, SecretId: str) -> RestoreSecretResponseTypeDef:
        """
        Cancels the scheduled deletion of a secret by removing the `DeletedDate` time
        stamp.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.restore_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#restore_secret)
        """
    async def rotate_secret(
        self,
        *,
        SecretId: str,
        ClientRequestToken: str = ...,
        RotationLambdaARN: str = ...,
        RotationRules: "RotationRulesTypeTypeDef" = ...,
        RotateImmediately: bool = ...
    ) -> RotateSecretResponseTypeDef:
        """
        Configures and starts the asynchronous process of rotating the secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.rotate_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#rotate_secret)
        """
    async def stop_replication_to_replica(
        self, *, SecretId: str
    ) -> StopReplicationToReplicaResponseTypeDef:
        """
        Removes the link between the replica secret and the primary secret and promotes
        the replica to a primary secret in the replica Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.stop_replication_to_replica)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#stop_replication_to_replica)
        """
    async def tag_resource(self, *, SecretId: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Attaches tags to a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#tag_resource)
        """
    async def untag_resource(self, *, SecretId: str, TagKeys: Sequence[str]) -> None:
        """
        Removes specific tags from a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#untag_resource)
        """
    async def update_secret(
        self,
        *,
        SecretId: str,
        ClientRequestToken: str = ...,
        Description: str = ...,
        KmsKeyId: str = ...,
        SecretBinary: Union[str, bytes, IO[Any], StreamingBody] = ...,
        SecretString: str = ...
    ) -> UpdateSecretResponseTypeDef:
        """
        Modifies the details of a secret, including metadata and the secret value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.update_secret)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#update_secret)
        """
    async def update_secret_version_stage(
        self,
        *,
        SecretId: str,
        VersionStage: str,
        RemoveFromVersionId: str = ...,
        MoveToVersionId: str = ...
    ) -> UpdateSecretVersionStageResponseTypeDef:
        """
        Modifies the staging labels attached to a version of a secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.update_secret_version_stage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#update_secret_version_stage)
        """
    async def validate_resource_policy(
        self, *, ResourcePolicy: str, SecretId: str = ...
    ) -> ValidateResourcePolicyResponseTypeDef:
        """
        Validates that a resource policy does not grant a wide range of principals
        access to your secret.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.validate_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#validate_resource_policy)
        """
    def get_paginator(self, operation_name: Literal["list_secrets"]) -> ListSecretsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/#get_paginator)
        """
    async def __aenter__(self) -> "SecretsManagerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/client/)
        """
