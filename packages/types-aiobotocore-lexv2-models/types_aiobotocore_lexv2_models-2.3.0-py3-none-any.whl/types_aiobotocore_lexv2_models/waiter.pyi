"""
Type annotations for lexv2-models service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lexv2_models.client import LexModelsV2Client
    from types_aiobotocore_lexv2_models.waiter import (
        BotAliasAvailableWaiter,
        BotAvailableWaiter,
        BotExportCompletedWaiter,
        BotImportCompletedWaiter,
        BotLocaleBuiltWaiter,
        BotLocaleCreatedWaiter,
        BotLocaleExpressTestingAvailableWaiter,
        BotVersionAvailableWaiter,
    )

    session = get_session()
    async with session.create_client("lexv2-models") as client:
        client: LexModelsV2Client

        bot_alias_available_waiter: BotAliasAvailableWaiter = client.get_waiter("bot_alias_available")
        bot_available_waiter: BotAvailableWaiter = client.get_waiter("bot_available")
        bot_export_completed_waiter: BotExportCompletedWaiter = client.get_waiter("bot_export_completed")
        bot_import_completed_waiter: BotImportCompletedWaiter = client.get_waiter("bot_import_completed")
        bot_locale_built_waiter: BotLocaleBuiltWaiter = client.get_waiter("bot_locale_built")
        bot_locale_created_waiter: BotLocaleCreatedWaiter = client.get_waiter("bot_locale_created")
        bot_locale_express_testing_available_waiter: BotLocaleExpressTestingAvailableWaiter = client.get_waiter("bot_locale_express_testing_available")
        bot_version_available_waiter: BotVersionAvailableWaiter = client.get_waiter("bot_version_available")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "BotAliasAvailableWaiter",
    "BotAvailableWaiter",
    "BotExportCompletedWaiter",
    "BotImportCompletedWaiter",
    "BotLocaleBuiltWaiter",
    "BotLocaleCreatedWaiter",
    "BotLocaleExpressTestingAvailableWaiter",
    "BotVersionAvailableWaiter",
)

class BotAliasAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAliasAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botaliasavailablewaiter)
    """

    async def wait(
        self, *, botAliasId: str, botId: str, WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAliasAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botaliasavailablewaiter)
        """

class BotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botavailablewaiter)
    """

    async def wait(self, *, botId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botavailablewaiter)
        """

class BotExportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotExportCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botexportcompletedwaiter)
    """

    async def wait(self, *, exportId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotExportCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botexportcompletedwaiter)
        """

class BotImportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotImportCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botimportcompletedwaiter)
    """

    async def wait(self, *, importId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotImportCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botimportcompletedwaiter)
        """

class BotLocaleBuiltWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleBuilt)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalebuiltwaiter)
    """

    async def wait(
        self,
        *,
        botId: str,
        botVersion: str,
        localeId: str,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleBuilt.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalebuiltwaiter)
        """

class BotLocaleCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalecreatedwaiter)
    """

    async def wait(
        self,
        *,
        botId: str,
        botVersion: str,
        localeId: str,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalecreatedwaiter)
        """

class BotLocaleExpressTestingAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
    """

    async def wait(
        self,
        *,
        botId: str,
        botVersion: str,
        localeId: str,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
        """

class BotVersionAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotVersionAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botversionavailablewaiter)
    """

    async def wait(
        self, *, botId: str, botVersion: str, WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models.html#LexModelsV2.Waiter.BotVersionAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botversionavailablewaiter)
        """
