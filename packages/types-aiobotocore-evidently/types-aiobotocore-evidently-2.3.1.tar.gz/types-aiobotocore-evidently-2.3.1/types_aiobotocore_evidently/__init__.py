"""
Main interface for evidently service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_evidently import (
        Client,
        CloudWatchEvidentlyClient,
        ListExperimentsPaginator,
        ListFeaturesPaginator,
        ListLaunchesPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    async with session.create_client("evidently") as client:
        client: CloudWatchEvidentlyClient
        ...


    list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
    list_features_paginator: ListFeaturesPaginator = client.get_paginator("list_features")
    list_launches_paginator: ListLaunchesPaginator = client.get_paginator("list_launches")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```
"""
from .client import CloudWatchEvidentlyClient
from .paginator import (
    ListExperimentsPaginator,
    ListFeaturesPaginator,
    ListLaunchesPaginator,
    ListProjectsPaginator,
)

Client = CloudWatchEvidentlyClient


__all__ = (
    "Client",
    "CloudWatchEvidentlyClient",
    "ListExperimentsPaginator",
    "ListFeaturesPaginator",
    "ListLaunchesPaginator",
    "ListProjectsPaginator",
)
