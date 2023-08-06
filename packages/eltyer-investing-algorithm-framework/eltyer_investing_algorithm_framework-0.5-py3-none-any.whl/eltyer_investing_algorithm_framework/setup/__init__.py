from investing_algorithm_framework import App
from eltyer_investing_algorithm_framework.exceptions \
    import EltyerInvestingAlgorithmFrameworkException
from eltyer_investing_algorithm_framework.configuration import constants
from eltyer_investing_algorithm_framework.initializer import EltyerInitializer
from eltyer_investing_algorithm_framework.order_executor import \
    EltyerOrderExecutor
from eltyer_investing_algorithm_framework.portfolio_manager import \
    EltyerPortfolioManager


def create_app(resource_directory, config={}, key=None):

    if key is None:
        raise EltyerInvestingAlgorithmFrameworkException(
            "Algorithm api key not provided"
        )

    config[constants.ELTYER_API_KEY] = key
    app = App(resource_directory=resource_directory, config=config)
    app.add_initializer(EltyerInitializer)
    app.add_order_executor(EltyerOrderExecutor)
    app.add_portfolio_manager(EltyerPortfolioManager)
    return app
