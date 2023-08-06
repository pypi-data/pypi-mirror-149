# ELTYER Investing Algorithm Framework Plugin
This is the official plugin for the [investing algorithm framework](https://investing-algorithm-framework.com) open source project.

## Installation
You can install the plugin with pip.
```shell
pip install eltyer-investing-algorithm-framework
```

## Usage 
Example trading bot using binance data using the eltyer components.
```python
import os

from investing_algorithm_framework import AlgorithmContext
from eltyer_investing_algorithm_framework.setup import create_app

dir_path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

app = create_app(
    resource_directory=dir_path, key="<YOUR_ELTYER_TRADING_BOT_API_KEY>"
)


@app.algorithm.strategy(
    time_unit="SECOND",
    interval=5,
    data_provider_identifier="BINANCE",
    target_symbol="BTC",
    trading_data_type="TICKER",
)
def perform_strategy(context: AlgorithmContext, ticker):
    print("Running my strategy")

    
if __name__ == "__main__":
    app.start()
```

## Documentation
You can find the official documentation at our [documentation website](https://docs.eltyer.com/python-client/introduction)