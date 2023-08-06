import logging

from investing_algorithm_framework import OrderExecutor, Order, OrderStatus, \
    OrderType
from investing_algorithm_framework.core import OperationalException
from eltyer import Client, ClientException
from eltyer_investing_algorithm_framework.configuration import constants

logger = logging.getLogger(__name__)


class EltyerOrderExecutor(OrderExecutor):
    identifier = "ELTYER"

    def execute_order(
        self, order: Order, algorithm_context, **kwargs
    ) -> Order:
        client: Client = algorithm_context.config[constants.ELTYER_CLIENT]

        if OrderType.LIMIT.equals(order.type):

            try:
                eltyer_order = client.create_limit_order(
                    target_symbol=order.get_target_symbol(),
                    amount=order.get_amount_target_symbol(),
                    side=order.get_side(),
                    price=order.get_initial_price()
                )
                order.set_reference_id(eltyer_order.order_reference)
                order.set_status(OrderStatus.PENDING)
            except ClientException as e:
                logger.error(e)
                raise OperationalException(e)
        else:
            try:
                eltyer_order = client.create_market_order(
                    target_symbol=order.get_target_symbol(),
                    amount=order.get_amount_target_symbol()
                )
                order.set_reference_id(eltyer_order.order_reference)
                order.set_status(OrderStatus.PENDING)
            except ClientException as e:
                logger.exception(e)

        return order

    def check_order_status(
        self, order: Order, algorithm_context, **kwargs
    ) -> Order:
        client: Client = algorithm_context.config[constants.ELTYER_CLIENT]

        try:
            eltyer_order = client.get_order(
                reference_id=order.get_reference_id()
            )
            order.set_status(
                OrderStatus.from_string(eltyer_order.get_status())
            )
        except ClientException as e:
            logger.error(e)
            raise OperationalException(
                "Could not get order status from eltyer"
            )
        return order
