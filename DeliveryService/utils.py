
import logging
from decimal import Decimal

import requests

from DeliveryService.decorators import retry


logger = logging.getLogger("main")

@retry(attempts=3)
def usd_to_rub_exchange_rate() -> Decimal:
    """Return USD to RUB exchange rate."""
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    exchange_rate = response.json()["Valute"]["USD"]["Value"]
    logger.info(f"Exchange rate getted. 1 USD = {exchange_rate} RUB")
    return Decimal(str(exchange_rate))

    
