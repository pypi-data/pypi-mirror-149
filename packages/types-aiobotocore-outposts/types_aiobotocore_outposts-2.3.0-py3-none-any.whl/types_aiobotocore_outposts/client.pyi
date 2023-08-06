"""
Type annotations for outposts service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_outposts.client import OutpostsClient

    session = get_session()
    async with session.create_client("outposts") as client:
        client: OutpostsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AddressTypeType,
    CatalogItemClassType,
    FiberOpticCableTypeType,
    MaximumSupportedWeightLbsType,
    OpticalStandardType,
    PaymentOptionType,
    PowerConnectorType,
    PowerDrawKvaType,
    PowerFeedDropType,
    PowerPhaseType,
    SupportedHardwareTypeType,
    SupportedStorageEnumType,
    UplinkCountType,
    UplinkGbpsType,
)
from .type_defs import (
    AddressTypeDef,
    CreateOrderOutputTypeDef,
    CreateOutpostOutputTypeDef,
    CreateSiteOutputTypeDef,
    GetCatalogItemOutputTypeDef,
    GetOrderOutputTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostOutputTypeDef,
    GetSiteAddressOutputTypeDef,
    GetSiteOutputTypeDef,
    LineItemRequestTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    RackPhysicalPropertiesTypeDef,
    UpdateOutpostOutputTypeDef,
    UpdateSiteAddressOutputTypeDef,
    UpdateSiteOutputTypeDef,
    UpdateSiteRackPhysicalPropertiesOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("OutpostsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class OutpostsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OutpostsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#can_paginate)
        """
    async def cancel_order(self, *, OrderId: str) -> Dict[str, Any]:
        """
        Cancels an order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.cancel_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#cancel_order)
        """
    async def create_order(
        self,
        *,
        OutpostIdentifier: str,
        LineItems: Sequence["LineItemRequestTypeDef"],
        PaymentOption: PaymentOptionType,
        PaymentTerm: Literal["THREE_YEARS"] = ...
    ) -> CreateOrderOutputTypeDef:
        """
        Creates an order for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#create_order)
        """
    async def create_outpost(
        self,
        *,
        Name: str,
        SiteId: str,
        Description: str = ...,
        AvailabilityZone: str = ...,
        AvailabilityZoneId: str = ...,
        Tags: Mapping[str, str] = ...,
        SupportedHardwareType: SupportedHardwareTypeType = ...
    ) -> CreateOutpostOutputTypeDef:
        """
        Creates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_outpost)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#create_outpost)
        """
    async def create_site(
        self,
        *,
        Name: str,
        Description: str = ...,
        Notes: str = ...,
        Tags: Mapping[str, str] = ...,
        OperatingAddress: "AddressTypeDef" = ...,
        ShippingAddress: "AddressTypeDef" = ...,
        RackPhysicalProperties: "RackPhysicalPropertiesTypeDef" = ...
    ) -> CreateSiteOutputTypeDef:
        """
        Creates a site for an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.create_site)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#create_site)
        """
    async def delete_outpost(self, *, OutpostId: str) -> Dict[str, Any]:
        """
        Deletes the Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_outpost)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#delete_outpost)
        """
    async def delete_site(self, *, SiteId: str) -> Dict[str, Any]:
        """
        Deletes the site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.delete_site)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#delete_site)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#generate_presigned_url)
        """
    async def get_catalog_item(self, *, CatalogItemId: str) -> GetCatalogItemOutputTypeDef:
        """
        Gets information about a catalog item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_catalog_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_catalog_item)
        """
    async def get_order(self, *, OrderId: str) -> GetOrderOutputTypeDef:
        """
        Gets an order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_order)
        """
    async def get_outpost(self, *, OutpostId: str) -> GetOutpostOutputTypeDef:
        """
        Gets information about the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_outpost)
        """
    async def get_outpost_instance_types(
        self, *, OutpostId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetOutpostInstanceTypesOutputTypeDef:
        """
        Lists the instance types for the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_outpost_instance_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_outpost_instance_types)
        """
    async def get_site(self, *, SiteId: str) -> GetSiteOutputTypeDef:
        """
        Gets information about the specified Outpost site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_site)
        """
    async def get_site_address(
        self, *, SiteId: str, AddressType: AddressTypeType
    ) -> GetSiteAddressOutputTypeDef:
        """
        Gets the site address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.get_site_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#get_site_address)
        """
    async def list_catalog_items(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        ItemClassFilter: Sequence[CatalogItemClassType] = ...,
        SupportedStorageFilter: Sequence[SupportedStorageEnumType] = ...,
        EC2FamilyFilter: Sequence[str] = ...
    ) -> ListCatalogItemsOutputTypeDef:
        """
        Use to create a list of every item in the catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_catalog_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#list_catalog_items)
        """
    async def list_orders(
        self, *, OutpostIdentifierFilter: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrdersOutputTypeDef:
        """
        Create a list of the Outpost orders for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_orders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#list_orders)
        """
    async def list_outposts(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        LifeCycleStatusFilter: Sequence[str] = ...,
        AvailabilityZoneFilter: Sequence[str] = ...,
        AvailabilityZoneIdFilter: Sequence[str] = ...
    ) -> ListOutpostsOutputTypeDef:
        """
        Create a list of the Outposts for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_outposts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#list_outposts)
        """
    async def list_sites(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        OperatingAddressCountryCodeFilter: Sequence[str] = ...,
        OperatingAddressStateOrRegionFilter: Sequence[str] = ...,
        OperatingAddressCityFilter: Sequence[str] = ...
    ) -> ListSitesOutputTypeDef:
        """
        Create a list of the Outpost sites for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_sites)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#list_sites)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#list_tags_for_resource)
        """
    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#untag_resource)
        """
    async def update_outpost(
        self,
        *,
        OutpostId: str,
        Name: str = ...,
        Description: str = ...,
        SupportedHardwareType: SupportedHardwareTypeType = ...
    ) -> UpdateOutpostOutputTypeDef:
        """
        Updates an Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_outpost)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#update_outpost)
        """
    async def update_site(
        self, *, SiteId: str, Name: str = ..., Description: str = ..., Notes: str = ...
    ) -> UpdateSiteOutputTypeDef:
        """
        Updates the site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#update_site)
        """
    async def update_site_address(
        self, *, SiteId: str, AddressType: AddressTypeType, Address: "AddressTypeDef"
    ) -> UpdateSiteAddressOutputTypeDef:
        """
        Updates the site address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#update_site_address)
        """
    async def update_site_rack_physical_properties(
        self,
        *,
        SiteId: str,
        PowerDrawKva: PowerDrawKvaType = ...,
        PowerPhase: PowerPhaseType = ...,
        PowerConnector: PowerConnectorType = ...,
        PowerFeedDrop: PowerFeedDropType = ...,
        UplinkGbps: UplinkGbpsType = ...,
        UplinkCount: UplinkCountType = ...,
        FiberOpticCableType: FiberOpticCableTypeType = ...,
        OpticalStandard: OpticalStandardType = ...,
        MaximumSupportedWeightLbs: MaximumSupportedWeightLbsType = ...
    ) -> UpdateSiteRackPhysicalPropertiesOutputTypeDef:
        """
        Update the physical and logistical details for a rack at a site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client.update_site_rack_physical_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/#update_site_rack_physical_properties)
        """
    async def __aenter__(self) -> "OutpostsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts.html#Outposts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/client/)
        """
