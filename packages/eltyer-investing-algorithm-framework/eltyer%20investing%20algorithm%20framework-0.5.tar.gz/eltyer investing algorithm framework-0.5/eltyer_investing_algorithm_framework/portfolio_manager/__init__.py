import logging
from typing import List
from datetime import datetime

from investing_algorithm_framework import PortfolioManager, Position, Order
from eltyer_investing_algorithm_framework.configuration import constants
from eltyer import Client

logger = logging.getLogger(__name__)


class EltyerPortfolioManager(PortfolioManager):
    identifier = "ELTYER"
    market = "ELTYER"
    client: Client = None

    def initialize(self, algorithm_context):
        self.client = algorithm_context.config.get(constants.ELTYER_CLIENT)
        portfolio = self.client.get_portfolio()
        self.market = portfolio.broker
        self.trading_symbol = portfolio.trading_symbol
        super(EltyerPortfolioManager, self).initialize(algorithm_context)

    def get_positions(
        self, algorithm_context=None, **kwargs
    ) -> List[Position]:
        positions_data = self.client.get_positions(json=True)
        positions = []

        for position_data in positions_data:
            positions.append(Position.from_dict(position_data))

        return positions

    def get_orders(
        self,
        symbol=None,
        since: datetime=None,
        algorithm_context=None,
        **kwargs
    ) -> List[Order]:
        orders_data = self.client.get_orders(json=True)
        orders = []

        for order_data in orders_data:
            orders.append(Order.from_dict(order_data))

        return orders
