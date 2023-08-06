"""
Main interface for health service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_health import (
        Client,
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsForOrganizationPaginator,
        DescribeEventsPaginator,
        HealthClient,
    )

    session = get_session()
    async with session.create_client("health") as client:
        client: HealthClient
        ...


    describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
    describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
    describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
    describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
    describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
    ```
"""
from .client import HealthClient
from .paginator import (
    DescribeAffectedAccountsForOrganizationPaginator,
    DescribeAffectedEntitiesForOrganizationPaginator,
    DescribeAffectedEntitiesPaginator,
    DescribeEventAggregatesPaginator,
    DescribeEventsForOrganizationPaginator,
    DescribeEventsPaginator,
    DescribeEventTypesPaginator,
)

Client = HealthClient

__all__ = (
    "Client",
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsForOrganizationPaginator",
    "DescribeEventsPaginator",
    "HealthClient",
)
