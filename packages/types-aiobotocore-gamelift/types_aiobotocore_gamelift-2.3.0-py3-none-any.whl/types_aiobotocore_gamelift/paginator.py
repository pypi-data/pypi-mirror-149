"""
Type annotations for gamelift service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_gamelift.client import GameLiftClient
    from types_aiobotocore_gamelift.paginator import (
        DescribeFleetAttributesPaginator,
        DescribeFleetCapacityPaginator,
        DescribeFleetEventsPaginator,
        DescribeFleetUtilizationPaginator,
        DescribeGameServerInstancesPaginator,
        DescribeGameSessionDetailsPaginator,
        DescribeGameSessionQueuesPaginator,
        DescribeGameSessionsPaginator,
        DescribeInstancesPaginator,
        DescribeMatchmakingConfigurationsPaginator,
        DescribeMatchmakingRuleSetsPaginator,
        DescribePlayerSessionsPaginator,
        DescribeScalingPoliciesPaginator,
        ListAliasesPaginator,
        ListBuildsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    session = get_session()
    with session.create_client("gamelift") as client:
        client: GameLiftClient

        describe_fleet_attributes_paginator: DescribeFleetAttributesPaginator = client.get_paginator("describe_fleet_attributes")
        describe_fleet_capacity_paginator: DescribeFleetCapacityPaginator = client.get_paginator("describe_fleet_capacity")
        describe_fleet_events_paginator: DescribeFleetEventsPaginator = client.get_paginator("describe_fleet_events")
        describe_fleet_utilization_paginator: DescribeFleetUtilizationPaginator = client.get_paginator("describe_fleet_utilization")
        describe_game_server_instances_paginator: DescribeGameServerInstancesPaginator = client.get_paginator("describe_game_server_instances")
        describe_game_session_details_paginator: DescribeGameSessionDetailsPaginator = client.get_paginator("describe_game_session_details")
        describe_game_session_queues_paginator: DescribeGameSessionQueuesPaginator = client.get_paginator("describe_game_session_queues")
        describe_game_sessions_paginator: DescribeGameSessionsPaginator = client.get_paginator("describe_game_sessions")
        describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
        describe_matchmaking_configurations_paginator: DescribeMatchmakingConfigurationsPaginator = client.get_paginator("describe_matchmaking_configurations")
        describe_matchmaking_rule_sets_paginator: DescribeMatchmakingRuleSetsPaginator = client.get_paginator("describe_matchmaking_rule_sets")
        describe_player_sessions_paginator: DescribePlayerSessionsPaginator = client.get_paginator("describe_player_sessions")
        describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_game_server_groups_paginator: ListGameServerGroupsPaginator = client.get_paginator("list_game_server_groups")
        list_game_servers_paginator: ListGameServersPaginator = client.get_paginator("list_game_servers")
        list_scripts_paginator: ListScriptsPaginator = client.get_paginator("list_scripts")
        search_game_sessions_paginator: SearchGameSessionsPaginator = client.get_paginator("search_game_sessions")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import BuildStatusType, RoutingStrategyTypeType, ScalingStatusTypeType, SortOrderType
from .type_defs import (
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersOutputTypeDef,
    ListScriptsOutputTypeDef,
    PaginatorConfigTypeDef,
    SearchGameSessionsOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "DescribeFleetAttributesPaginator",
    "DescribeFleetCapacityPaginator",
    "DescribeFleetEventsPaginator",
    "DescribeFleetUtilizationPaginator",
    "DescribeGameServerInstancesPaginator",
    "DescribeGameSessionDetailsPaginator",
    "DescribeGameSessionQueuesPaginator",
    "DescribeGameSessionsPaginator",
    "DescribeInstancesPaginator",
    "DescribeMatchmakingConfigurationsPaginator",
    "DescribeMatchmakingRuleSetsPaginator",
    "DescribePlayerSessionsPaginator",
    "DescribeScalingPoliciesPaginator",
    "ListAliasesPaginator",
    "ListBuildsPaginator",
    "ListFleetsPaginator",
    "ListGameServerGroupsPaginator",
    "ListGameServersPaginator",
    "ListScriptsPaginator",
    "SearchGameSessionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeFleetAttributesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
        """


class DescribeFleetCapacityPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
        """


class DescribeFleetEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
        """


class DescribeFleetUtilizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
    """

    def paginate(
        self, *, FleetIds: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
        """


class DescribeGameServerInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
    """

    def paginate(
        self,
        *,
        GameServerGroupName: str,
        InstanceIds: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
        """


class DescribeGameSessionDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
        """


class DescribeGameSessionQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
    """

    def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
        """


class DescribeGameSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        GameSessionId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        StatusFilter: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
        """


class DescribeInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        InstanceId: str = ...,
        Location: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
        """


class DescribeMatchmakingConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        Names: Sequence[str] = ...,
        RuleSetName: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """


class DescribeMatchmakingRuleSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
    """

    def paginate(
        self, *, Names: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
        """


class DescribePlayerSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
    """

    def paginate(
        self,
        *,
        GameSessionId: str = ...,
        PlayerId: str = ...,
        PlayerSessionId: str = ...,
        PlayerSessionStatusFilter: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
        """


class DescribeScalingPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str,
        StatusFilter: ScalingStatusTypeType = ...,
        Location: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
        """


class ListAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
    """

    def paginate(
        self,
        *,
        RoutingStrategyType: RoutingStrategyTypeType = ...,
        Name: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
        """


class ListBuildsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListBuilds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
    """

    def paginate(
        self, *, Status: BuildStatusType = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListBuilds.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
        """


class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
    """

    def paginate(
        self,
        *,
        BuildId: str = ...,
        ScriptId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
        """


class ListGameServerGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
        """


class ListGameServersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
    """

    def paginate(
        self,
        *,
        GameServerGroupName: str,
        SortOrder: SortOrderType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListGameServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
        """


class ListScriptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListScripts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.ListScripts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
        """


class SearchGameSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
    """

    def paginate(
        self,
        *,
        FleetId: str = ...,
        AliasId: str = ...,
        Location: str = ...,
        FilterExpression: str = ...,
        SortExpression: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
        """
