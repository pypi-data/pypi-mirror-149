"""
Type annotations for network-firewall service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_network_firewall.client import NetworkFirewallClient

    session = get_session()
    async with session.create_client("network-firewall") as client:
        client: NetworkFirewallClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ResourceManagedStatusType, RuleGroupTypeType
from .paginator import (
    ListFirewallPoliciesPaginator,
    ListFirewallsPaginator,
    ListRuleGroupsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AssociateFirewallPolicyResponseTypeDef,
    AssociateSubnetsResponseTypeDef,
    CreateFirewallPolicyResponseTypeDef,
    CreateFirewallResponseTypeDef,
    CreateRuleGroupResponseTypeDef,
    DeleteFirewallPolicyResponseTypeDef,
    DeleteFirewallResponseTypeDef,
    DeleteRuleGroupResponseTypeDef,
    DescribeFirewallPolicyResponseTypeDef,
    DescribeFirewallResponseTypeDef,
    DescribeLoggingConfigurationResponseTypeDef,
    DescribeResourcePolicyResponseTypeDef,
    DescribeRuleGroupMetadataResponseTypeDef,
    DescribeRuleGroupResponseTypeDef,
    DisassociateSubnetsResponseTypeDef,
    FirewallPolicyTypeDef,
    ListFirewallPoliciesResponseTypeDef,
    ListFirewallsResponseTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LoggingConfigurationTypeDef,
    RuleGroupTypeDef,
    SubnetMappingTypeDef,
    TagTypeDef,
    UpdateFirewallDeleteProtectionResponseTypeDef,
    UpdateFirewallDescriptionResponseTypeDef,
    UpdateFirewallPolicyChangeProtectionResponseTypeDef,
    UpdateFirewallPolicyResponseTypeDef,
    UpdateLoggingConfigurationResponseTypeDef,
    UpdateRuleGroupResponseTypeDef,
    UpdateSubnetChangeProtectionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("NetworkFirewallClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InsufficientCapacityException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResourcePolicyException: Type[BotocoreClientError]
    InvalidTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LogDestinationPermissionException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceOwnerCheckException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class NetworkFirewallClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NetworkFirewallClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#exceptions)
        """

    async def associate_firewall_policy(
        self,
        *,
        FirewallPolicyArn: str,
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> AssociateFirewallPolicyResponseTypeDef:
        """
        Associates a  FirewallPolicy to a  Firewall .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.associate_firewall_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#associate_firewall_policy)
        """

    async def associate_subnets(
        self,
        *,
        SubnetMappings: Sequence["SubnetMappingTypeDef"],
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> AssociateSubnetsResponseTypeDef:
        """
        Associates the specified subnets in the Amazon VPC to the firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.associate_subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#associate_subnets)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#can_paginate)
        """

    async def create_firewall(
        self,
        *,
        FirewallName: str,
        FirewallPolicyArn: str,
        VpcId: str,
        SubnetMappings: Sequence["SubnetMappingTypeDef"],
        DeleteProtection: bool = ...,
        SubnetChangeProtection: bool = ...,
        FirewallPolicyChangeProtection: bool = ...,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateFirewallResponseTypeDef:
        """
        Creates an AWS Network Firewall  Firewall and accompanying  FirewallStatus for a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.create_firewall)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#create_firewall)
        """

    async def create_firewall_policy(
        self,
        *,
        FirewallPolicyName: str,
        FirewallPolicy: "FirewallPolicyTypeDef",
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DryRun: bool = ...
    ) -> CreateFirewallPolicyResponseTypeDef:
        """
        Creates the firewall policy for the firewall according to the specifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.create_firewall_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#create_firewall_policy)
        """

    async def create_rule_group(
        self,
        *,
        RuleGroupName: str,
        Type: RuleGroupTypeType,
        Capacity: int,
        RuleGroup: "RuleGroupTypeDef" = ...,
        Rules: str = ...,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DryRun: bool = ...
    ) -> CreateRuleGroupResponseTypeDef:
        """
        Creates the specified stateless or stateful rule group, which includes the rules
        for network traffic inspection, a capacity setting, and tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.create_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#create_rule_group)
        """

    async def delete_firewall(
        self, *, FirewallName: str = ..., FirewallArn: str = ...
    ) -> DeleteFirewallResponseTypeDef:
        """
        Deletes the specified  Firewall and its  FirewallStatus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.delete_firewall)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#delete_firewall)
        """

    async def delete_firewall_policy(
        self, *, FirewallPolicyName: str = ..., FirewallPolicyArn: str = ...
    ) -> DeleteFirewallPolicyResponseTypeDef:
        """
        Deletes the specified  FirewallPolicy .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.delete_firewall_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#delete_firewall_policy)
        """

    async def delete_resource_policy(self, *, ResourceArn: str) -> Dict[str, Any]:
        """
        Deletes a resource policy that you created in a  PutResourcePolicy request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#delete_resource_policy)
        """

    async def delete_rule_group(
        self, *, RuleGroupName: str = ..., RuleGroupArn: str = ..., Type: RuleGroupTypeType = ...
    ) -> DeleteRuleGroupResponseTypeDef:
        """
        Deletes the specified  RuleGroup .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.delete_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#delete_rule_group)
        """

    async def describe_firewall(
        self, *, FirewallName: str = ..., FirewallArn: str = ...
    ) -> DescribeFirewallResponseTypeDef:
        """
        Returns the data objects for the specified firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_firewall)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_firewall)
        """

    async def describe_firewall_policy(
        self, *, FirewallPolicyName: str = ..., FirewallPolicyArn: str = ...
    ) -> DescribeFirewallPolicyResponseTypeDef:
        """
        Returns the data objects for the specified firewall policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_firewall_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_firewall_policy)
        """

    async def describe_logging_configuration(
        self, *, FirewallArn: str = ..., FirewallName: str = ...
    ) -> DescribeLoggingConfigurationResponseTypeDef:
        """
        Returns the logging configuration for the specified firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_logging_configuration)
        """

    async def describe_resource_policy(
        self, *, ResourceArn: str
    ) -> DescribeResourcePolicyResponseTypeDef:
        """
        Retrieves a resource policy that you created in a  PutResourcePolicy request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_resource_policy)
        """

    async def describe_rule_group(
        self, *, RuleGroupName: str = ..., RuleGroupArn: str = ..., Type: RuleGroupTypeType = ...
    ) -> DescribeRuleGroupResponseTypeDef:
        """
        Returns the data objects for the specified rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_rule_group)
        """

    async def describe_rule_group_metadata(
        self, *, RuleGroupName: str = ..., RuleGroupArn: str = ..., Type: RuleGroupTypeType = ...
    ) -> DescribeRuleGroupMetadataResponseTypeDef:
        """
        High-level information about a rule group, returned by operations like create
        and describe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.describe_rule_group_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#describe_rule_group_metadata)
        """

    async def disassociate_subnets(
        self,
        *,
        SubnetIds: Sequence[str],
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> DisassociateSubnetsResponseTypeDef:
        """
        Removes the specified subnet associations from the firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.disassociate_subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#disassociate_subnets)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#generate_presigned_url)
        """

    async def list_firewall_policies(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFirewallPoliciesResponseTypeDef:
        """
        Retrieves the metadata for the firewall policies that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.list_firewall_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#list_firewall_policies)
        """

    async def list_firewalls(
        self, *, NextToken: str = ..., VpcIds: Sequence[str] = ..., MaxResults: int = ...
    ) -> ListFirewallsResponseTypeDef:
        """
        Retrieves the metadata for the firewalls that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.list_firewalls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#list_firewalls)
        """

    async def list_rule_groups(
        self, *, NextToken: str = ..., MaxResults: int = ..., Scope: ResourceManagedStatusType = ...
    ) -> ListRuleGroupsResponseTypeDef:
        """
        Retrieves the metadata for the rule groups that you have defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.list_rule_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#list_rule_groups)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#list_tags_for_resource)
        """

    async def put_resource_policy(self, *, ResourceArn: str, Policy: str) -> Dict[str, Any]:
        """
        Creates or updates an AWS Identity and Access Management policy for your rule
        group or firewall policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#put_resource_policy)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the tags with the specified keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#untag_resource)
        """

    async def update_firewall_delete_protection(
        self,
        *,
        DeleteProtection: bool,
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> UpdateFirewallDeleteProtectionResponseTypeDef:
        """
        Modifies the flag, `DeleteProtection` , which indicates whether it is possible
        to delete the firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_delete_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_firewall_delete_protection)
        """

    async def update_firewall_description(
        self,
        *,
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...,
        Description: str = ...
    ) -> UpdateFirewallDescriptionResponseTypeDef:
        """
        Modifies the description for the specified firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_firewall_description)
        """

    async def update_firewall_policy(
        self,
        *,
        UpdateToken: str,
        FirewallPolicy: "FirewallPolicyTypeDef",
        FirewallPolicyArn: str = ...,
        FirewallPolicyName: str = ...,
        Description: str = ...,
        DryRun: bool = ...
    ) -> UpdateFirewallPolicyResponseTypeDef:
        """
        Updates the properties of the specified firewall policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_firewall_policy)
        """

    async def update_firewall_policy_change_protection(
        self,
        *,
        FirewallPolicyChangeProtection: bool,
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> UpdateFirewallPolicyChangeProtectionResponseTypeDef:
        """
        Modifies the flag, `ChangeProtection` , which indicates whether it is possible
        to change the firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_firewall_policy_change_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_firewall_policy_change_protection)
        """

    async def update_logging_configuration(
        self,
        *,
        FirewallArn: str = ...,
        FirewallName: str = ...,
        LoggingConfiguration: "LoggingConfigurationTypeDef" = ...
    ) -> UpdateLoggingConfigurationResponseTypeDef:
        """
        Sets the logging configuration for the specified firewall.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_logging_configuration)
        """

    async def update_rule_group(
        self,
        *,
        UpdateToken: str,
        RuleGroupArn: str = ...,
        RuleGroupName: str = ...,
        RuleGroup: "RuleGroupTypeDef" = ...,
        Rules: str = ...,
        Type: RuleGroupTypeType = ...,
        Description: str = ...,
        DryRun: bool = ...
    ) -> UpdateRuleGroupResponseTypeDef:
        """
        Updates the rule settings for the specified rule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_rule_group)
        """

    async def update_subnet_change_protection(
        self,
        *,
        SubnetChangeProtection: bool,
        UpdateToken: str = ...,
        FirewallArn: str = ...,
        FirewallName: str = ...
    ) -> UpdateSubnetChangeProtectionResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/network-
        firewall-2020-11-12/UpdateSubnetChangeProtection).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.update_subnet_change_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#update_subnet_change_protection)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_firewall_policies"]
    ) -> ListFirewallPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_firewalls"]) -> ListFirewallsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rule_groups"]) -> ListRuleGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/#get_paginator)
        """

    async def __aenter__(self) -> "NetworkFirewallClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall.html#NetworkFirewall.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/client/)
        """
