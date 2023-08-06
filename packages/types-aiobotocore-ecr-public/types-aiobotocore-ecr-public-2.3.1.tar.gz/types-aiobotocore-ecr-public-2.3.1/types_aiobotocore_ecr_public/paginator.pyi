"""
Type annotations for ecr-public service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecr_public.client import ECRPublicClient
    from types_aiobotocore_ecr_public.paginator import (
        DescribeImageTagsPaginator,
        DescribeImagesPaginator,
        DescribeRegistriesPaginator,
        DescribeRepositoriesPaginator,
    )

    session = get_session()
    with session.create_client("ecr-public") as client:
        client: ECRPublicClient

        describe_image_tags_paginator: DescribeImageTagsPaginator = client.get_paginator("describe_image_tags")
        describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
        describe_registries_paginator: DescribeRegistriesPaginator = client.get_paginator("describe_registries")
        describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeImagesResponseTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesResponseTypeDef,
    ImageIdentifierTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeImageTagsPaginator",
    "DescribeImagesPaginator",
    "DescribeRegistriesPaginator",
    "DescribeRepositoriesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeImageTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeImageTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagetagspaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeImageTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeImageTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagetagspaginator)
        """

class DescribeImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagespaginator)
    """

    def paginate(
        self,
        *,
        repositoryName: str,
        registryId: str = ...,
        imageIds: Sequence["ImageIdentifierTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagespaginator)
        """

class DescribeRegistriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeRegistries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeregistriespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeRegistries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeregistriespaginator)
        """

class DescribeRepositoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeRepositories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describerepositoriespaginator)
    """

    def paginate(
        self,
        *,
        registryId: str = ...,
        repositoryNames: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Paginator.DescribeRepositories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describerepositoriespaginator)
        """
