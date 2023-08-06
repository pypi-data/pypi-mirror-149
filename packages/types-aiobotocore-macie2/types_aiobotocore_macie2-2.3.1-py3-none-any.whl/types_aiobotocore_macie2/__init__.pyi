"""
Main interface for macie2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_macie2 import (
        Client,
        DescribeBucketsPaginator,
        GetUsageStatisticsPaginator,
        ListClassificationJobsPaginator,
        ListCustomDataIdentifiersPaginator,
        ListFindingsFiltersPaginator,
        ListFindingsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        Macie2Client,
        SearchResourcesPaginator,
    )

    session = get_session()
    async with session.create_client("macie2") as client:
        client: Macie2Client
        ...


    describe_buckets_paginator: DescribeBucketsPaginator = client.get_paginator("describe_buckets")
    get_usage_statistics_paginator: GetUsageStatisticsPaginator = client.get_paginator("get_usage_statistics")
    list_classification_jobs_paginator: ListClassificationJobsPaginator = client.get_paginator("list_classification_jobs")
    list_custom_data_identifiers_paginator: ListCustomDataIdentifiersPaginator = client.get_paginator("list_custom_data_identifiers")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_findings_filters_paginator: ListFindingsFiltersPaginator = client.get_paginator("list_findings_filters")
    list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
    search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
from .client import Macie2Client
from .paginator import (
    DescribeBucketsPaginator,
    GetUsageStatisticsPaginator,
    ListClassificationJobsPaginator,
    ListCustomDataIdentifiersPaginator,
    ListFindingsFiltersPaginator,
    ListFindingsPaginator,
    ListInvitationsPaginator,
    ListMembersPaginator,
    ListOrganizationAdminAccountsPaginator,
    SearchResourcesPaginator,
)

Client = Macie2Client

__all__ = (
    "Client",
    "DescribeBucketsPaginator",
    "GetUsageStatisticsPaginator",
    "ListClassificationJobsPaginator",
    "ListCustomDataIdentifiersPaginator",
    "ListFindingsFiltersPaginator",
    "ListFindingsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "Macie2Client",
    "SearchResourcesPaginator",
)
