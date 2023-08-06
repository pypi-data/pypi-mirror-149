"""
Type annotations for directconnect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_directconnect.client import DirectConnectClient

    session = get_session()
    async with session.create_client("directconnect") as client:
        client: DirectConnectClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeDirectConnectGatewayAssociationsPaginator,
    DescribeDirectConnectGatewayAttachmentsPaginator,
    DescribeDirectConnectGatewaysPaginator,
)
from .type_defs import (
    AcceptDirectConnectGatewayAssociationProposalResultTypeDef,
    AllocateTransitVirtualInterfaceResultTypeDef,
    AssociateMacSecKeyResponseTypeDef,
    ConfirmConnectionResponseTypeDef,
    ConfirmCustomerAgreementResponseTypeDef,
    ConfirmPrivateVirtualInterfaceResponseTypeDef,
    ConfirmPublicVirtualInterfaceResponseTypeDef,
    ConfirmTransitVirtualInterfaceResponseTypeDef,
    ConnectionResponseMetadataTypeDef,
    ConnectionsTypeDef,
    CreateBGPPeerResponseTypeDef,
    CreateDirectConnectGatewayAssociationProposalResultTypeDef,
    CreateDirectConnectGatewayAssociationResultTypeDef,
    CreateDirectConnectGatewayResultTypeDef,
    CreateTransitVirtualInterfaceResultTypeDef,
    DeleteBGPPeerResponseTypeDef,
    DeleteDirectConnectGatewayAssociationProposalResultTypeDef,
    DeleteDirectConnectGatewayAssociationResultTypeDef,
    DeleteDirectConnectGatewayResultTypeDef,
    DeleteInterconnectResponseTypeDef,
    DeleteVirtualInterfaceResponseTypeDef,
    DescribeConnectionLoaResponseTypeDef,
    DescribeCustomerMetadataResponseTypeDef,
    DescribeDirectConnectGatewayAssociationProposalsResultTypeDef,
    DescribeDirectConnectGatewayAssociationsResultTypeDef,
    DescribeDirectConnectGatewayAttachmentsResultTypeDef,
    DescribeDirectConnectGatewaysResultTypeDef,
    DescribeInterconnectLoaResponseTypeDef,
    DescribeRouterConfigurationResponseTypeDef,
    DescribeTagsResponseTypeDef,
    DisassociateMacSecKeyResponseTypeDef,
    InterconnectResponseMetadataTypeDef,
    InterconnectsTypeDef,
    LagResponseMetadataTypeDef,
    LagsTypeDef,
    ListVirtualInterfaceTestHistoryResponseTypeDef,
    LoaResponseMetadataTypeDef,
    LocationsTypeDef,
    NewBGPPeerTypeDef,
    NewPrivateVirtualInterfaceAllocationTypeDef,
    NewPrivateVirtualInterfaceTypeDef,
    NewPublicVirtualInterfaceAllocationTypeDef,
    NewPublicVirtualInterfaceTypeDef,
    NewTransitVirtualInterfaceAllocationTypeDef,
    NewTransitVirtualInterfaceTypeDef,
    RouteFilterPrefixTypeDef,
    StartBgpFailoverTestResponseTypeDef,
    StopBgpFailoverTestResponseTypeDef,
    TagTypeDef,
    UpdateDirectConnectGatewayAssociationResultTypeDef,
    UpdateDirectConnectGatewayResponseTypeDef,
    VirtualGatewaysTypeDef,
    VirtualInterfaceResponseMetadataTypeDef,
    VirtualInterfacesTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DirectConnectClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DirectConnectClientException: Type[BotocoreClientError]
    DirectConnectServerException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class DirectConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DirectConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#exceptions)
        """
    async def accept_direct_connect_gateway_association_proposal(
        self,
        *,
        directConnectGatewayId: str,
        proposalId: str,
        associatedGatewayOwnerAccount: str,
        overrideAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...
    ) -> AcceptDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Accepts a proposal request to attach a virtual private gateway or transit
        gateway to a Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.accept_direct_connect_gateway_association_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#accept_direct_connect_gateway_association_proposal)
        """
    async def allocate_connection_on_interconnect(
        self,
        *,
        bandwidth: str,
        connectionName: str,
        ownerAccount: str,
        interconnectId: str,
        vlan: int
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.allocate_connection_on_interconnect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_connection_on_interconnect)
        """
    async def allocate_hosted_connection(
        self,
        *,
        connectionId: str,
        ownerAccount: str,
        bandwidth: str,
        connectionName: str,
        vlan: int,
        tags: Sequence["TagTypeDef"] = ...
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Creates a hosted connection on the specified interconnect or a link aggregation
        group (LAG) of interconnects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.allocate_hosted_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_hosted_connection)
        """
    async def allocate_private_virtual_interface(
        self,
        *,
        connectionId: str,
        ownerAccount: str,
        newPrivateVirtualInterfaceAllocation: "NewPrivateVirtualInterfaceAllocationTypeDef"
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Provisions a private virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.allocate_private_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_private_virtual_interface)
        """
    async def allocate_public_virtual_interface(
        self,
        *,
        connectionId: str,
        ownerAccount: str,
        newPublicVirtualInterfaceAllocation: "NewPublicVirtualInterfaceAllocationTypeDef"
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Provisions a public virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.allocate_public_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_public_virtual_interface)
        """
    async def allocate_transit_virtual_interface(
        self,
        *,
        connectionId: str,
        ownerAccount: str,
        newTransitVirtualInterfaceAllocation: "NewTransitVirtualInterfaceAllocationTypeDef"
    ) -> AllocateTransitVirtualInterfaceResultTypeDef:
        """
        Provisions a transit virtual interface to be owned by the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.allocate_transit_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#allocate_transit_virtual_interface)
        """
    async def associate_connection_with_lag(
        self, *, connectionId: str, lagId: str
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Associates an existing connection with a link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.associate_connection_with_lag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_connection_with_lag)
        """
    async def associate_hosted_connection(
        self, *, connectionId: str, parentConnectionId: str
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Associates a hosted connection and its virtual interfaces with a link
        aggregation group (LAG) or interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.associate_hosted_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_hosted_connection)
        """
    async def associate_mac_sec_key(
        self, *, connectionId: str, secretARN: str = ..., ckn: str = ..., cak: str = ...
    ) -> AssociateMacSecKeyResponseTypeDef:
        """
        Associates a MAC Security (MACsec) Connection Key Name (CKN)/ Connectivity
        Association Key (CAK) pair with an Direct Connect dedicated connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.associate_mac_sec_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_mac_sec_key)
        """
    async def associate_virtual_interface(
        self, *, virtualInterfaceId: str, connectionId: str
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Associates a virtual interface with a specified link aggregation group (LAG) or
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.associate_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#associate_virtual_interface)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#can_paginate)
        """
    async def confirm_connection(self, *, connectionId: str) -> ConfirmConnectionResponseTypeDef:
        """
        Confirms the creation of the specified hosted connection on an interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_connection)
        """
    async def confirm_customer_agreement(
        self, *, agreementName: str = ...
    ) -> ConfirmCustomerAgreementResponseTypeDef:
        """
        The confirmation of the terms of agreement when creating the connection/link
        aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_customer_agreement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_customer_agreement)
        """
    async def confirm_private_virtual_interface(
        self,
        *,
        virtualInterfaceId: str,
        virtualGatewayId: str = ...,
        directConnectGatewayId: str = ...
    ) -> ConfirmPrivateVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a private virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_private_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_private_virtual_interface)
        """
    async def confirm_public_virtual_interface(
        self, *, virtualInterfaceId: str
    ) -> ConfirmPublicVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a public virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_public_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_public_virtual_interface)
        """
    async def confirm_transit_virtual_interface(
        self, *, virtualInterfaceId: str, directConnectGatewayId: str
    ) -> ConfirmTransitVirtualInterfaceResponseTypeDef:
        """
        Accepts ownership of a transit virtual interface created by another Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.confirm_transit_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#confirm_transit_virtual_interface)
        """
    async def create_bgp_peer(
        self, *, virtualInterfaceId: str = ..., newBGPPeer: "NewBGPPeerTypeDef" = ...
    ) -> CreateBGPPeerResponseTypeDef:
        """
        Creates a BGP peer on the specified virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_bgp_peer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_bgp_peer)
        """
    async def create_connection(
        self,
        *,
        location: str,
        bandwidth: str,
        connectionName: str,
        lagId: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        providerName: str = ...,
        requestMACSec: bool = ...
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Creates a connection between a customer network and a specific Direct Connect
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_connection)
        """
    async def create_direct_connect_gateway(
        self, *, directConnectGatewayName: str, amazonSideAsn: int = ...
    ) -> CreateDirectConnectGatewayResultTypeDef:
        """
        Creates a Direct Connect gateway, which is an intermediate object that enables
        you to connect a set of virtual interfaces and virtual private gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_direct_connect_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway)
        """
    async def create_direct_connect_gateway_association(
        self,
        *,
        directConnectGatewayId: str,
        gatewayId: str = ...,
        addAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...,
        virtualGatewayId: str = ...
    ) -> CreateDirectConnectGatewayAssociationResultTypeDef:
        """
        Creates an association between a Direct Connect gateway and a virtual private
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_direct_connect_gateway_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway_association)
        """
    async def create_direct_connect_gateway_association_proposal(
        self,
        *,
        directConnectGatewayId: str,
        directConnectGatewayOwnerAccount: str,
        gatewayId: str,
        addAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...,
        removeAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...
    ) -> CreateDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Creates a proposal to associate the specified virtual private gateway or transit
        gateway with the specified Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_direct_connect_gateway_association_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_direct_connect_gateway_association_proposal)
        """
    async def create_interconnect(
        self,
        *,
        interconnectName: str,
        bandwidth: str,
        location: str,
        lagId: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        providerName: str = ...
    ) -> InterconnectResponseMetadataTypeDef:
        """
        Creates an interconnect between an Direct Connect Partner's network and a
        specific Direct Connect location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_interconnect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_interconnect)
        """
    async def create_lag(
        self,
        *,
        numberOfConnections: int,
        location: str,
        connectionsBandwidth: str,
        lagName: str,
        connectionId: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        childConnectionTags: Sequence["TagTypeDef"] = ...,
        providerName: str = ...,
        requestMACSec: bool = ...
    ) -> LagResponseMetadataTypeDef:
        """
        Creates a link aggregation group (LAG) with the specified number of bundled
        physical dedicated connections between the customer network and a specific
        Direct Connect location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_lag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_lag)
        """
    async def create_private_virtual_interface(
        self, *, connectionId: str, newPrivateVirtualInterface: "NewPrivateVirtualInterfaceTypeDef"
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Creates a private virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_private_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_private_virtual_interface)
        """
    async def create_public_virtual_interface(
        self, *, connectionId: str, newPublicVirtualInterface: "NewPublicVirtualInterfaceTypeDef"
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Creates a public virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_public_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_public_virtual_interface)
        """
    async def create_transit_virtual_interface(
        self, *, connectionId: str, newTransitVirtualInterface: "NewTransitVirtualInterfaceTypeDef"
    ) -> CreateTransitVirtualInterfaceResultTypeDef:
        """
        Creates a transit virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.create_transit_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#create_transit_virtual_interface)
        """
    async def delete_bgp_peer(
        self,
        *,
        virtualInterfaceId: str = ...,
        asn: int = ...,
        customerAddress: str = ...,
        bgpPeerId: str = ...
    ) -> DeleteBGPPeerResponseTypeDef:
        """
        Deletes the specified BGP peer on the specified virtual interface with the
        specified customer address and ASN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_bgp_peer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_bgp_peer)
        """
    async def delete_connection(self, *, connectionId: str) -> ConnectionResponseMetadataTypeDef:
        """
        Deletes the specified connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_connection)
        """
    async def delete_direct_connect_gateway(
        self, *, directConnectGatewayId: str
    ) -> DeleteDirectConnectGatewayResultTypeDef:
        """
        Deletes the specified Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_direct_connect_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway)
        """
    async def delete_direct_connect_gateway_association(
        self,
        *,
        associationId: str = ...,
        directConnectGatewayId: str = ...,
        virtualGatewayId: str = ...
    ) -> DeleteDirectConnectGatewayAssociationResultTypeDef:
        """
        Deletes the association between the specified Direct Connect gateway and virtual
        private gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_direct_connect_gateway_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway_association)
        """
    async def delete_direct_connect_gateway_association_proposal(
        self, *, proposalId: str
    ) -> DeleteDirectConnectGatewayAssociationProposalResultTypeDef:
        """
        Deletes the association proposal request between the specified Direct Connect
        gateway and virtual private gateway or transit gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_direct_connect_gateway_association_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_direct_connect_gateway_association_proposal)
        """
    async def delete_interconnect(
        self, *, interconnectId: str
    ) -> DeleteInterconnectResponseTypeDef:
        """
        Deletes the specified interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_interconnect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_interconnect)
        """
    async def delete_lag(self, *, lagId: str) -> LagResponseMetadataTypeDef:
        """
        Deletes the specified link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_lag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_lag)
        """
    async def delete_virtual_interface(
        self, *, virtualInterfaceId: str
    ) -> DeleteVirtualInterfaceResponseTypeDef:
        """
        Deletes a virtual interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.delete_virtual_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#delete_virtual_interface)
        """
    async def describe_connection_loa(
        self,
        *,
        connectionId: str,
        providerName: str = ...,
        loaContentType: Literal["application/pdf"] = ...
    ) -> DescribeConnectionLoaResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_connection_loa)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connection_loa)
        """
    async def describe_connections(self, *, connectionId: str = ...) -> ConnectionsTypeDef:
        """
        Displays the specified connection or all connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connections)
        """
    async def describe_connections_on_interconnect(
        self, *, interconnectId: str
    ) -> ConnectionsTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_connections_on_interconnect)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_connections_on_interconnect)
        """
    async def describe_customer_metadata(self) -> DescribeCustomerMetadataResponseTypeDef:
        """
        Get and view a list of customer agreements, along with their signed status and
        whether the customer is an NNIPartner, NNIPartnerV2, or a nonPartner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_customer_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_customer_metadata)
        """
    async def describe_direct_connect_gateway_association_proposals(
        self,
        *,
        directConnectGatewayId: str = ...,
        proposalId: str = ...,
        associatedGatewayId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeDirectConnectGatewayAssociationProposalsResultTypeDef:
        """
        Describes one or more association proposals for connection between a virtual
        private gateway or transit gateway and a Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_direct_connect_gateway_association_proposals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_association_proposals)
        """
    async def describe_direct_connect_gateway_associations(
        self,
        *,
        associationId: str = ...,
        associatedGatewayId: str = ...,
        directConnectGatewayId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        virtualGatewayId: str = ...
    ) -> DescribeDirectConnectGatewayAssociationsResultTypeDef:
        """
        Lists the associations between your Direct Connect gateways and virtual private
        gateways and transit gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_direct_connect_gateway_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_associations)
        """
    async def describe_direct_connect_gateway_attachments(
        self,
        *,
        directConnectGatewayId: str = ...,
        virtualInterfaceId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeDirectConnectGatewayAttachmentsResultTypeDef:
        """
        Lists the attachments between your Direct Connect gateways and virtual
        interfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_direct_connect_gateway_attachments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateway_attachments)
        """
    async def describe_direct_connect_gateways(
        self, *, directConnectGatewayId: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> DescribeDirectConnectGatewaysResultTypeDef:
        """
        Lists all your Direct Connect gateways or only the specified Direct Connect
        gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_direct_connect_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_direct_connect_gateways)
        """
    async def describe_hosted_connections(self, *, connectionId: str) -> ConnectionsTypeDef:
        """
        Lists the hosted connections that have been provisioned on the specified
        interconnect or link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_hosted_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_hosted_connections)
        """
    async def describe_interconnect_loa(
        self,
        *,
        interconnectId: str,
        providerName: str = ...,
        loaContentType: Literal["application/pdf"] = ...
    ) -> DescribeInterconnectLoaResponseTypeDef:
        """
        Deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_interconnect_loa)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_interconnect_loa)
        """
    async def describe_interconnects(self, *, interconnectId: str = ...) -> InterconnectsTypeDef:
        """
        Lists the interconnects owned by the Amazon Web Services account or only the
        specified interconnect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_interconnects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_interconnects)
        """
    async def describe_lags(self, *, lagId: str = ...) -> LagsTypeDef:
        """
        Describes all your link aggregation groups (LAG) or the specified LAG.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_lags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_lags)
        """
    async def describe_loa(
        self,
        *,
        connectionId: str,
        providerName: str = ...,
        loaContentType: Literal["application/pdf"] = ...
    ) -> LoaResponseMetadataTypeDef:
        """
        Gets the LOA-CFA for a connection, interconnect, or link aggregation group
        (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_loa)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_loa)
        """
    async def describe_locations(self) -> LocationsTypeDef:
        """
        Lists the Direct Connect locations in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_locations)
        """
    async def describe_router_configuration(
        self, *, virtualInterfaceId: str, routerTypeIdentifier: str = ...
    ) -> DescribeRouterConfigurationResponseTypeDef:
        """
        Details about the router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_router_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_router_configuration)
        """
    async def describe_tags(self, *, resourceArns: Sequence[str]) -> DescribeTagsResponseTypeDef:
        """
        Describes the tags associated with the specified Direct Connect resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_tags)
        """
    async def describe_virtual_gateways(self) -> VirtualGatewaysTypeDef:
        """
        Lists the virtual private gateways owned by the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_virtual_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_virtual_gateways)
        """
    async def describe_virtual_interfaces(
        self, *, connectionId: str = ..., virtualInterfaceId: str = ...
    ) -> VirtualInterfacesTypeDef:
        """
        Displays all virtual interfaces for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.describe_virtual_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#describe_virtual_interfaces)
        """
    async def disassociate_connection_from_lag(
        self, *, connectionId: str, lagId: str
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Disassociates a connection from a link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.disassociate_connection_from_lag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#disassociate_connection_from_lag)
        """
    async def disassociate_mac_sec_key(
        self, *, connectionId: str, secretARN: str
    ) -> DisassociateMacSecKeyResponseTypeDef:
        """
        Removes the association between a MAC Security (MACsec) security key and an
        Direct Connect dedicated connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.disassociate_mac_sec_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#disassociate_mac_sec_key)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#generate_presigned_url)
        """
    async def list_virtual_interface_test_history(
        self,
        *,
        testId: str = ...,
        virtualInterfaceId: str = ...,
        bgpPeers: Sequence[str] = ...,
        status: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListVirtualInterfaceTestHistoryResponseTypeDef:
        """
        Lists the virtual interface failover test history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.list_virtual_interface_test_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#list_virtual_interface_test_history)
        """
    async def start_bgp_failover_test(
        self,
        *,
        virtualInterfaceId: str,
        bgpPeers: Sequence[str] = ...,
        testDurationInMinutes: int = ...
    ) -> StartBgpFailoverTestResponseTypeDef:
        """
        Starts the virtual interface failover test that verifies your configuration
        meets your resiliency requirements by placing the BGP peering session in the
        DOWN state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.start_bgp_failover_test)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#start_bgp_failover_test)
        """
    async def stop_bgp_failover_test(
        self, *, virtualInterfaceId: str
    ) -> StopBgpFailoverTestResponseTypeDef:
        """
        Stops the virtual interface failover test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.stop_bgp_failover_test)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#stop_bgp_failover_test)
        """
    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified Direct Connect resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Direct Connect resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#untag_resource)
        """
    async def update_connection(
        self, *, connectionId: str, connectionName: str = ..., encryptionMode: str = ...
    ) -> ConnectionResponseMetadataTypeDef:
        """
        Updates the Direct Connect dedicated connection configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.update_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_connection)
        """
    async def update_direct_connect_gateway(
        self, *, directConnectGatewayId: str, newDirectConnectGatewayName: str
    ) -> UpdateDirectConnectGatewayResponseTypeDef:
        """
        Updates the name of a current Direct Connect gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.update_direct_connect_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_direct_connect_gateway)
        """
    async def update_direct_connect_gateway_association(
        self,
        *,
        associationId: str = ...,
        addAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...,
        removeAllowedPrefixesToDirectConnectGateway: Sequence["RouteFilterPrefixTypeDef"] = ...
    ) -> UpdateDirectConnectGatewayAssociationResultTypeDef:
        """
        Updates the specified attributes of the Direct Connect gateway association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.update_direct_connect_gateway_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_direct_connect_gateway_association)
        """
    async def update_lag(
        self, *, lagId: str, lagName: str = ..., minimumLinks: int = ..., encryptionMode: str = ...
    ) -> LagResponseMetadataTypeDef:
        """
        Updates the attributes of the specified link aggregation group (LAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.update_lag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_lag)
        """
    async def update_virtual_interface_attributes(
        self,
        *,
        virtualInterfaceId: str,
        mtu: int = ...,
        enableSiteLink: bool = ...,
        virtualInterfaceName: str = ...
    ) -> VirtualInterfaceResponseMetadataTypeDef:
        """
        Updates the specified attributes of the specified virtual private interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.update_virtual_interface_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#update_virtual_interface_attributes)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateway_associations"]
    ) -> DescribeDirectConnectGatewayAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateway_attachments"]
    ) -> DescribeDirectConnectGatewayAttachmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_direct_connect_gateways"]
    ) -> DescribeDirectConnectGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/#get_paginator)
        """
    async def __aenter__(self) -> "DirectConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect.html#DirectConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/client/)
        """
