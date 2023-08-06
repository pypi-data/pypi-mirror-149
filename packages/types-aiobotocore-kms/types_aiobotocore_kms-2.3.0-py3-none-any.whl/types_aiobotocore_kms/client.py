"""
Type annotations for kms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kms.client import KMSClient

    session = get_session()
    async with session.create_client("kms") as client:
        client: KMSClient
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import (
    AlgorithmSpecType,
    CustomerMasterKeySpecType,
    DataKeyPairSpecType,
    DataKeySpecType,
    EncryptionAlgorithmSpecType,
    ExpirationModelTypeType,
    GrantOperationType,
    KeySpecType,
    KeyUsageTypeType,
    MessageTypeType,
    OriginTypeType,
    SigningAlgorithmSpecType,
)
from .paginator import (
    ListAliasesPaginator,
    ListGrantsPaginator,
    ListKeyPoliciesPaginator,
    ListKeysPaginator,
)
from .type_defs import (
    CancelKeyDeletionResponseTypeDef,
    CreateCustomKeyStoreResponseTypeDef,
    CreateGrantResponseTypeDef,
    CreateKeyResponseTypeDef,
    DecryptResponseTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    DescribeKeyResponseTypeDef,
    EncryptResponseTypeDef,
    GenerateDataKeyPairResponseTypeDef,
    GenerateDataKeyPairWithoutPlaintextResponseTypeDef,
    GenerateDataKeyResponseTypeDef,
    GenerateDataKeyWithoutPlaintextResponseTypeDef,
    GenerateRandomResponseTypeDef,
    GetKeyPolicyResponseTypeDef,
    GetKeyRotationStatusResponseTypeDef,
    GetParametersForImportResponseTypeDef,
    GetPublicKeyResponseTypeDef,
    GrantConstraintsTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsResponseTypeDef,
    ReEncryptResponseTypeDef,
    ReplicateKeyResponseTypeDef,
    ScheduleKeyDeletionResponseTypeDef,
    SignResponseTypeDef,
    TagTypeDef,
    VerifyResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KMSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudHsmClusterInUseException: Type[BotocoreClientError]
    CloudHsmClusterInvalidConfigurationException: Type[BotocoreClientError]
    CloudHsmClusterNotActiveException: Type[BotocoreClientError]
    CloudHsmClusterNotFoundException: Type[BotocoreClientError]
    CloudHsmClusterNotRelatedException: Type[BotocoreClientError]
    CustomKeyStoreHasCMKsException: Type[BotocoreClientError]
    CustomKeyStoreInvalidStateException: Type[BotocoreClientError]
    CustomKeyStoreNameInUseException: Type[BotocoreClientError]
    CustomKeyStoreNotFoundException: Type[BotocoreClientError]
    DependencyTimeoutException: Type[BotocoreClientError]
    DisabledException: Type[BotocoreClientError]
    ExpiredImportTokenException: Type[BotocoreClientError]
    IncorrectKeyException: Type[BotocoreClientError]
    IncorrectKeyMaterialException: Type[BotocoreClientError]
    IncorrectTrustAnchorException: Type[BotocoreClientError]
    InvalidAliasNameException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidCiphertextException: Type[BotocoreClientError]
    InvalidGrantIdException: Type[BotocoreClientError]
    InvalidGrantTokenException: Type[BotocoreClientError]
    InvalidImportTokenException: Type[BotocoreClientError]
    InvalidKeyUsageException: Type[BotocoreClientError]
    InvalidMarkerException: Type[BotocoreClientError]
    KMSInternalException: Type[BotocoreClientError]
    KMSInvalidSignatureException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KeyUnavailableException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TagException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class KMSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#can_paginate)
        """

    async def cancel_key_deletion(self, *, KeyId: str) -> CancelKeyDeletionResponseTypeDef:
        """
        Cancels the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.cancel_key_deletion)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#cancel_key_deletion)
        """

    async def connect_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Connects or reconnects a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-
        overview.html)_ to its associated CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.connect_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#connect_custom_key_store)
        """

    async def create_alias(self, *, AliasName: str, TargetKeyId: str) -> None:
        """
        Creates a friendly name for a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_alias)
        """

    async def create_custom_key_store(
        self,
        *,
        CustomKeyStoreName: str,
        CloudHsmClusterId: str,
        TrustAnchorCertificate: str,
        KeyStorePassword: str
    ) -> CreateCustomKeyStoreResponseTypeDef:
        """
        Creates a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-
        overview.html)_ that is associated with an [CloudHSM
        cluster](https://docs.aws.amazon.com/cloudhsm/latest/userguide/clusters.html)_
        that you own and manage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_custom_key_store)
        """

    async def create_grant(
        self,
        *,
        KeyId: str,
        GranteePrincipal: str,
        Operations: Sequence[GrantOperationType],
        RetiringPrincipal: str = ...,
        Constraints: "GrantConstraintsTypeDef" = ...,
        GrantTokens: Sequence[str] = ...,
        Name: str = ...
    ) -> CreateGrantResponseTypeDef:
        """
        Adds a grant to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_grant)
        """

    async def create_key(
        self,
        *,
        Policy: str = ...,
        Description: str = ...,
        KeyUsage: KeyUsageTypeType = ...,
        CustomerMasterKeySpec: CustomerMasterKeySpecType = ...,
        KeySpec: KeySpecType = ...,
        Origin: OriginTypeType = ...,
        CustomKeyStoreId: str = ...,
        BypassPolicyLockoutSafetyCheck: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        MultiRegion: bool = ...
    ) -> CreateKeyResponseTypeDef:
        """
        Creates a unique customer managed [KMS
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms-
        keys)_ in your Amazon Web Services account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_key)
        """

    async def decrypt(
        self,
        *,
        CiphertextBlob: Union[str, bytes, IO[Any], StreamingBody],
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        KeyId: str = ...,
        EncryptionAlgorithm: EncryptionAlgorithmSpecType = ...
    ) -> DecryptResponseTypeDef:
        """
        Decrypts ciphertext that was encrypted by a KMS key using any of the following
        operations *  Encrypt *  GenerateDataKey *  GenerateDataKeyPair *
        GenerateDataKeyWithoutPlaintext *  GenerateDataKeyPairWithoutPlaintext You can
        use this operation to decrypt cipher...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.decrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#decrypt)
        """

    async def delete_alias(self, *, AliasName: str) -> None:
        """
        Deletes the specified alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_alias)
        """

    async def delete_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Deletes a [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-
        overview.html)_.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_custom_key_store)
        """

    async def delete_imported_key_material(self, *, KeyId: str) -> None:
        """
        Deletes key material that you previously imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_imported_key_material)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_imported_key_material)
        """

    async def describe_custom_key_stores(
        self,
        *,
        CustomKeyStoreId: str = ...,
        CustomKeyStoreName: str = ...,
        Limit: int = ...,
        Marker: str = ...
    ) -> DescribeCustomKeyStoresResponseTypeDef:
        """
        Gets information about [custom key
        stores](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-
        overview.html)_ in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.describe_custom_key_stores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_custom_key_stores)
        """

    async def describe_key(
        self, *, KeyId: str, GrantTokens: Sequence[str] = ...
    ) -> DescribeKeyResponseTypeDef:
        """
        Provides detailed information about a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.describe_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_key)
        """

    async def disable_key(self, *, KeyId: str) -> None:
        """
        Sets the state of a KMS key to disabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disable_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key)
        """

    async def disable_key_rotation(self, *, KeyId: str) -> None:
        """
        Disables [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-
        keys.html)_ for the specified symmetric KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disable_key_rotation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key_rotation)
        """

    async def disconnect_custom_key_store(self, *, CustomKeyStoreId: str) -> Dict[str, Any]:
        """
        Disconnects the [custom key
        store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-
        overview.html)_ from its associated CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.disconnect_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disconnect_custom_key_store)
        """

    async def enable_key(self, *, KeyId: str) -> None:
        """
        Sets the key state of a KMS key to enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.enable_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key)
        """

    async def enable_key_rotation(self, *, KeyId: str) -> None:
        """
        Enables [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-
        keys.html)_ for the specified symmetric KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.enable_key_rotation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key_rotation)
        """

    async def encrypt(
        self,
        *,
        KeyId: str,
        Plaintext: Union[str, bytes, IO[Any], StreamingBody],
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...,
        EncryptionAlgorithm: EncryptionAlgorithmSpecType = ...
    ) -> EncryptResponseTypeDef:
        """
        Encrypts plaintext into ciphertext by using a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.encrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#encrypt)
        """

    async def generate_data_key(
        self,
        *,
        KeyId: str,
        EncryptionContext: Mapping[str, str] = ...,
        NumberOfBytes: int = ...,
        KeySpec: DataKeySpecType = ...,
        GrantTokens: Sequence[str] = ...
    ) -> GenerateDataKeyResponseTypeDef:
        """
        Generates a unique symmetric data key for client-side encryption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key)
        """

    async def generate_data_key_pair(
        self,
        *,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpecType,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...
    ) -> GenerateDataKeyPairResponseTypeDef:
        """
        Generates a unique asymmetric data key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair)
        """

    async def generate_data_key_pair_without_plaintext(
        self,
        *,
        KeyId: str,
        KeyPairSpec: DataKeyPairSpecType,
        EncryptionContext: Mapping[str, str] = ...,
        GrantTokens: Sequence[str] = ...
    ) -> GenerateDataKeyPairWithoutPlaintextResponseTypeDef:
        """
        Generates a unique asymmetric data key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_pair_without_plaintext)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair_without_plaintext)
        """

    async def generate_data_key_without_plaintext(
        self,
        *,
        KeyId: str,
        EncryptionContext: Mapping[str, str] = ...,
        KeySpec: DataKeySpecType = ...,
        NumberOfBytes: int = ...,
        GrantTokens: Sequence[str] = ...
    ) -> GenerateDataKeyWithoutPlaintextResponseTypeDef:
        """
        Generates a unique symmetric data key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_data_key_without_plaintext)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_without_plaintext)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_presigned_url)
        """

    async def generate_random(
        self, *, NumberOfBytes: int = ..., CustomKeyStoreId: str = ...
    ) -> GenerateRandomResponseTypeDef:
        """
        Returns a random byte string that is cryptographically secure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.generate_random)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_random)
        """

    async def get_key_policy(self, *, KeyId: str, PolicyName: str) -> GetKeyPolicyResponseTypeDef:
        """
        Gets a key policy attached to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_key_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_policy)
        """

    async def get_key_rotation_status(self, *, KeyId: str) -> GetKeyRotationStatusResponseTypeDef:
        """
        Gets a Boolean value that indicates whether [automatic rotation of the key
        material](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-
        keys.html)_ is enabled for the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_key_rotation_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_rotation_status)
        """

    async def get_parameters_for_import(
        self,
        *,
        KeyId: str,
        WrappingAlgorithm: AlgorithmSpecType,
        WrappingKeySpec: Literal["RSA_2048"]
    ) -> GetParametersForImportResponseTypeDef:
        """
        Returns the items you need to import key material into a symmetric, customer
        managed KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_parameters_for_import)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_parameters_for_import)
        """

    async def get_public_key(
        self, *, KeyId: str, GrantTokens: Sequence[str] = ...
    ) -> GetPublicKeyResponseTypeDef:
        """
        Returns the public key of an asymmetric KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_public_key)
        """

    async def import_key_material(
        self,
        *,
        KeyId: str,
        ImportToken: Union[str, bytes, IO[Any], StreamingBody],
        EncryptedKeyMaterial: Union[str, bytes, IO[Any], StreamingBody],
        ValidTo: Union[datetime, str] = ...,
        ExpirationModel: ExpirationModelTypeType = ...
    ) -> Dict[str, Any]:
        """
        Imports key material into an existing symmetric KMS KMS key that was created
        without key material.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.import_key_material)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#import_key_material)
        """

    async def list_aliases(
        self, *, KeyId: str = ..., Limit: int = ..., Marker: str = ...
    ) -> ListAliasesResponseTypeDef:
        """
        Gets a list of aliases in the caller's Amazon Web Services account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_aliases)
        """

    async def list_grants(
        self,
        *,
        KeyId: str,
        Limit: int = ...,
        Marker: str = ...,
        GrantId: str = ...,
        GranteePrincipal: str = ...
    ) -> ListGrantsResponseTypeDef:
        """
        Gets a list of all grants for the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_grants)
        """

    async def list_key_policies(
        self, *, KeyId: str, Limit: int = ..., Marker: str = ...
    ) -> ListKeyPoliciesResponseTypeDef:
        """
        Gets the names of the key policies that are attached to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_key_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_key_policies)
        """

    async def list_keys(self, *, Limit: int = ..., Marker: str = ...) -> ListKeysResponseTypeDef:
        """
        Gets a list of all KMS keys in the caller's Amazon Web Services account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_keys)
        """

    async def list_resource_tags(
        self, *, KeyId: str, Limit: int = ..., Marker: str = ...
    ) -> ListResourceTagsResponseTypeDef:
        """
        Returns all tags on the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_resource_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_resource_tags)
        """

    async def list_retirable_grants(
        self, *, RetiringPrincipal: str, Limit: int = ..., Marker: str = ...
    ) -> ListGrantsResponseTypeDef:
        """
        Returns information about all grants in the Amazon Web Services account and
        Region that have the specified retiring principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.list_retirable_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_retirable_grants)
        """

    async def put_key_policy(
        self,
        *,
        KeyId: str,
        PolicyName: str,
        Policy: str,
        BypassPolicyLockoutSafetyCheck: bool = ...
    ) -> None:
        """
        Attaches a key policy to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.put_key_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#put_key_policy)
        """

    async def re_encrypt(
        self,
        *,
        CiphertextBlob: Union[str, bytes, IO[Any], StreamingBody],
        DestinationKeyId: str,
        SourceEncryptionContext: Mapping[str, str] = ...,
        SourceKeyId: str = ...,
        DestinationEncryptionContext: Mapping[str, str] = ...,
        SourceEncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        DestinationEncryptionAlgorithm: EncryptionAlgorithmSpecType = ...,
        GrantTokens: Sequence[str] = ...
    ) -> ReEncryptResponseTypeDef:
        """
        Decrypts ciphertext and then reencrypts it entirely within KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.re_encrypt)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#re_encrypt)
        """

    async def replicate_key(
        self,
        *,
        KeyId: str,
        ReplicaRegion: str,
        Policy: str = ...,
        BypassPolicyLockoutSafetyCheck: bool = ...,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ReplicateKeyResponseTypeDef:
        """
        Replicates a multi-Region key into the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.replicate_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#replicate_key)
        """

    async def retire_grant(
        self, *, GrantToken: str = ..., KeyId: str = ..., GrantId: str = ...
    ) -> None:
        """
        Deletes a grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.retire_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#retire_grant)
        """

    async def revoke_grant(self, *, KeyId: str, GrantId: str) -> None:
        """
        Deletes the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.revoke_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#revoke_grant)
        """

    async def schedule_key_deletion(
        self, *, KeyId: str, PendingWindowInDays: int = ...
    ) -> ScheduleKeyDeletionResponseTypeDef:
        """
        Schedules the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.schedule_key_deletion)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#schedule_key_deletion)
        """

    async def sign(
        self,
        *,
        KeyId: str,
        Message: Union[str, bytes, IO[Any], StreamingBody],
        SigningAlgorithm: SigningAlgorithmSpecType,
        MessageType: MessageTypeType = ...,
        GrantTokens: Sequence[str] = ...
    ) -> SignResponseTypeDef:
        """
        Creates a [digital signature](https://en.wikipedia.org/wiki/Digital_signature)_
        for a message or message digest by using the private key in an asymmetric KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.sign)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#sign)
        """

    async def tag_resource(self, *, KeyId: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds or edits tags on a [customer managed
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-
        cmk)_ .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#tag_resource)
        """

    async def untag_resource(self, *, KeyId: str, TagKeys: Sequence[str]) -> None:
        """
        Deletes tags from a [customer managed
        key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-
        cmk)_.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#untag_resource)
        """

    async def update_alias(self, *, AliasName: str, TargetKeyId: str) -> None:
        """
        Associates an existing KMS alias with a different KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_alias)
        """

    async def update_custom_key_store(
        self,
        *,
        CustomKeyStoreId: str,
        NewCustomKeyStoreName: str = ...,
        KeyStorePassword: str = ...,
        CloudHsmClusterId: str = ...
    ) -> Dict[str, Any]:
        """
        Changes the properties of a custom key store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_custom_key_store)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_custom_key_store)
        """

    async def update_key_description(self, *, KeyId: str, Description: str) -> None:
        """
        Updates the description of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_key_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_key_description)
        """

    async def update_primary_region(self, *, KeyId: str, PrimaryRegion: str) -> None:
        """
        Changes the primary key of a multi-Region key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.update_primary_region)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_primary_region)
        """

    async def verify(
        self,
        *,
        KeyId: str,
        Message: Union[str, bytes, IO[Any], StreamingBody],
        Signature: Union[str, bytes, IO[Any], StreamingBody],
        SigningAlgorithm: SigningAlgorithmSpecType,
        MessageType: MessageTypeType = ...,
        GrantTokens: Sequence[str] = ...
    ) -> VerifyResponseTypeDef:
        """
        Verifies a digital signature that was generated by the  Sign operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.verify)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#verify)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_grants"]) -> ListGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_key_policies"]
    ) -> ListKeyPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    async def __aenter__(self) -> "KMSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """
