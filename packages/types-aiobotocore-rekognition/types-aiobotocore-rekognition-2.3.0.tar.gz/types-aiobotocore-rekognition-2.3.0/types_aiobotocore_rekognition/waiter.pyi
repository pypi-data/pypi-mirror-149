"""
Type annotations for rekognition service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_rekognition.waiter import (
        ProjectVersionRunningWaiter,
        ProjectVersionTrainingCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("rekognition") as client:
        client: RekognitionClient

        project_version_running_waiter: ProjectVersionRunningWaiter = client.get_waiter("project_version_running")
        project_version_training_completed_waiter: ProjectVersionTrainingCompletedWaiter = client.get_waiter("project_version_training_completed")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("ProjectVersionRunningWaiter", "ProjectVersionTrainingCompletedWaiter")

class ProjectVersionRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversionrunningwaiter)
    """

    async def wait(
        self,
        *,
        ProjectArn: str,
        VersionNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversionrunningwaiter)
        """

class ProjectVersionTrainingCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionTrainingCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversiontrainingcompletedwaiter)
    """

    async def wait(
        self,
        *,
        ProjectArn: str,
        VersionNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionTrainingCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversiontrainingcompletedwaiter)
        """
