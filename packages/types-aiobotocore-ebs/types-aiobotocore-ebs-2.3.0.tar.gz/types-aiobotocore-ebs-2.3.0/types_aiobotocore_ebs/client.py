"""
Type annotations for ebs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ebs.client import EBSClient

    session = get_session()
    async with session.create_client("ebs") as client:
        client: EBSClient
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .type_defs import (
    CompleteSnapshotResponseTypeDef,
    GetSnapshotBlockResponseTypeDef,
    ListChangedBlocksResponseTypeDef,
    ListSnapshotBlocksResponseTypeDef,
    PutSnapshotBlockResponseTypeDef,
    StartSnapshotResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("EBSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentLimitExceededException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    RequestThrottledException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EBSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EBSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#can_paginate)
        """

    async def complete_snapshot(
        self,
        *,
        SnapshotId: str,
        ChangedBlocksCount: int,
        Checksum: str = ...,
        ChecksumAlgorithm: Literal["SHA256"] = ...,
        ChecksumAggregationMethod: Literal["LINEAR"] = ...
    ) -> CompleteSnapshotResponseTypeDef:
        """
        Seals and completes the snapshot after all of the required blocks of data have
        been written to it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.complete_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#complete_snapshot)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#generate_presigned_url)
        """

    async def get_snapshot_block(
        self, *, SnapshotId: str, BlockIndex: int, BlockToken: str
    ) -> GetSnapshotBlockResponseTypeDef:
        """
        Returns the data in a block in an Amazon Elastic Block Store snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.get_snapshot_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#get_snapshot_block)
        """

    async def list_changed_blocks(
        self,
        *,
        SecondSnapshotId: str,
        FirstSnapshotId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        StartingBlockIndex: int = ...
    ) -> ListChangedBlocksResponseTypeDef:
        """
        Returns information about the blocks that are different between two Amazon
        Elastic Block Store snapshots of the same volume/snapshot lineage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.list_changed_blocks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#list_changed_blocks)
        """

    async def list_snapshot_blocks(
        self,
        *,
        SnapshotId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        StartingBlockIndex: int = ...
    ) -> ListSnapshotBlocksResponseTypeDef:
        """
        Returns information about the blocks in an Amazon Elastic Block Store snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.list_snapshot_blocks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#list_snapshot_blocks)
        """

    async def put_snapshot_block(
        self,
        *,
        SnapshotId: str,
        BlockIndex: int,
        BlockData: Union[str, bytes, IO[Any], StreamingBody],
        DataLength: int,
        Checksum: str,
        ChecksumAlgorithm: Literal["SHA256"],
        Progress: int = ...
    ) -> PutSnapshotBlockResponseTypeDef:
        """
        Writes a block of data to a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.put_snapshot_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#put_snapshot_block)
        """

    async def start_snapshot(
        self,
        *,
        VolumeSize: int,
        ParentSnapshotId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        Description: str = ...,
        ClientToken: str = ...,
        Encrypted: bool = ...,
        KmsKeyArn: str = ...,
        Timeout: int = ...
    ) -> StartSnapshotResponseTypeDef:
        """
        Creates a new Amazon EBS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client.start_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/#start_snapshot)
        """

    async def __aenter__(self) -> "EBSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ebs.html#EBS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ebs/client/)
        """
