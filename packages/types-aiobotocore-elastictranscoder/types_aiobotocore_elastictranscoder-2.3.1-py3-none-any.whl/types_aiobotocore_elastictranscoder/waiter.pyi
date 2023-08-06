"""
Type annotations for elastictranscoder service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
    from types_aiobotocore_elastictranscoder.waiter import (
        JobCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("elastictranscoder") as client:
        client: ElasticTranscoderClient

        job_complete_waiter: JobCompleteWaiter = client.get_waiter("job_complete")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("JobCompleteWaiter",)

class JobCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Waiter.JobComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/#jobcompletewaiter)
    """

    async def wait(self, *, Id: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Waiter.JobComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/#jobcompletewaiter)
        """
