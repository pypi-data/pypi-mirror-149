"""
Type annotations for elastic-inference service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elastic_inference.client import ElasticInferenceClient

    session = get_session()
    async with session.create_client("elastic-inference") as client:
        client: ElasticInferenceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import LocationTypeType
from .paginator import DescribeAcceleratorsPaginator
from .type_defs import (
    DescribeAcceleratorOfferingsResponseTypeDef,
    DescribeAcceleratorsResponseTypeDef,
    DescribeAcceleratorTypesResponseTypeDef,
    FilterTypeDef,
    ListTagsForResourceResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ElasticInferenceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class ElasticInferenceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticInferenceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#can_paginate)
        """

    async def describe_accelerator_offerings(
        self, *, locationType: LocationTypeType, acceleratorTypes: Sequence[str] = ...
    ) -> DescribeAcceleratorOfferingsResponseTypeDef:
        """
        Describes the locations in which a given accelerator type or set of types is
        present in a given region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerator_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#describe_accelerator_offerings)
        """

    async def describe_accelerator_types(self) -> DescribeAcceleratorTypesResponseTypeDef:
        """
        Describes the accelerator types available in a given region, as well as their
        characteristics, such as memory and throughput.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerator_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#describe_accelerator_types)
        """

    async def describe_accelerators(
        self,
        *,
        acceleratorIds: Sequence[str] = ...,
        filters: Sequence["FilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeAcceleratorsResponseTypeDef:
        """
        Describes information over a provided set of accelerators belonging to an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#describe_accelerators)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#generate_presigned_url)
        """

    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResultTypeDef:
        """
        Returns all tags of an Elastic Inference Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#list_tags_for_resource)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds the specified tags to an Elastic Inference Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from an Elastic Inference Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#untag_resource)
        """

    def get_paginator(
        self, operation_name: Literal["describe_accelerators"]
    ) -> DescribeAcceleratorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/#get_paginator)
        """

    async def __aenter__(self) -> "ElasticInferenceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/client/)
        """
