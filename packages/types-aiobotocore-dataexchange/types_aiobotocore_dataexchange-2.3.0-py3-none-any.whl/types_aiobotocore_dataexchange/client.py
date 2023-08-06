"""
Type annotations for dataexchange service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dataexchange.client import DataExchangeClient

    session = get_session()
    async with session.create_client("dataexchange") as client:
        client: DataExchangeClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import AssetTypeType, TypeType
from .paginator import (
    ListDataSetRevisionsPaginator,
    ListDataSetsPaginator,
    ListEventActionsPaginator,
    ListJobsPaginator,
    ListRevisionAssetsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    CreateDataSetResponseTypeDef,
    CreateEventActionResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateRevisionResponseTypeDef,
    EventTypeDef,
    GetAssetResponseTypeDef,
    GetDataSetResponseTypeDef,
    GetEventActionResponseTypeDef,
    GetJobResponseTypeDef,
    GetRevisionResponseTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListEventActionsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListRevisionAssetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RequestDetailsTypeDef,
    RevokeRevisionResponseTypeDef,
    SendApiAssetResponseTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateEventActionResponseTypeDef,
    UpdateRevisionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DataExchangeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DataExchangeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataExchangeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#can_paginate)
        """

    async def cancel_job(self, *, JobId: str) -> None:
        """
        This operation cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#cancel_job)
        """

    async def create_data_set(
        self,
        *,
        AssetType: AssetTypeType,
        Description: str,
        Name: str,
        Tags: Mapping[str, str] = ...
    ) -> CreateDataSetResponseTypeDef:
        """
        This operation creates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_data_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_data_set)
        """

    async def create_event_action(
        self, *, Action: "ActionTypeDef", Event: "EventTypeDef"
    ) -> CreateEventActionResponseTypeDef:
        """
        This operation creates an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_event_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_event_action)
        """

    async def create_job(
        self, *, Details: "RequestDetailsTypeDef", Type: TypeType
    ) -> CreateJobResponseTypeDef:
        """
        This operation creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_job)
        """

    async def create_revision(
        self, *, DataSetId: str, Comment: str = ..., Tags: Mapping[str, str] = ...
    ) -> CreateRevisionResponseTypeDef:
        """
        This operation creates a revision for a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.create_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#create_revision)
        """

    async def delete_asset(self, *, AssetId: str, DataSetId: str, RevisionId: str) -> None:
        """
        This operation deletes an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_asset)
        """

    async def delete_data_set(self, *, DataSetId: str) -> None:
        """
        This operation deletes a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_data_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_data_set)
        """

    async def delete_event_action(self, *, EventActionId: str) -> None:
        """
        This operation deletes the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_event_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_event_action)
        """

    async def delete_revision(self, *, DataSetId: str, RevisionId: str) -> None:
        """
        This operation deletes a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.delete_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#delete_revision)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#generate_presigned_url)
        """

    async def get_asset(
        self, *, AssetId: str, DataSetId: str, RevisionId: str
    ) -> GetAssetResponseTypeDef:
        """
        This operation returns information about an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_asset)
        """

    async def get_data_set(self, *, DataSetId: str) -> GetDataSetResponseTypeDef:
        """
        This operation returns information about a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_data_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_data_set)
        """

    async def get_event_action(self, *, EventActionId: str) -> GetEventActionResponseTypeDef:
        """
        This operation retrieves information about an event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_event_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_event_action)
        """

    async def get_job(self, *, JobId: str) -> GetJobResponseTypeDef:
        """
        This operation returns information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_job)
        """

    async def get_revision(self, *, DataSetId: str, RevisionId: str) -> GetRevisionResponseTypeDef:
        """
        This operation returns information about a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_revision)
        """

    async def list_data_set_revisions(
        self, *, DataSetId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDataSetRevisionsResponseTypeDef:
        """
        This operation lists a data set's revisions sorted by CreatedAt in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_data_set_revisions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_data_set_revisions)
        """

    async def list_data_sets(
        self, *, MaxResults: int = ..., NextToken: str = ..., Origin: str = ...
    ) -> ListDataSetsResponseTypeDef:
        """
        This operation lists your data sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_data_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_data_sets)
        """

    async def list_event_actions(
        self, *, EventSourceId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListEventActionsResponseTypeDef:
        """
        This operation lists your event actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_event_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_event_actions)
        """

    async def list_jobs(
        self,
        *,
        DataSetId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        RevisionId: str = ...
    ) -> ListJobsResponseTypeDef:
        """
        This operation lists your jobs sorted by CreatedAt in descending order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_jobs)
        """

    async def list_revision_assets(
        self, *, DataSetId: str, RevisionId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRevisionAssetsResponseTypeDef:
        """
        This operation lists a revision's assets sorted alphabetically in descending
        order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_revision_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_revision_assets)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        This operation lists the tags on the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#list_tags_for_resource)
        """

    async def revoke_revision(
        self, *, DataSetId: str, RevisionId: str, RevocationComment: str
    ) -> RevokeRevisionResponseTypeDef:
        """
        This operation revokes subscribers' access to a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.revoke_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#revoke_revision)
        """

    async def send_api_asset(
        self,
        *,
        AssetId: str,
        DataSetId: str,
        RevisionId: str,
        Body: str = ...,
        QueryStringParameters: Mapping[str, str] = ...,
        RequestHeaders: Mapping[str, str] = ...,
        Method: str = ...,
        Path: str = ...
    ) -> SendApiAssetResponseTypeDef:
        """
        This operation invokes an API Gateway API asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.send_api_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#send_api_asset)
        """

    async def start_job(self, *, JobId: str) -> Dict[str, Any]:
        """
        This operation starts a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.start_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#start_job)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> None:
        """
        This operation tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> None:
        """
        This operation removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#untag_resource)
        """

    async def update_asset(
        self, *, AssetId: str, DataSetId: str, Name: str, RevisionId: str
    ) -> UpdateAssetResponseTypeDef:
        """
        This operation updates an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_asset)
        """

    async def update_data_set(
        self, *, DataSetId: str, Description: str = ..., Name: str = ...
    ) -> UpdateDataSetResponseTypeDef:
        """
        This operation updates a data set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_data_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_data_set)
        """

    async def update_event_action(
        self, *, EventActionId: str, Action: "ActionTypeDef" = ...
    ) -> UpdateEventActionResponseTypeDef:
        """
        This operation updates the event action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_event_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_event_action)
        """

    async def update_revision(
        self, *, DataSetId: str, RevisionId: str, Comment: str = ..., Finalized: bool = ...
    ) -> UpdateRevisionResponseTypeDef:
        """
        This operation updates a revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.update_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#update_revision)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_set_revisions"]
    ) -> ListDataSetRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_sets"]) -> ListDataSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_actions"]
    ) -> ListEventActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_revision_assets"]
    ) -> ListRevisionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/#get_paginator)
        """

    async def __aenter__(self) -> "DataExchangeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dataexchange.html#DataExchange.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dataexchange/client/)
        """
