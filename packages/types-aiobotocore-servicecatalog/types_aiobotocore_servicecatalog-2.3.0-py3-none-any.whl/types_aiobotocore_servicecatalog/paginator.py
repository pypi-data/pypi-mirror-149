"""
Type annotations for servicecatalog service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_servicecatalog.client import ServiceCatalogClient
    from types_aiobotocore_servicecatalog.paginator import (
        ListAcceptedPortfolioSharesPaginator,
        ListConstraintsForPortfolioPaginator,
        ListLaunchPathsPaginator,
        ListOrganizationPortfolioAccessPaginator,
        ListPortfoliosPaginator,
        ListPortfoliosForProductPaginator,
        ListPrincipalsForPortfolioPaginator,
        ListProvisionedProductPlansPaginator,
        ListProvisioningArtifactsForServiceActionPaginator,
        ListRecordHistoryPaginator,
        ListResourcesForTagOptionPaginator,
        ListServiceActionsPaginator,
        ListServiceActionsForProvisioningArtifactPaginator,
        ListTagOptionsPaginator,
        ScanProvisionedProductsPaginator,
        SearchProductsAsAdminPaginator,
    )

    session = get_session()
    with session.create_client("servicecatalog") as client:
        client: ServiceCatalogClient

        list_accepted_portfolio_shares_paginator: ListAcceptedPortfolioSharesPaginator = client.get_paginator("list_accepted_portfolio_shares")
        list_constraints_for_portfolio_paginator: ListConstraintsForPortfolioPaginator = client.get_paginator("list_constraints_for_portfolio")
        list_launch_paths_paginator: ListLaunchPathsPaginator = client.get_paginator("list_launch_paths")
        list_organization_portfolio_access_paginator: ListOrganizationPortfolioAccessPaginator = client.get_paginator("list_organization_portfolio_access")
        list_portfolios_paginator: ListPortfoliosPaginator = client.get_paginator("list_portfolios")
        list_portfolios_for_product_paginator: ListPortfoliosForProductPaginator = client.get_paginator("list_portfolios_for_product")
        list_principals_for_portfolio_paginator: ListPrincipalsForPortfolioPaginator = client.get_paginator("list_principals_for_portfolio")
        list_provisioned_product_plans_paginator: ListProvisionedProductPlansPaginator = client.get_paginator("list_provisioned_product_plans")
        list_provisioning_artifacts_for_service_action_paginator: ListProvisioningArtifactsForServiceActionPaginator = client.get_paginator("list_provisioning_artifacts_for_service_action")
        list_record_history_paginator: ListRecordHistoryPaginator = client.get_paginator("list_record_history")
        list_resources_for_tag_option_paginator: ListResourcesForTagOptionPaginator = client.get_paginator("list_resources_for_tag_option")
        list_service_actions_paginator: ListServiceActionsPaginator = client.get_paginator("list_service_actions")
        list_service_actions_for_provisioning_artifact_paginator: ListServiceActionsForProvisioningArtifactPaginator = client.get_paginator("list_service_actions_for_provisioning_artifact")
        list_tag_options_paginator: ListTagOptionsPaginator = client.get_paginator("list_tag_options")
        scan_provisioned_products_paginator: ScanProvisionedProductsPaginator = client.get_paginator("scan_provisioned_products")
        search_products_as_admin_paginator: SearchProductsAsAdminPaginator = client.get_paginator("search_products_as_admin")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    OrganizationNodeTypeType,
    PortfolioShareTypeType,
    ProductViewFilterByType,
    ProductViewSortByType,
    SortOrderType,
)
from .type_defs import (
    AccessLevelFilterTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListRecordHistorySearchFilterTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsOutputTypeDef,
    ListTagOptionsFiltersTypeDef,
    ListTagOptionsOutputTypeDef,
    PaginatorConfigTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator
if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAcceptedPortfolioSharesPaginator",
    "ListConstraintsForPortfolioPaginator",
    "ListLaunchPathsPaginator",
    "ListOrganizationPortfolioAccessPaginator",
    "ListPortfoliosPaginator",
    "ListPortfoliosForProductPaginator",
    "ListPrincipalsForPortfolioPaginator",
    "ListProvisionedProductPlansPaginator",
    "ListProvisioningArtifactsForServiceActionPaginator",
    "ListRecordHistoryPaginator",
    "ListResourcesForTagOptionPaginator",
    "ListServiceActionsPaginator",
    "ListServiceActionsForProvisioningArtifactPaginator",
    "ListTagOptionsPaginator",
    "ScanProvisionedProductsPaginator",
    "SearchProductsAsAdminPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAcceptedPortfolioSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        PortfolioShareType: PortfolioShareTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAcceptedPortfolioSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
        """


class ListConstraintsForPortfolioPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        ProductId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListConstraintsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
        """


class ListLaunchPathsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListLaunchPaths)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListLaunchPathsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListLaunchPaths.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
        """


class ListOrganizationPortfolioAccessPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        OrganizationNodeType: OrganizationNodeTypeType,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOrganizationPortfolioAccessOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
        """


class ListPortfoliosPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
    """

    def paginate(
        self, *, AcceptLanguage: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPortfoliosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
        """


class ListPortfoliosForProductPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfoliosForProduct)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPortfoliosForProductOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfoliosForProduct.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
        """


class ListPrincipalsForPortfolioPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
    """

    def paginate(
        self,
        *,
        PortfolioId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPrincipalsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
        """


class ListProvisionedProductPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisionedProductPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        ProvisionProductId: str = ...,
        AccessLevelFilter: "AccessLevelFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListProvisionedProductPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisionedProductPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
        """


class ListProvisioningArtifactsForServiceActionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
    """

    def paginate(
        self,
        *,
        ServiceActionId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListProvisioningArtifactsForServiceActionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
        """


class ListRecordHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListRecordHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: "AccessLevelFilterTypeDef" = ...,
        SearchFilter: "ListRecordHistorySearchFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRecordHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListRecordHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
        """


class ListResourcesForTagOptionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListResourcesForTagOption)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
    """

    def paginate(
        self,
        *,
        TagOptionId: str,
        ResourceType: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListResourcesForTagOptionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListResourcesForTagOption.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
        """


class ListServiceActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
    """

    def paginate(
        self, *, AcceptLanguage: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListServiceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
        """


class ListServiceActionsForProvisioningArtifactPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
    """

    def paginate(
        self,
        *,
        ProductId: str,
        ProvisioningArtifactId: str,
        AcceptLanguage: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListServiceActionsForProvisioningArtifactOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
        """


class ListTagOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListTagOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
    """

    def paginate(
        self,
        *,
        Filters: "ListTagOptionsFiltersTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListTagOptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
        """


class ScanProvisionedProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ScanProvisionedProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        AccessLevelFilter: "AccessLevelFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ScanProvisionedProductsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ScanProvisionedProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
        """


class SearchProductsAsAdminPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.SearchProductsAsAdmin)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
    """

    def paginate(
        self,
        *,
        AcceptLanguage: str = ...,
        PortfolioId: str = ...,
        Filters: Mapping[ProductViewFilterByType, Sequence[str]] = ...,
        SortBy: ProductViewSortByType = ...,
        SortOrder: SortOrderType = ...,
        ProductSource: Literal["ACCOUNT"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SearchProductsAsAdminOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.SearchProductsAsAdmin.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
        """
