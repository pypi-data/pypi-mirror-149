"""
Main interface for network-firewall service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_network_firewall import (
        Client,
        ListFirewallPoliciesPaginator,
        ListFirewallsPaginator,
        ListRuleGroupsPaginator,
        ListTagsForResourcePaginator,
        NetworkFirewallClient,
    )

    session = get_session()
    async with session.create_client("network-firewall") as client:
        client: NetworkFirewallClient
        ...


    list_firewall_policies_paginator: ListFirewallPoliciesPaginator = client.get_paginator("list_firewall_policies")
    list_firewalls_paginator: ListFirewallsPaginator = client.get_paginator("list_firewalls")
    list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from .client import NetworkFirewallClient
from .paginator import (
    ListFirewallPoliciesPaginator,
    ListFirewallsPaginator,
    ListRuleGroupsPaginator,
    ListTagsForResourcePaginator,
)

Client = NetworkFirewallClient


__all__ = (
    "Client",
    "ListFirewallPoliciesPaginator",
    "ListFirewallsPaginator",
    "ListRuleGroupsPaginator",
    "ListTagsForResourcePaginator",
    "NetworkFirewallClient",
)
