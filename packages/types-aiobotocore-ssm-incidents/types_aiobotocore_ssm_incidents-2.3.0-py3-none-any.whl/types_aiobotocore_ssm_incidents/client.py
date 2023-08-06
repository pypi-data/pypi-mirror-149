"""
Type annotations for ssm-incidents service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient

    session = get_session()
    async with session.create_client("ssm-incidents") as client:
        client: SSMIncidentsClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import IncidentRecordStatusType, SortOrderType
from .paginator import (
    GetResourcePoliciesPaginator,
    ListIncidentRecordsPaginator,
    ListRelatedItemsPaginator,
    ListReplicationSetsPaginator,
    ListResponsePlansPaginator,
    ListTimelineEventsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    ChatChannelTypeDef,
    CreateReplicationSetOutputTypeDef,
    CreateResponsePlanOutputTypeDef,
    CreateTimelineEventOutputTypeDef,
    FilterTypeDef,
    GetIncidentRecordOutputTypeDef,
    GetReplicationSetOutputTypeDef,
    GetResourcePoliciesOutputTypeDef,
    GetResponsePlanOutputTypeDef,
    GetTimelineEventOutputTypeDef,
    IncidentTemplateTypeDef,
    ListIncidentRecordsOutputTypeDef,
    ListRelatedItemsOutputTypeDef,
    ListReplicationSetsOutputTypeDef,
    ListResponsePlansOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimelineEventsOutputTypeDef,
    NotificationTargetItemTypeDef,
    PutResourcePolicyOutputTypeDef,
    RegionMapInputValueTypeDef,
    RelatedItemsUpdateTypeDef,
    RelatedItemTypeDef,
    StartIncidentOutputTypeDef,
    TriggerDetailsTypeDef,
    UpdateReplicationSetActionTypeDef,
)
from .waiter import WaitForReplicationSetActiveWaiter, WaitForReplicationSetDeletedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SSMIncidentsClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SSMIncidentsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMIncidentsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#can_paginate)
        """

    async def create_replication_set(
        self, *, regions: Mapping[str, "RegionMapInputValueTypeDef"], clientToken: str = ...
    ) -> CreateReplicationSetOutputTypeDef:
        """
        A replication set replicates and encrypts your data to the provided Regions with
        the provided KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.create_replication_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_replication_set)
        """

    async def create_response_plan(
        self,
        *,
        incidentTemplate: "IncidentTemplateTypeDef",
        name: str,
        actions: Sequence["ActionTypeDef"] = ...,
        chatChannel: "ChatChannelTypeDef" = ...,
        clientToken: str = ...,
        displayName: str = ...,
        engagements: Sequence[str] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateResponsePlanOutputTypeDef:
        """
        Creates a response plan that automates the initial response to incidents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.create_response_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_response_plan)
        """

    async def create_timeline_event(
        self,
        *,
        eventData: str,
        eventTime: Union[datetime, str],
        eventType: str,
        incidentRecordArn: str,
        clientToken: str = ...
    ) -> CreateTimelineEventOutputTypeDef:
        """
        Creates a custom timeline event on the incident details page of an incident
        record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.create_timeline_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_timeline_event)
        """

    async def delete_incident_record(self, *, arn: str) -> Dict[str, Any]:
        """
        Delete an incident record from Incident Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.delete_incident_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_incident_record)
        """

    async def delete_replication_set(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes all Regions in your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.delete_replication_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_replication_set)
        """

    async def delete_resource_policy(self, *, policyId: str, resourceArn: str) -> Dict[str, Any]:
        """
        Deletes the resource policy that Resource Access Manager uses to share your
        Incident Manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_resource_policy)
        """

    async def delete_response_plan(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.delete_response_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_response_plan)
        """

    async def delete_timeline_event(
        self, *, eventId: str, incidentRecordArn: str
    ) -> Dict[str, Any]:
        """
        Deletes a timeline event from an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.delete_timeline_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_timeline_event)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#generate_presigned_url)
        """

    async def get_incident_record(self, *, arn: str) -> GetIncidentRecordOutputTypeDef:
        """
        Returns the details for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_incident_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_incident_record)
        """

    async def get_replication_set(self, *, arn: str) -> GetReplicationSetOutputTypeDef:
        """
        Retrieve your Incident Manager replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_replication_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_replication_set)
        """

    async def get_resource_policies(
        self, *, resourceArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetResourcePoliciesOutputTypeDef:
        """
        Retrieves the resource policies attached to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_resource_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_resource_policies)
        """

    async def get_response_plan(self, *, arn: str) -> GetResponsePlanOutputTypeDef:
        """
        Retrieves the details of the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_response_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_response_plan)
        """

    async def get_timeline_event(
        self, *, eventId: str, incidentRecordArn: str
    ) -> GetTimelineEventOutputTypeDef:
        """
        Retrieves a timeline event based on its ID and incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_timeline_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_timeline_event)
        """

    async def list_incident_records(
        self,
        *,
        filters: Sequence["FilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListIncidentRecordsOutputTypeDef:
        """
        Lists all incident records in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_incident_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_incident_records)
        """

    async def list_related_items(
        self, *, incidentRecordArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListRelatedItemsOutputTypeDef:
        """
        List all related items for an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_related_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_related_items)
        """

    async def list_replication_sets(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListReplicationSetsOutputTypeDef:
        """
        Lists details about the replication set configured in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_replication_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_replication_sets)
        """

    async def list_response_plans(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListResponsePlansOutputTypeDef:
        """
        Lists all response plans in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_response_plans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_response_plans)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_tags_for_resource)
        """

    async def list_timeline_events(
        self,
        *,
        incidentRecordArn: str,
        filters: Sequence["FilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sortBy: Literal["EVENT_TIME"] = ...,
        sortOrder: SortOrderType = ...
    ) -> ListTimelineEventsOutputTypeDef:
        """
        Lists timeline events for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.list_timeline_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_timeline_events)
        """

    async def put_resource_policy(
        self, *, policy: str, resourceArn: str
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Adds a resource policy to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#put_resource_policy)
        """

    async def start_incident(
        self,
        *,
        responsePlanArn: str,
        clientToken: str = ...,
        impact: int = ...,
        relatedItems: Sequence["RelatedItemTypeDef"] = ...,
        title: str = ...,
        triggerDetails: "TriggerDetailsTypeDef" = ...
    ) -> StartIncidentOutputTypeDef:
        """
        Used to start an incident from CloudWatch alarms, EventBridge events, or
        manually.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.start_incident)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#start_incident)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds a tag to a response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#untag_resource)
        """

    async def update_deletion_protection(
        self, *, arn: str, deletionProtected: bool, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Update deletion protection to either allow or deny deletion of the final Region
        in a replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_deletion_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_deletion_protection)
        """

    async def update_incident_record(
        self,
        *,
        arn: str,
        chatChannel: "ChatChannelTypeDef" = ...,
        clientToken: str = ...,
        impact: int = ...,
        notificationTargets: Sequence["NotificationTargetItemTypeDef"] = ...,
        status: IncidentRecordStatusType = ...,
        summary: str = ...,
        title: str = ...
    ) -> Dict[str, Any]:
        """
        Update the details of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_incident_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_incident_record)
        """

    async def update_related_items(
        self,
        *,
        incidentRecordArn: str,
        relatedItemsUpdate: "RelatedItemsUpdateTypeDef",
        clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Add or remove related items from the related items tab of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_related_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_related_items)
        """

    async def update_replication_set(
        self,
        *,
        actions: Sequence["UpdateReplicationSetActionTypeDef"],
        arn: str,
        clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Add or delete Regions from your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_replication_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_replication_set)
        """

    async def update_response_plan(
        self,
        *,
        arn: str,
        actions: Sequence["ActionTypeDef"] = ...,
        chatChannel: "ChatChannelTypeDef" = ...,
        clientToken: str = ...,
        displayName: str = ...,
        engagements: Sequence[str] = ...,
        incidentTemplateDedupeString: str = ...,
        incidentTemplateImpact: int = ...,
        incidentTemplateNotificationTargets: Sequence["NotificationTargetItemTypeDef"] = ...,
        incidentTemplateSummary: str = ...,
        incidentTemplateTitle: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_response_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_response_plan)
        """

    async def update_timeline_event(
        self,
        *,
        eventId: str,
        incidentRecordArn: str,
        clientToken: str = ...,
        eventData: str = ...,
        eventTime: Union[datetime, str] = ...,
        eventType: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a timeline event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.update_timeline_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_timeline_event)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_incident_records"]
    ) -> ListIncidentRecordsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_related_items"]
    ) -> ListRelatedItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_replication_sets"]
    ) -> ListReplicationSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_response_plans"]
    ) -> ListResponsePlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_timeline_events"]
    ) -> ListTimelineEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["wait_for_replication_set_active"]
    ) -> WaitForReplicationSetActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["wait_for_replication_set_deleted"]
    ) -> WaitForReplicationSetDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_waiter)
        """

    async def __aenter__(self) -> "SSMIncidentsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
        """
