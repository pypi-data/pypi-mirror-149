"""
Type annotations for managedblockchain service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    FrameworkType,
    MemberStatusType,
    NetworkStatusType,
    NodeStatusType,
    VoteValueType,
)
from .type_defs import (
    CreateMemberOutputTypeDef,
    CreateNetworkOutputTypeDef,
    CreateNodeOutputTypeDef,
    CreateProposalOutputTypeDef,
    GetMemberOutputTypeDef,
    GetNetworkOutputTypeDef,
    GetNodeOutputTypeDef,
    GetProposalOutputTypeDef,
    ListInvitationsOutputTypeDef,
    ListMembersOutputTypeDef,
    ListNetworksOutputTypeDef,
    ListNodesOutputTypeDef,
    ListProposalsOutputTypeDef,
    ListProposalVotesOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    MemberConfigurationTypeDef,
    MemberLogPublishingConfigurationTypeDef,
    NetworkFrameworkConfigurationTypeDef,
    NodeConfigurationTypeDef,
    NodeLogPublishingConfigurationTypeDef,
    ProposalActionsTypeDef,
    VotingPolicyTypeDef,
)

__all__ = ("ManagedBlockchainClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IllegalActionException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class ManagedBlockchainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedBlockchainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#can_paginate)
        """
    async def create_member(
        self,
        *,
        ClientRequestToken: str,
        InvitationId: str,
        NetworkId: str,
        MemberConfiguration: "MemberConfigurationTypeDef"
    ) -> CreateMemberOutputTypeDef:
        """
        Creates a member within a Managed Blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_member)
        """
    async def create_network(
        self,
        *,
        ClientRequestToken: str,
        Name: str,
        Framework: FrameworkType,
        FrameworkVersion: str,
        VotingPolicy: "VotingPolicyTypeDef",
        MemberConfiguration: "MemberConfigurationTypeDef",
        Description: str = ...,
        FrameworkConfiguration: "NetworkFrameworkConfigurationTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateNetworkOutputTypeDef:
        """
        Creates a new blockchain network using Amazon Managed Blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_network)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_network)
        """
    async def create_node(
        self,
        *,
        ClientRequestToken: str,
        NetworkId: str,
        NodeConfiguration: "NodeConfigurationTypeDef",
        MemberId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateNodeOutputTypeDef:
        """
        Creates a node on the specified blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_node)
        """
    async def create_proposal(
        self,
        *,
        ClientRequestToken: str,
        NetworkId: str,
        MemberId: str,
        Actions: "ProposalActionsTypeDef",
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateProposalOutputTypeDef:
        """
        Creates a proposal for a change to the network that other members of the network
        can vote on, for example, a proposal to add a new member to the network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_proposal)
        """
    async def delete_member(self, *, NetworkId: str, MemberId: str) -> Dict[str, Any]:
        """
        Deletes a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.delete_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_member)
        """
    async def delete_node(
        self, *, NetworkId: str, NodeId: str, MemberId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a node that your AWS account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.delete_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_node)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#generate_presigned_url)
        """
    async def get_member(self, *, NetworkId: str, MemberId: str) -> GetMemberOutputTypeDef:
        """
        Returns detailed information about a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_member)
        """
    async def get_network(self, *, NetworkId: str) -> GetNetworkOutputTypeDef:
        """
        Returns detailed information about a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_network)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_network)
        """
    async def get_node(
        self, *, NetworkId: str, NodeId: str, MemberId: str = ...
    ) -> GetNodeOutputTypeDef:
        """
        Returns detailed information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_node)
        """
    async def get_proposal(self, *, NetworkId: str, ProposalId: str) -> GetProposalOutputTypeDef:
        """
        Returns detailed information about a proposal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_proposal)
        """
    async def list_invitations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListInvitationsOutputTypeDef:
        """
        Returns a list of all invitations for the current AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_invitations)
        """
    async def list_members(
        self,
        *,
        NetworkId: str,
        Name: str = ...,
        Status: MemberStatusType = ...,
        IsOwned: bool = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListMembersOutputTypeDef:
        """
        Returns a list of the members in a network and properties of their
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_members)
        """
    async def list_networks(
        self,
        *,
        Name: str = ...,
        Framework: FrameworkType = ...,
        Status: NetworkStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListNetworksOutputTypeDef:
        """
        Returns information about the networks in which the current AWS account
        participates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_networks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_networks)
        """
    async def list_nodes(
        self,
        *,
        NetworkId: str,
        MemberId: str = ...,
        Status: NodeStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListNodesOutputTypeDef:
        """
        Returns information about the nodes within a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_nodes)
        """
    async def list_proposal_votes(
        self, *, NetworkId: str, ProposalId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListProposalVotesOutputTypeDef:
        """
        Returns the list of votes for a specified proposal, including the value of each
        vote and the unique identifier of the member that cast the vote.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_proposal_votes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposal_votes)
        """
    async def list_proposals(
        self, *, NetworkId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListProposalsOutputTypeDef:
        """
        Returns a list of proposals for the network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_proposals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposals)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_tags_for_resource)
        """
    async def reject_invitation(self, *, InvitationId: str) -> Dict[str, Any]:
        """
        Rejects an invitation to join a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.reject_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#reject_invitation)
        """
    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or overwrites the specified tags for the specified Amazon Managed
        Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the Amazon Managed Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#untag_resource)
        """
    async def update_member(
        self,
        *,
        NetworkId: str,
        MemberId: str,
        LogPublishingConfiguration: "MemberLogPublishingConfigurationTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates a member configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.update_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_member)
        """
    async def update_node(
        self,
        *,
        NetworkId: str,
        NodeId: str,
        MemberId: str = ...,
        LogPublishingConfiguration: "NodeLogPublishingConfigurationTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates a node configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.update_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_node)
        """
    async def vote_on_proposal(
        self, *, NetworkId: str, ProposalId: str, VoterMemberId: str, Vote: VoteValueType
    ) -> Dict[str, Any]:
        """
        Casts a vote for a specified `ProposalId` on behalf of a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.vote_on_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#vote_on_proposal)
        """
    async def __aenter__(self) -> "ManagedBlockchainClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """
