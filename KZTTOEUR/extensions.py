import requests
import json
from config import access_key


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        url = f'https://openexchangerates.org/api/latest.json?app_id={access_key}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException('API unavailable')

        try:
            data = json.loads(response.text)
            base_rate = data['rates'][base.upper()]
            quote_rate = data['rates'][quote.upper()]
            total = round((quote_rate / base_rate) * float(amount), 2)
        except (KeyError, ValueError):
            raise APIException('Error getting price data')

        return total
