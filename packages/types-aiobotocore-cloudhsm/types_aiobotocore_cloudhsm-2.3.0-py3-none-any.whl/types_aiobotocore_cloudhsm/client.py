"""
Type annotations for cloudhsm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudhsm.client import CloudHSMClient

    session = get_session()
    async with session.create_client("cloudhsm") as client:
        client: CloudHSMClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ClientVersionType
from .paginator import ListHapgsPaginator, ListHsmsPaginator, ListLunaClientsPaginator
from .type_defs import (
    AddTagsToResourceResponseTypeDef,
    CreateHapgResponseTypeDef,
    CreateHsmResponseTypeDef,
    CreateLunaClientResponseTypeDef,
    DeleteHapgResponseTypeDef,
    DeleteHsmResponseTypeDef,
    DeleteLunaClientResponseTypeDef,
    DescribeHapgResponseTypeDef,
    DescribeHsmResponseTypeDef,
    DescribeLunaClientResponseTypeDef,
    GetConfigResponseTypeDef,
    ListAvailableZonesResponseTypeDef,
    ListHapgsResponseTypeDef,
    ListHsmsResponseTypeDef,
    ListLunaClientsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyHapgResponseTypeDef,
    ModifyHsmResponseTypeDef,
    ModifyLunaClientResponseTypeDef,
    RemoveTagsFromResourceResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudHSMClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CloudHsmInternalException: Type[BotocoreClientError]
    CloudHsmServiceException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]


class CloudHSMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudHSMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#exceptions)
        """

    async def add_tags_to_resource(
        self, *, ResourceArn: str, TagList: Sequence["TagTypeDef"]
    ) -> AddTagsToResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.add_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#add_tags_to_resource)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#can_paginate)
        """

    async def create_hapg(self, *, Label: str) -> CreateHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_hapg)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_hapg)
        """

    async def create_hsm(
        self,
        *,
        SubnetId: str,
        SshKey: str,
        IamRoleArn: str,
        SubscriptionType: Literal["PRODUCTION"],
        EniIp: str = ...,
        ExternalId: str = ...,
        ClientToken: str = ...,
        SyslogIp: str = ...
    ) -> CreateHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_hsm)
        """

    async def create_luna_client(
        self, *, Certificate: str, Label: str = ...
    ) -> CreateLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.create_luna_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#create_luna_client)
        """

    async def delete_hapg(self, *, HapgArn: str) -> DeleteHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_hapg)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_hapg)
        """

    async def delete_hsm(self, *, HsmArn: str) -> DeleteHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_hsm)
        """

    async def delete_luna_client(self, *, ClientArn: str) -> DeleteLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.delete_luna_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#delete_luna_client)
        """

    async def describe_hapg(self, *, HapgArn: str) -> DescribeHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_hapg)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_hapg)
        """

    async def describe_hsm(
        self, *, HsmArn: str = ..., HsmSerialNumber: str = ...
    ) -> DescribeHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_hsm)
        """

    async def describe_luna_client(
        self, *, ClientArn: str = ..., CertificateFingerprint: str = ...
    ) -> DescribeLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.describe_luna_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#describe_luna_client)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#generate_presigned_url)
        """

    async def get_config(
        self, *, ClientArn: str, ClientVersion: ClientVersionType, HapgList: Sequence[str]
    ) -> GetConfigResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_config)
        """

    async def list_available_zones(self) -> ListAvailableZonesResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_available_zones)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_available_zones)
        """

    async def list_hapgs(self, *, NextToken: str = ...) -> ListHapgsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_hapgs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_hapgs)
        """

    async def list_hsms(self, *, NextToken: str = ...) -> ListHsmsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_hsms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_hsms)
        """

    async def list_luna_clients(self, *, NextToken: str = ...) -> ListLunaClientsResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_luna_clients)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_luna_clients)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#list_tags_for_resource)
        """

    async def modify_hapg(
        self, *, HapgArn: str, Label: str = ..., PartitionSerialList: Sequence[str] = ...
    ) -> ModifyHapgResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_hapg)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_hapg)
        """

    async def modify_hsm(
        self,
        *,
        HsmArn: str,
        SubnetId: str = ...,
        EniIp: str = ...,
        IamRoleArn: str = ...,
        ExternalId: str = ...,
        SyslogIp: str = ...
    ) -> ModifyHsmResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_hsm)
        """

    async def modify_luna_client(
        self, *, ClientArn: str, Certificate: str
    ) -> ModifyLunaClientResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.modify_luna_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#modify_luna_client)
        """

    async def remove_tags_from_resource(
        self, *, ResourceArn: str, TagKeyList: Sequence[str]
    ) -> RemoveTagsFromResourceResponseTypeDef:
        """
        This is documentation for **AWS CloudHSM Classic**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.remove_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#remove_tags_from_resource)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hapgs"]) -> ListHapgsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_hsms"]) -> ListHsmsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_luna_clients"]
    ) -> ListLunaClientsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudHSMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsm.html#CloudHSM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsm/client/)
        """
