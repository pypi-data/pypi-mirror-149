# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict

import click

from lean.components.util.logger import Logger
from lean.constants import BINANCE_PRODUCT_ID
from lean.container import container
from lean.models.brokerages.local.base import LocalBrokerage
from lean.models.config import LeanConfigConfigurer
from lean.models.logger import Option


class BinanceBrokerage(LocalBrokerage):
    """A LocalBrokerage implementation for the Binance brokerage."""
    _is_module_installed = False

    def __init__(self, organization_id: str, api_key: str, api_secret: str, testnet: bool) -> None:
        self._organization_id = organization_id
        self._api_key = api_key
        self._api_secret = api_secret
        self._testnet = testnet

    @classmethod
    def get_name(cls) -> str:
        return "Binance"

    @classmethod
    def _build(cls, lean_config: Dict[str, Any], logger: Logger) -> LocalBrokerage:
        api_client = container.api_client()

        organizations = api_client.organizations.get_all()
        options = [Option(id=organization.id, label=organization.name) for organization in organizations]

        organization_id = logger.prompt_list(
            "Select the organization with the {} module subscription".format(cls.get_name()),
            options
        )

        logger.info("""
Create an API key by logging in and accessing the Binance API Management page (https://www.binance.com/en/my/settings/api-management).
        """.strip())

        api_key = click.prompt("API key", cls._get_default(lean_config, "binance-api-key"))
        api_secret = logger.prompt_password("API secret", cls._get_default(lean_config, "binance-api-secret"))
        testnet = click.confirm("Use the testnet?")

        return BinanceBrokerage(organization_id, api_key, api_secret, testnet)

    def _configure_environment(self, lean_config: Dict[str, Any], environment_name: str) -> None:
        self.ensure_module_installed()

        lean_config["environments"][environment_name]["live-mode-brokerage"] = "BinanceBrokerage"
        lean_config["environments"][environment_name]["transaction-handler"] = \
            "QuantConnect.Lean.Engine.TransactionHandlers.BrokerageTransactionHandler"

    def configure_credentials(self, lean_config: Dict[str, Any]) -> None:
        lean_config["binance-api-key"] = self._api_key
        lean_config["binance-api-secret"] = self._api_secret
        lean_config["binance-use-testnet"] = self._testnet

        if self._testnet:
            lean_config["binance-api-url"] = "https://testnet.binance.vision"
            lean_config["binance-websocket-url"] = "wss://testnet.binance.vision/ws"
        else:
            lean_config["binance-api-url"] = "https://api.binance.com"
            lean_config["binance-websocket-url"] = "wss://stream.binance.com:9443/ws"

        lean_config["job-organization-id"] = self._organization_id
        self._save_properties(lean_config, ["job-organization-id", "binance-api-key", "binance-api-secret", "binance-use-testnet"])

    def ensure_module_installed(self) -> None:
        if not self._is_module_installed:
            container.module_manager().install_module(BINANCE_PRODUCT_ID, self._organization_id)
            self._is_module_installed = True

class BinanceDataFeed(LeanConfigConfigurer):
    """A LeanConfigConfigurer implementation for the Binance data feed."""

    def __init__(self, brokerage: BinanceBrokerage) -> None:
        self._brokerage = brokerage

    @classmethod
    def get_name(cls) -> str:
        return BinanceBrokerage.get_name()

    @classmethod
    def build(cls, lean_config: Dict[str, Any], logger: Logger) -> LeanConfigConfigurer:
        return BinanceDataFeed(BinanceBrokerage.build(lean_config, logger))

    def configure(self, lean_config: Dict[str, Any], environment_name: str) -> None:
        self._brokerage.ensure_module_installed()

        lean_config["environments"][environment_name]["data-queue-handler"] = "BinanceBrokerage"
        lean_config["environments"][environment_name]["history-provider"] = "BrokerageHistoryProvider"

        self._brokerage.configure_credentials(lean_config)
