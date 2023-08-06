"""
Type annotations for lex-models service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lex_models.client import LexModelBuildingServiceClient
    from types_aiobotocore_lex_models.paginator import (
        GetBotAliasesPaginator,
        GetBotChannelAssociationsPaginator,
        GetBotVersionsPaginator,
        GetBotsPaginator,
        GetBuiltinIntentsPaginator,
        GetBuiltinSlotTypesPaginator,
        GetIntentVersionsPaginator,
        GetIntentsPaginator,
        GetSlotTypeVersionsPaginator,
        GetSlotTypesPaginator,
    )

    session = get_session()
    with session.create_client("lex-models") as client:
        client: LexModelBuildingServiceClient

        get_bot_aliases_paginator: GetBotAliasesPaginator = client.get_paginator("get_bot_aliases")
        get_bot_channel_associations_paginator: GetBotChannelAssociationsPaginator = client.get_paginator("get_bot_channel_associations")
        get_bot_versions_paginator: GetBotVersionsPaginator = client.get_paginator("get_bot_versions")
        get_bots_paginator: GetBotsPaginator = client.get_paginator("get_bots")
        get_builtin_intents_paginator: GetBuiltinIntentsPaginator = client.get_paginator("get_builtin_intents")
        get_builtin_slot_types_paginator: GetBuiltinSlotTypesPaginator = client.get_paginator("get_builtin_slot_types")
        get_intent_versions_paginator: GetIntentVersionsPaginator = client.get_paginator("get_intent_versions")
        get_intents_paginator: GetIntentsPaginator = client.get_paginator("get_intents")
        get_slot_type_versions_paginator: GetSlotTypeVersionsPaginator = client.get_paginator("get_slot_type_versions")
        get_slot_types_paginator: GetSlotTypesPaginator = client.get_paginator("get_slot_types")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import LocaleType
from .type_defs import (
    GetBotAliasesResponseTypeDef,
    GetBotChannelAssociationsResponseTypeDef,
    GetBotsResponseTypeDef,
    GetBotVersionsResponseTypeDef,
    GetBuiltinIntentsResponseTypeDef,
    GetBuiltinSlotTypesResponseTypeDef,
    GetIntentsResponseTypeDef,
    GetIntentVersionsResponseTypeDef,
    GetSlotTypesResponseTypeDef,
    GetSlotTypeVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "GetBotAliasesPaginator",
    "GetBotChannelAssociationsPaginator",
    "GetBotVersionsPaginator",
    "GetBotsPaginator",
    "GetBuiltinIntentsPaginator",
    "GetBuiltinSlotTypesPaginator",
    "GetIntentVersionsPaginator",
    "GetIntentsPaginator",
    "GetSlotTypeVersionsPaginator",
    "GetSlotTypesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetBotAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotaliasespaginator)
    """

    def paginate(
        self,
        *,
        botName: str,
        nameContains: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBotAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotaliasespaginator)
        """

class GetBotChannelAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotChannelAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotchannelassociationspaginator)
    """

    def paginate(
        self,
        *,
        botName: str,
        botAlias: str,
        nameContains: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBotChannelAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotChannelAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotchannelassociationspaginator)
        """

class GetBotVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBotVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotversionspaginator)
        """

class GetBotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotspaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotspaginator)
        """

class GetBuiltinIntentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinIntents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinintentspaginator)
    """

    def paginate(
        self,
        *,
        locale: LocaleType = ...,
        signatureContains: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBuiltinIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinIntents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinintentspaginator)
        """

class GetBuiltinSlotTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinslottypespaginator)
    """

    def paginate(
        self,
        *,
        locale: LocaleType = ...,
        signatureContains: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBuiltinSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinslottypespaginator)
        """

class GetIntentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetIntentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentversionspaginator)
        """

class GetIntentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentspaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentspaginator)
        """

class GetSlotTypeVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypeVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypeversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetSlotTypeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypeVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypeversionspaginator)
        """

class GetSlotTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypespaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypespaginator)
        """
