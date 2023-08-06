"""
Main interface for kms service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kms import (
        Client,
        KMSClient,
        ListAliasesPaginator,
        ListGrantsPaginator,
        ListKeyPoliciesPaginator,
        ListKeysPaginator,
    )

    session = get_session()
    async with session.create_client("kms") as client:
        client: KMSClient
        ...


    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_grants_paginator: ListGrantsPaginator = client.get_paginator("list_grants")
    list_key_policies_paginator: ListKeyPoliciesPaginator = client.get_paginator("list_key_policies")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```
"""
from .client import KMSClient
from .paginator import (
    ListAliasesPaginator,
    ListGrantsPaginator,
    ListKeyPoliciesPaginator,
    ListKeysPaginator,
)

Client = KMSClient

__all__ = (
    "Client",
    "KMSClient",
    "ListAliasesPaginator",
    "ListGrantsPaginator",
    "ListKeyPoliciesPaginator",
    "ListKeysPaginator",
)
