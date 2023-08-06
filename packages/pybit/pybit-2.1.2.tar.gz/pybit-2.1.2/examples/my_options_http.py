from pybit import usdc_options
import logging
logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

api_key = "2PDV5PHWAT1BUpnYoQ"
api_secret = "YsXAGWQauSnfDqsKZdQAO2lFTy7OL4SH6bB4"

session = usdc_options.HTTP(
    endpoint='https://api-testnet.bybit.com',
    api_key=api_key,
    api_secret=api_secret
)

print(session.orderbook())
