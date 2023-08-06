"""Fairdesk REST api
"""
import time
import hmac
import hashlib
import json
import requests


class Fairdesk:
    """Fairdesk
    """
    BASE_ENDPOINT = "https://api.fairdesk.com"

    def __init__(self, api_key: str="", api_secret: str=""):
        """initializer

        Args:
            api_key (str, optional): api key (ID). Defaults to "".
            api_secret (str, optional): api secret. Defaults to "".
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def load_markets(self) -> dict:
        """load markets

        Returns:
            dict: status, error, data
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/products"
        resp = requests.get(url)
        return resp.json()

    def fetch_order_book(self, symbol: str) -> dict:
        """fetch order book

        Args:
            symbol (str): btcusdt

        Returns:
            dict: _description_
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/md/orderbook"
        params = {"symbol": symbol}
        resp = requests.get(url, params=params)
        return resp.json()

    def fetch_recent_trade(self, symbol: str) -> dict:
        """fetch recent trade

        Args:
            symbol (str): btcusdt

        Returns:
            dict: _description_
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/md/trade-recent"
        params = {"symbol": symbol}
        resp = requests.get(url, params=params)
        return resp.json()

    def fetch_trade_history(self, symbol: str, fromts: int, limit:int=500):
        """fetch trade history

        Args:
            symbol (str): _description_
            fromts (int): _description_
            limit (_type_, optional): _description_. Defaults to int.

        Returns:
            _type_: _description_
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/md/trade-history"
        params = {
            "symbol": symbol,
            "from": fromts,
            "limit": limit
        }
        resp = requests.get(url, params=params)
        return resp.json()

    def fetch_ticker(self, symbol: str):
        """fetch 24h ticker

        Args:
            symbol (str): ticker (btcusdt)

        Returns:
            _type_: _description_
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/md/ticker24h"
        params = {"symbol": symbol}
        resp = requests.get(url, params=params)
        return resp.json()

    def fetch_ohlcv(self, symbol: str, interval: str, from_ts: int, to_ts: int, limit: int=500):
        """_summary_

        Args:
            symbol (str): _description_
            interval (str): _description_
            from_ts (int): _description_
            to_ts (int): _description_
            limit (int, optional): _description_. Defaults to 500.

        Returns:
            _type_: _description_
        """
        url = self.BASE_ENDPOINT + "/api/v1/public/md/kline"
        params = {
            "symbol": symbol,
            "interval": interval,
            "from": from_ts,
            "to": to_ts,
            "limit": limit
        }
        resp = requests.get(url, params=params)
        return resp.json()

    def _generate_signature(self, url_path, query_string, body: dict, expiry):
        if len(body) != 0:
            message = url_path + query_string + str(expiry) + json.dumps(body)
        else:
            message = url_path + query_string + str(expiry)

        return  hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256).hexdigest()

    def _put_request(self, url_path:str, body:dict):
        expiry = int(time.time() * 1000000 + 60 * 1000000)
        signatue = self._generate_signature(url_path, "", body, expiry)

        headers = {
            "x-fairdesk-access-key": self.api_key,
            "x-fairdesk-request-expiry": str(expiry),
            "x-fairdesk-request-signature": signatue
        }

        url = self.BASE_ENDPOINT + url_path
        resp = requests.put(url=url, headers=headers, json=body)
        return resp.json()

    def _post_request(self, url_path:str, body:dict):
        expiry = int(time.time() * 1000000 + 60 * 1000000)
        signatue = self._generate_signature(url_path, "", body, expiry)

        headers = {
            "x-fairdesk-access-key": self.api_key,
            "x-fairdesk-request-expiry": str(expiry),
            "x-fairdesk-request-signature": signatue
        }

        url = self.BASE_ENDPOINT + url_path
        if len(body) == 0:
            resp = requests.post(url=url, headers=headers)
        else:
            resp = requests.post(url=url, headers=headers, json=body)
        return resp.json()

    def _get_request(self, url_path: str, params: str=""):
        expiry = int(time.time() * 1000000 + 60 * 1000000)
        signatue = self._generate_signature(url_path, params, body={}, expiry=expiry)

        headers = {
            "x-fairdesk-access-key": self.api_key,
            "x-fairdesk-request-expiry": str(expiry),
            "x-fairdesk-request-signature": signatue
        }

        url = self.BASE_ENDPOINT + url_path
        resp = requests.get(url=url, headers=headers, params=params)
        return resp.json()

    def fetch_positions(self) -> dict:
        """query current furture positions

        Returns:
            dict : _description_
        """
        return self._get_request("/api/v1/private/account/positions")

    def fetch_open_orders(self) -> dict:
        """fetch open orders

        Returns:
            dict: _description_
        """
        return self._get_request("/api/v1/private/trade/open-orders")

    def fetch_balance(self) -> dict:
        """fetch balance

        Returns:
            dict: balance
        """
        return self._get_request("/api/v1/private/account/balance")

    def _create_order(self, symbol: str, side: str, position: str,
                      isolated: bool, amount: float, price: float,
                      order_type: str, time_in_force: str="GTC") -> dict:
        data = {
            "symbol": symbol,
            "side": side,
            "positionSide": position,
            "isolated": str(isolated).lower(),
            "quantity": str(amount),
            'type': order_type
        }

        # limit only
        if order_type == "LIMIT":
            data['price'] = str(price)
            data['timeInForce'] = time_in_force

        return self._post_request("/api/v1/private/trade/place-order", data)

    def create_market_order(self, symbol: str, side: str, amount: float, params = None):
        """create market order

        Args:
            symbol (str): symbol
            side (str): "buy" or "sell"
            amount (float): amount
            params (dict): parameters

        Returns:
            _type_: _description_
        """
        if isinstance(params, dict):
            reduce_only = params.get('reduce_only', False)
        else:
            reduce_only = False

        if reduce_only is True:
            if side == "buy":
                position = "SHORT"
            else:
                position = "LONG"
        else:
            if side == "buy":
                position = "LONG"
            else:
                position = "SHORT"

        return self._create_order(
            symbol,
            side.upper(),
            position,
            True,
            amount,
            0.0,
            "MARKET"
        )

    def create_limit_order(self, symbol: str, side: str, amount: float,
                           price: float, params = None):
        """create market order

        Args:
            symbol (str): symbol
            side (str): "buy" or "sell"
            amount (float): amount
            price (float): price
            params (dict): parameters

        Returns:
            _type_: _description_
        """
        if isinstance(params, dict):
            reduce_only = params.get('reduce_only', False)
        else:
            reduce_only = False

        if reduce_only is True:
            if side == "buy":
                position = "SHORT"
            else:
                position = "LONG"
        else:
            if side == "buy":
                position = "LONG"
            else:
                position = "SHORT"

        # time in force
        if isinstance(params, dict):
            time_in_force = params.get('time_in_force', "GTC")
        else:
            time_in_force = False

        return self._create_order(
            symbol,
            side.upper(),
            position,
            True,
            amount,
            price,
            "LIMIT",
            time_in_force
        )

    def cancel_all_orders(self, symbol: str="btcusdt") -> dict:
        """cancel all orders

        Returns:
            dict: _description_
        """
        data = {
            "symbol": symbol,
            "settleCcy": "USDT"
        }
        return self._post_request("/api/v1/private/trade/cancel-all-order", data)

    def cancel_order(self, symbol: str, order_id: str) -> dict:
        """cancel single order by order_id

        Args:
            symbol (str): symbol (btcusdt)
            order_id (str): order id to cancel

        Returns:
            dict: basic output format
        """
        data = {
            "symbol": symbol,
            "orderId": order_id
        }
        return self._post_request("/api/v1/private/trade/cancel-order", body=data)

    def fetch_symbol_config(self) -> dict:
        """fetch symbol config

        Returns:
            dict: _description_
        """
        return self._get_request("/api/v1/private/account/symbol-config")

    def adjust_leverage(self, symbol: str, isolated: bool, leverage: int) -> dict:
        """adjust leverage

        Args:
            symbol (str): _description_
            isolated (bool): _description_
            leverage (int): _description_

        Returns:
            dict: _description_
        """
        data = {
            "symbol": symbol,
            "leverage": str(leverage),
            "isolated": isolated
        }
        return self._put_request("/api/v1/private/account/config/adjust-leverage", data)

    def create_websocket_token(self) -> dict:
        """create websocket token

        Returns:
            dict: token
        """
        return self._post_request("/api/v1/private/token/create", body={})

    def refresh_websocket_token(self) -> dict:
        """refresh websocket token

        Returns:
            dict: token
        """
        return self._post_request("/api/v1/private/token/refresh", body={})

    def delete_websocket_token(self) -> dict:
        """delete websocket token

        Returns:
            dict: token
        """
        return self._post_request("/api/v1/private/token/delete", body={})

if __name__ == "__main__":
    import pprint

    with open("../fairdesk.key", "r", encoding="utf-8") as f:
        lines = f.readlines()
        key = lines[0].strip()
        secret = lines[1].strip()

    exchange = Fairdesk(key, secret)
    pprint.pprint(exchange.create_websocket_token())
    #resp = exchange.adjust_leverage(symbol="btcusdt", isolated=True, leverage=2)
    #pprint.pprint(resp)
    #resp = exchange.create_limit_buy_order("btcusdt", "long", True, 0.001, 40000)
    #pprint.pprint(resp)
