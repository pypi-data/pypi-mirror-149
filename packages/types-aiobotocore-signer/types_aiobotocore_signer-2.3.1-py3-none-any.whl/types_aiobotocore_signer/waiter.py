"""
Type annotations for signer service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_signer.client import signerClient
    from types_aiobotocore_signer.waiter import (
        SuccessfulSigningJobWaiter,
    )

    session = get_session()
    async with session.create_client("signer") as client:
        client: signerClient

        successful_signing_job_waiter: SuccessfulSigningJobWaiter = client.get_waiter("successful_signing_job")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("SuccessfulSigningJobWaiter",)


class SuccessfulSigningJobWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Waiter.SuccessfulSigningJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/#successfulsigningjobwaiter)
    """

    async def wait(self, *, jobId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer.html#signer.Waiter.SuccessfulSigningJob.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/waiters/#successfulsigningjobwaiter)
        """
