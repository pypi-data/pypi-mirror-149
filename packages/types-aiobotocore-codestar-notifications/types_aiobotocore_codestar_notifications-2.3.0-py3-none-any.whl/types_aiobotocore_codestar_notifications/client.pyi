"""
Type annotations for codestar-notifications service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient

    session = get_session()
    async with session.create_client("codestar-notifications") as client:
        client: CodeStarNotificationsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import DetailTypeType, NotificationRuleStatusType
from .paginator import ListEventTypesPaginator, ListNotificationRulesPaginator, ListTargetsPaginator
from .type_defs import (
    CreateNotificationRuleResultTypeDef,
    DeleteNotificationRuleResultTypeDef,
    DescribeNotificationRuleResultTypeDef,
    ListEventTypesFilterTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesFilterTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTagsForResourceResultTypeDef,
    ListTargetsFilterTypeDef,
    ListTargetsResultTypeDef,
    SubscribeResultTypeDef,
    TagResourceResultTypeDef,
    TargetTypeDef,
    UnsubscribeResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CodeStarNotificationsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConfigurationException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeStarNotificationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeStarNotificationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#can_paginate)
        """
    async def create_notification_rule(
        self,
        *,
        Name: str,
        EventTypeIds: Sequence[str],
        Resource: str,
        Targets: Sequence["TargetTypeDef"],
        DetailType: DetailTypeType,
        ClientRequestToken: str = ...,
        Tags: Mapping[str, str] = ...,
        Status: NotificationRuleStatusType = ...
    ) -> CreateNotificationRuleResultTypeDef:
        """
        Creates a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.create_notification_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#create_notification_rule)
        """
    async def delete_notification_rule(self, *, Arn: str) -> DeleteNotificationRuleResultTypeDef:
        """
        Deletes a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.delete_notification_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#delete_notification_rule)
        """
    async def delete_target(
        self, *, TargetAddress: str, ForceUnsubscribeAll: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified target for notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.delete_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#delete_target)
        """
    async def describe_notification_rule(
        self, *, Arn: str
    ) -> DescribeNotificationRuleResultTypeDef:
        """
        Returns information about a specified notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.describe_notification_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#describe_notification_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#generate_presigned_url)
        """
    async def list_event_types(
        self,
        *,
        Filters: Sequence["ListEventTypesFilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListEventTypesResultTypeDef:
        """
        Returns information about the event types available for configuring
        notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.list_event_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_event_types)
        """
    async def list_notification_rules(
        self,
        *,
        Filters: Sequence["ListNotificationRulesFilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListNotificationRulesResultTypeDef:
        """
        Returns a list of the notification rules for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.list_notification_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_notification_rules)
        """
    async def list_tags_for_resource(self, *, Arn: str) -> ListTagsForResourceResultTypeDef:
        """
        Returns a list of the tags associated with a notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_tags_for_resource)
        """
    async def list_targets(
        self,
        *,
        Filters: Sequence["ListTargetsFilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListTargetsResultTypeDef:
        """
        Returns a list of the notification rule targets for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.list_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_targets)
        """
    async def subscribe(
        self, *, Arn: str, Target: "TargetTypeDef", ClientRequestToken: str = ...
    ) -> SubscribeResultTypeDef:
        """
        Creates an association between a notification rule and an SNS topic so that the
        associated target can receive notifications when the events described in the
        rule are triggered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.subscribe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#subscribe)
        """
    async def tag_resource(self, *, Arn: str, Tags: Mapping[str, str]) -> TagResourceResultTypeDef:
        """
        Associates a set of provided tags with a notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#tag_resource)
        """
    async def unsubscribe(self, *, Arn: str, TargetAddress: str) -> UnsubscribeResultTypeDef:
        """
        Removes an association between a notification rule and an Amazon SNS topic so
        that subscribers to that topic stop receiving notifications when the events
        described in the rule are triggered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.unsubscribe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#unsubscribe)
        """
    async def untag_resource(self, *, Arn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the association between one or more provided tags and a notification
        rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#untag_resource)
        """
    async def update_notification_rule(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Status: NotificationRuleStatusType = ...,
        EventTypeIds: Sequence[str] = ...,
        Targets: Sequence["TargetTypeDef"] = ...,
        DetailType: DetailTypeType = ...
    ) -> Dict[str, Any]:
        """
        Updates a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.update_notification_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#update_notification_rule)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_event_types"]) -> ListEventTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_rules"]
    ) -> ListNotificationRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_targets"]) -> ListTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """
    async def __aenter__(self) -> "CodeStarNotificationsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
        """
