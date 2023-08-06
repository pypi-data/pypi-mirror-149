"""
Type annotations for elastictranscoder service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
    from types_aiobotocore_elastictranscoder.paginator import (
        ListJobsByPipelinePaginator,
        ListJobsByStatusPaginator,
        ListPipelinesPaginator,
        ListPresetsPaginator,
    )

    session = get_session()
    with session.create_client("elastictranscoder") as client:
        client: ElasticTranscoderClient

        list_jobs_by_pipeline_paginator: ListJobsByPipelinePaginator = client.get_paginator("list_jobs_by_pipeline")
        list_jobs_by_status_paginator: ListJobsByStatusPaginator = client.get_paginator("list_jobs_by_status")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListJobsByPipelineResponseTypeDef,
    ListJobsByStatusResponseTypeDef,
    ListPipelinesResponseTypeDef,
    ListPresetsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListJobsByPipelinePaginator",
    "ListJobsByStatusPaginator",
    "ListPipelinesPaginator",
    "ListPresetsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobsByPipelinePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByPipeline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbypipelinepaginator)
    """

    def paginate(
        self,
        *,
        PipelineId: str,
        Ascending: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobsByPipelineResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByPipeline.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbypipelinepaginator)
        """


class ListJobsByStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbystatuspaginator)
    """

    def paginate(
        self, *, Status: str, Ascending: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobsByStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListJobsByStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listjobsbystatuspaginator)
        """


class ListPipelinesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpipelinespaginator)
    """

    def paginate(
        self, *, Ascending: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpipelinespaginator)
        """


class ListPresetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPresets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpresetspaginator)
    """

    def paginate(
        self, *, Ascending: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Paginator.ListPresets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/paginators/#listpresetspaginator)
        """
