"""
Type annotations for mturk service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mturk.client import MTurkClient
    from types_aiobotocore_mturk.paginator import (
        ListAssignmentsForHITPaginator,
        ListBonusPaymentsPaginator,
        ListHITsPaginator,
        ListHITsForQualificationTypePaginator,
        ListQualificationRequestsPaginator,
        ListQualificationTypesPaginator,
        ListReviewableHITsPaginator,
        ListWorkerBlocksPaginator,
        ListWorkersWithQualificationTypePaginator,
    )

    session = get_session()
    with session.create_client("mturk") as client:
        client: MTurkClient

        list_assignments_for_hit_paginator: ListAssignmentsForHITPaginator = client.get_paginator("list_assignments_for_hit")
        list_bonus_payments_paginator: ListBonusPaymentsPaginator = client.get_paginator("list_bonus_payments")
        list_hits_paginator: ListHITsPaginator = client.get_paginator("list_hits")
        list_hits_for_qualification_type_paginator: ListHITsForQualificationTypePaginator = client.get_paginator("list_hits_for_qualification_type")
        list_qualification_requests_paginator: ListQualificationRequestsPaginator = client.get_paginator("list_qualification_requests")
        list_qualification_types_paginator: ListQualificationTypesPaginator = client.get_paginator("list_qualification_types")
        list_reviewable_hits_paginator: ListReviewableHITsPaginator = client.get_paginator("list_reviewable_hits")
        list_worker_blocks_paginator: ListWorkerBlocksPaginator = client.get_paginator("list_worker_blocks")
        list_workers_with_qualification_type_paginator: ListWorkersWithQualificationTypePaginator = client.get_paginator("list_workers_with_qualification_type")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import AssignmentStatusType, QualificationStatusType, ReviewableHITStatusType
from .type_defs import (
    ListAssignmentsForHITResponseTypeDef,
    ListBonusPaymentsResponseTypeDef,
    ListHITsForQualificationTypeResponseTypeDef,
    ListHITsResponseTypeDef,
    ListQualificationRequestsResponseTypeDef,
    ListQualificationTypesResponseTypeDef,
    ListReviewableHITsResponseTypeDef,
    ListWorkerBlocksResponseTypeDef,
    ListWorkersWithQualificationTypeResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListAssignmentsForHITPaginator",
    "ListBonusPaymentsPaginator",
    "ListHITsPaginator",
    "ListHITsForQualificationTypePaginator",
    "ListQualificationRequestsPaginator",
    "ListQualificationTypesPaginator",
    "ListReviewableHITsPaginator",
    "ListWorkerBlocksPaginator",
    "ListWorkersWithQualificationTypePaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssignmentsForHITPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListAssignmentsForHIT)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listassignmentsforhitpaginator)
    """

    def paginate(
        self,
        *,
        HITId: str,
        AssignmentStatuses: Sequence[AssignmentStatusType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAssignmentsForHITResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListAssignmentsForHIT.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listassignmentsforhitpaginator)
        """


class ListBonusPaymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListBonusPayments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listbonuspaymentspaginator)
    """

    def paginate(
        self,
        *,
        HITId: str = ...,
        AssignmentId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBonusPaymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListBonusPayments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listbonuspaymentspaginator)
        """


class ListHITsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListHITs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHITsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListHITs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitspaginator)
        """


class ListHITsForQualificationTypePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListHITsForQualificationType)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitsforqualificationtypepaginator)
    """

    def paginate(
        self, *, QualificationTypeId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHITsForQualificationTypeResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListHITsForQualificationType.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitsforqualificationtypepaginator)
        """


class ListQualificationRequestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListQualificationRequests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationrequestspaginator)
    """

    def paginate(
        self, *, QualificationTypeId: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListQualificationRequestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListQualificationRequests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationrequestspaginator)
        """


class ListQualificationTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListQualificationTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationtypespaginator)
    """

    def paginate(
        self,
        *,
        MustBeRequestable: bool,
        Query: str = ...,
        MustBeOwnedByCaller: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListQualificationTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListQualificationTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationtypespaginator)
        """


class ListReviewableHITsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListReviewableHITs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listreviewablehitspaginator)
    """

    def paginate(
        self,
        *,
        HITTypeId: str = ...,
        Status: ReviewableHITStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListReviewableHITsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListReviewableHITs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listreviewablehitspaginator)
        """


class ListWorkerBlocksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListWorkerBlocks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerblockspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListWorkerBlocksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListWorkerBlocks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerblockspaginator)
        """


class ListWorkersWithQualificationTypePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListWorkersWithQualificationType)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerswithqualificationtypepaginator)
    """

    def paginate(
        self,
        *,
        QualificationTypeId: str,
        Status: QualificationStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListWorkersWithQualificationTypeResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Paginator.ListWorkersWithQualificationType.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerswithqualificationtypepaginator)
        """
