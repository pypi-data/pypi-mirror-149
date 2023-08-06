"""
Type annotations for route53-recovery-cluster service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient

    session = get_session()
    async with session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import RoutingControlStateType
from .type_defs import GetRoutingControlStateResponseTypeDef, UpdateRoutingControlStateEntryTypeDef

__all__ = ("Route53RecoveryClusterClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointTemporarilyUnavailableException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Route53RecoveryClusterClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryClusterClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#generate_presigned_url)
        """

    async def get_routing_control_state(
        self, *, RoutingControlArn: str
    ) -> GetRoutingControlStateResponseTypeDef:
        """
        Get the state for a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.get_routing_control_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#get_routing_control_state)
        """

    async def update_routing_control_state(
        self,
        *,
        RoutingControlArn: str,
        RoutingControlState: RoutingControlStateType,
        SafetyRulesToOverride: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Set the state of the routing control to reroute traffic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.update_routing_control_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#update_routing_control_state)
        """

    async def update_routing_control_states(
        self,
        *,
        UpdateRoutingControlStateEntries: Sequence["UpdateRoutingControlStateEntryTypeDef"],
        SafetyRulesToOverride: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Set multiple routing control states.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client.update_routing_control_states)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/#update_routing_control_states)
        """

    async def __aenter__(self) -> "Route53RecoveryClusterClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster.html#Route53RecoveryCluster.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/client/)
        """
