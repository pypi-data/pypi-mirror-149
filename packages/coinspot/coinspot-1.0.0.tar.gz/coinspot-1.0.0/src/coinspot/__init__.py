# Python wrapper for the Coinspot API
# Copyright (C) 2022 Alex Verrico
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from time import time
from hashlib import sha512
import hmac
import json
import requests


class PublicAPIV2:
    API_ENDPOINT = 'https://www.coinspot.com.au:443/pubapi/v2'

    def latest(self, coin: str = None, market_type: str = None) -> dict:
        """
        Get latest coin prices

        :param coin: (optional) Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :return:
        coin=None market_type=None: {"status":"ok", "message":"ok", "prices":{"btc":{"bid":11111, "ask":222222, "last":1111.11}, ...}}
        coin=ABC market_type=None: {"status":"ok", "message":"ok", "prices":{"bid":11111, "ask":222222, "last":1111.11}}
        coin=ABC market_type=XYZ: {"status":"ok", "message":"ok", "prices":{"bid":11111, "ask":222222, "last":1111.11}}
        """
        if not coin:
            return requests.get(self.API_ENDPOINT + '/latest').json()
        if not market_type:
            return requests.get(self.API_ENDPOINT + '/latest/' + coin).json()
        return requests.get(f'{self.API_ENDPOINT}/latest/{coin}/{market_type}').json()

    def buy_price(self, coin: str, market_type: str = None) -> dict:
        """
        Get latest buy price for {coin}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :return:
        coin=ABC market_type=None: {"status":"ok", "message":"ok", "rate":11111, "market": "ABC/AUD"}
        coin=ABC market_type=XYZ: {"status":"ok", "message":"ok", "rate":11111, "market": "ABC/XYZ"}
        """
        if not market_type:
            return requests.get(f'{self.API_ENDPOINT}/buyprice/{coin}').json()
        return requests.get(f'{self.API_ENDPOINT}/buyprice/{coin}/{market_type}').json()

    def sell_price(self, coin: str, market_type: str = None) -> dict:
        """
        Get latest sell price for {coin}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :return:
        coin=ABC market_type=None: {"status":"ok", "message":"ok", "rate":11111, "market": "ABC/AUD"}
        coin=ABC market_type=XYZ: {"status":"ok", "message":"ok", "rate":11111, "market": "ABC/XYZ"}
        """
        if not market_type:
            return requests.get(f'{self.API_ENDPOINT}/sellprice/{coin}').json()
        return requests.get(f'{self.API_ENDPOINT}/sellprice/{coin}/{market_type}').json()

    def open_orders(self, coin: str, market_type: str = None) -> dict:
        """
        List open orders for {coin}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :return:
        coin=ABC market_type=None: {"status":"ok", "message":"ok",
            "buyorders":[{"amount":0.1, "rate":111111, "total":111111, "coin":"ABC", "market":"ABC/AUD"}, ...],
            "sellorders":[{"amount":0.0001, "rate":1111111, "total":1.111, "coin":"ABC", "market":"ABC/AUD"}, ...]}
        coin=ABC market_type=XYZ: {"status":"ok", "message":"ok",
            "buyorders":[{"amount":0.1, "rate":111111, "total":111111, "coin":"ABC", "market":"ABC/XYZ"}, ...],
            "sellorders":[{"amount":0.0001, "rate":1111111, "total":1.111, "coin":"ABC", "market":"ABC/XYZ"}, ...]}
        """
        if not market_type:
            return requests.get(f'{self.API_ENDPOINT}/orders/open/{coin}').json()
        return requests.get(f'{self.API_ENDPOINT}/orders/open/{coin}/{market_type}').json()

    def completed_orders(self, coin: str, market_type: str = None) -> dict:
        """
        List completed orders for {coin}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :return:
        coin=ABC market_type=None: {"status":"ok", "message":"ok",
            "buyorders":[{"amount":0.1, "rate":111111, "total":111111, "coin":"ABC", "solddate":"2020-05-21T13:22:45.000Z", "market":"ABC/AUD"}, ...],
            "sellorders":[{"amount":0.0001, "rate":1111111, "total":1.111, "coin":"ABC", "solddate":"2020-05-21T13:22:45.000Z", "market":"ABC/AUD"}, ...]}
        coin=ABC market_type=XYZ: {"status":"ok", "message":"ok",
            "buyorders":[{"amount":0.1, "rate":111111, "total":111111, "coin":"ABC", "solddate":"2020-05-21T13:22:45.000Z", "market":"ABC/XYZ"}, ...],
            "sellorders":[{"amount":0.0001, "rate":1111111, "total":1.111, "coin":"ABC", "solddate":"2020-05-21T13:22:45.000Z", "market":"ABC/XYZ"}, ...]}
        """
        if not market_type:
            return requests.get(f'{self.API_ENDPOINT}/orders/completed/{coin}').json()
        return requests.get(f'{self.API_ENDPOINT}/orders/completed/{coin}/{market_type}').json()


class FullAccessAPIV2:
    API_ENDPOINT = 'https://www.coinspot.com.au:443/api/v2'

    def __init__(self, api_key: str, api_secret: str):
        """
        Wrapper for the CoinSpot FullAccess API V2

        :param api_key: your CoinSpot FullAccess API Key
        :param api_secret: the Secret associated with the provided API key
        """

        self.api_key = api_key
        self.api_secret = api_secret.encode()
        return

    @staticmethod
    def _chunker(data):
        yield data

    def _request(self, path: str, data: dict = None, nonce: int = None):
        if not data:
            data = {}

        if not nonce:
            data['nonce'] = int(time() * 1000)
        else:
            data['nonce'] = nonce

        json_data = json.dumps(data, separators=(',', ':')).encode()

        try:
            return requests.post(
                self.API_ENDPOINT + path,
                data=self._chunker(json_data),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'coinspot-api/0.0.1',
                    'sign': hmac.new(self.api_secret, json_data, sha512).hexdigest(),
                    'key': self.api_key,
                }
            ).json()
        except:
            return {'status': 'error', 'message': 'API unreachable or timed out'}

    def status(self, nonce: int = None) -> dict:
        """
        Return the status of the CoinSpot API.

        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {'status': 'ok'}
        """

        return self._request('/status', nonce=nonce)

    def coin_deposit_address(self, coin: str, nonce: int = None) -> dict:
        """
        Return the deposit address for {coin}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           'status':'ok',
           'message':'ok',
           'networks': [
                {'name': 'BEP2', 'network': 'BNB', 'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx', 'memo': '123456'},
                {'name': 'ERC20', 'network': 'ETH', 'address': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx', 'memo': ''}
            ]
        }
        """

        return self._request('/my/coin/deposit', data={'cointype': coin}, nonce=nonce)

    def quote_buy_now(self, coin: str, amount: float, amount_type: str, nonce: int = None) -> dict:
        """
        Return a quote to buy {amount} of {coin}.

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount to buy of {coin}
        :param amount_type: "coin" or "aud" - whether {amount} is coin amount or AUD amount
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {'status': 'ok', 'message': 'ok', 'rate': 1234}
        """

        return self._request('/quote/buy/now', data={'cointype': coin, 'amount': amount, 'amountype': amount_type},
                             nonce=nonce)

    def quote_sell_now(self, coin: str, amount: float, amount_type: str, nonce: int = None) -> dict:
        """
        Return a quote to sell {amount} of {coins}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount to buy of {coin}
        :param amount_type: "coin" or "aud" - whether {amount} is coin amount or AUD amount
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {'status': 'ok', 'message': 'ok', 'rate': 1234}
        """
        
        return self._request('/quote/sell/now', data={'cointype': coin, 'amount': amount, 'amountype': amount_type},
                             nonce=nonce)

    def quote_swap_now(self, coin_to_sell: str, coin_to_buy: str, amount: float, nonce: int = None) -> dict:
        """
        Return a quote to swap {amount} of {coin_to_sell} for {coin_to_buy}

        :param coin_to_sell: Coin short name, eg. BTC, ETH, LTC
        :param coin_to_buy: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin_to_sell} to sell
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {'status': 'ok', 'message': 'ok', 'rate': 1234}
        """

        return self._request('/quote/swap/now', data={'cointypesell': coin_to_sell, 'cointypebuy': coin_to_buy, 
                                                      'amount': amount}, nonce=nonce)
    
    def market_buy_order(self, coin: str, amount: float, rate: float, market_type: str = 'AUD',
                         nonce: int = None) -> dict:
        """
        Place a market buy order for {amount} of {coin} at {rate}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin} to buy, max precision 8 decimal places
        :param rate: Rate in market currency (e.g. AUD or USDT) you are willing to pay, max precision 8 decimal places
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "coin":"BTC",
           "market": "BTC/AUD",
           "amount":1.234
           "rate":123.344
           "id":"12345678901234567890"
        }
        """

        return self._request('/my/buy', data={'cointype': coin, 'amount': amount, 'rate': rate,
                                              'markettype': market_type}, nonce=nonce)

    def buy_now_order(self, coin: str, amount: float, amount_type: str, rate: float = None,
                      threshold: float = None, direction: str = 'UP', nonce: int = None) -> dict:
        """
        Place a buy now order for {amount} of {coin}.
        {amount} can be AUD or {coin}, determined by {amount_type}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin} to buy, max precision 8 decimal places
        :param amount_type: "coin" or "aud" - whether {amount} is coin amount or AUD amount
        :param rate: (optional) rate in AUD received from using quote_buy_now or otherwise
        :param threshold: (optional) 0 to 1000 - buy request will terminate if not within percentage threshold for
            current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction: (optional) UP, DOWN, or BOTH - direction the price has moved for the percentage
            threshold to apply
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "coin":"BTC",
           "amount":1.234,
           "market":"BTC/AUD",
           "total": 10.234
        }
        """

        data = {'cointype': coin, 'amounttype': amount_type, 'amount': amount, 'direction': direction}

        if rate:
            data['rate'] = rate
            data['threshold'] = threshold

        return self._request('/my/buy/now', data=data, nonce=nonce)

    def market_sell_order(self, coin: str, amount: float, rate: float, market_type: str = 'AUD',
                          nonce: int = None) -> dict:
        """
        Place a market sell order for {amount} of {coin} at {rate}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin} to sell, max precision 8 decimal places
        :param rate: rate in AUD you are willing to sell for, max precision 8 decimal places
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "coin":"BTC",
           "market": "BTC/AUD",
           "amount":1.234,
           "rate":123.344,
           "id":"12345678901234567890"
        }
        """
        return self._request('/my/sell', data={'cointype': coin, 'amount': amount, 'rate': rate,
                                               'markettype': market_type}, nonce=nonce)

    def sell_now_order(self, coin: str, amount: float, amount_type: str, rate: float = None,
                       threshold: float = None, direction: str = 'DOWN', nonce: int = None) -> dict:
        """
        Place a sell now order for {amount} of {coin}.
        {amount} can be AUD or {coin}, determined by {amount_type}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin} to buy, max precision 8 decimal places
        :param amount_type: "coin" or "aud" - whether {amount} is coin amount or AUD amount
        :param rate: (optional) rate in AUD received from using Sell Now Quote or otherwise
        :param threshold: (optional) 0 to 1000 - sell request will terminate if not within percentage threshold for
            current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction: (optional) UP, DOWN, or BOTH - direction the price has moved for the percentage
        threshold to apply
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
          "status":"ok",
           "message":"ok",
           "coin":"BTC",
           "amount":1.234,
           "rate":3.234,
           "market":"BTC/AUD",
           "total": 10.234
        }
        """
        data = {'cointype': coin, 'amount': amount, 'amounttype': amount_type, 'direction': direction}

        if rate:
            data['rate'] = rate
            data['threshold'] = threshold

        return self._request('/my/sell/now', data=data, nonce=nonce)

    def swap_now_order(self, coin_to_sell: str, coin_to_buy: str, amount: float, rate: float = None,
                       threshold: float = None, direction: str = 'BOTH', nonce: int = None) -> dict:
        """
        Place a swap order to swap {amount} of {coin_to_sell} for {coin_to_buy}

        :param coin_to_sell: Coin short name, eg. BTC, ETH, LTC
        :param coin_to_buy: Coin short name, eg. BTC, ETH, LTC
        :param amount: Amount of {coin_to_sell} to swap
        :param rate: (optional) rate received from using Swap Now Quote or otherwise
        :param threshold: (optional) 0 to 1000 - swap request will terminate if not within percentage threshold for
            current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction: (optional) UP, DOWN, or BOTH - direction the price has moved for the
            percentage threshold to apply
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "coin":"BTC",
           "amount":1.234,
           "rate":3.234,
           "market":"BTC/ETH",
           "total": 10.234
        }
        """
        data = {'cointypesell': coin_to_sell, 'cointypebuy': coin_to_buy, 'amount': amount, 'direction': direction}

        if rate:
            data['rate'] = rate
            data['threshold'] = threshold

        return self._request('/my/swap/now', data=data, nonce=nonce)

    def cancel_buy_order(self, order_id: str, nonce: int = None) -> dict:
        """
        Cancel open Buy Order

        :param order_id: ID of order to cancel
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok"
        }
        """
        return self._request('/my/buy/cancel', data={'id': order_id}, nonce=nonce)

    def cancel_sell_order(self, order_id: str, nonce: int = None) -> dict:
        """
        Cancel open Sell Order

        :param order_id: ID of order to cancel
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok"
        }
        """
        return self._request('/my/sell/cancel', data={'id': order_id}, nonce=nonce)

    def get_coin_withdrawal_details(self, coin: str, nonce: int = None) -> dict:
        """
        Get list of networks that {coin} can be sent over

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "networks": [
            { "network": "BNB", "paymentid": "no", "fee": 0.001, "minsend": 0.00001, default: false},
            { "network": "BSC", "paymentid": "optional", "fee": 0.002, "minsend": 0.00001, default: false},
            { "network": "ETH", "paymentid": "no", "fee":0.003, "minsend": 0.00001, default: true},
            ]

        }

        """
        return self._request('/my/coin/withdraw/senddetails', data={'cointype': coin}, nonce=nonce)

    def coin_withdrawal(self, coin: str, amount: float, address: str, require_email_confirmation: str = 'NO',
                        network: str = None, payment_id: str = None, nonce: int = None) -> dict:
        """
        Transfer {amount} of {coin} to {address} using {network}

        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param amount: the amount (in coin currency) of coin you would like to transfer
        :param address: the destination address for the coin amount
        :param require_email_confirmation: (optional) if 'YES' an email confirmation will be sent and
            withdraw will not complete until confirmation link within email is clicked, values: 'YES', 'NO'
        :param network: (optional) - network you would like to send using e.g. 'BNB', 'ETH' - None for 'default' network
        :param payment_id: (optional) - the appropriate payment id/memo for the withdrawal where permitted
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok"
        }
        """
        data = {'cointype': coin, 'amount': amount, 'address': address, 'emailconfirm': require_email_confirmation}

        if network:
            data['network'] = network

        if payment_id:
            data['paymentid'] = payment_id

        return self._request('/my/coin/withdraw/send', data=data, nonce=nonce)


class ReadOnlyAPIV2:
    API_ENDPOINT = 'https://www.coinspot.com.au:443/api/v2/ro'

    def __init__(self, api_key: str, api_secret: str):
        """
        Wrapper for the CoinSpot ReadOnly API V2

        :param api_key: is your CoinSpot ReadOnly API Key
        :param api_secret: is the Secret associated with the provided API key
        """

        self.api_key = api_key
        self.api_secret = api_secret.encode()
        return

    @staticmethod
    def _chunker(data):
        yield data

    def _request(self, path: str, data: dict = None, nonce: int = None):
        if not data:
            data = {}

        if not nonce:
            data['nonce'] = int(time() * 1000)
        else:
            data['nonce'] = nonce

        json_data = json.dumps(data, separators=(',', ':')).encode()

        try:
            return requests.post(
                self.API_ENDPOINT + path,
                data=self._chunker(json_data),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'coinspot-api/0.0.1',
                    'sign': hmac.new(self.api_secret, json_data, sha512).hexdigest(),
                    'key': self.api_key,
                }
            ).json()
        except:
            return {'status': 'error', 'message': 'API unreachable or timed out'}

    def status(self, nonce: int = None) -> dict:
        """
        Return the status of the CoinSpot API.

        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {"status":"ok"}
        """

        return self._request('/status', nonce=nonce)

    def public_open_market_orders(self, coin: str, market_type: str = None, nonce: int = None) -> dict:
        """
        Return a list of the top 20 public open buy and sell market orders
        
        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "amount":0.0001,
                 "rate":111111,
                 "total":0.1,
                 "coin":"BTC",
                 "market": "BTC/AUD"
              },
              {
                 "amount":0.001,
                 "rate":11111111,
                 "total":0.01,
                 "coin":"BTC",
                 "market": "BTC/AUD"
              }
           ],
           "sellorders":[
              {
                 "amount":0.0001,
                 "rate":111111,
                 "total":1,
                 "coin":"BTC",
                 "market": "BTC/AUD"
              },
              {
                 "amount":0.0001855,
                 "rate":11111,
                 "total":2,
                 "coin":"BTC",
                 "market": "BTC/AUD"
              }
           ]
        }
        """

        data = {'cointype': coin}
        if market_type:
            data['markettype'] = market_type

        return self._request('/orders/market/open', data=data, nonce=nonce)

    def public_completed_market_orders(self, coin: str, market_type: str = None, start_date: str = None,
                                       end_date: str = None, limit: int = 200, nonce: int = None) -> dict:
        """
        Return a list of public completed buy and sell market orders
        
        :param coin: Coin short name, eg. BTC, ETH, LTC
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param limit: (optional) max 500 records
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "amount":0.0001,
                 "rate":111111,
                 "total":0.1,
                 "coin":"BTC",
                 "market": "BTC/AUD",
                 "solddate":"2020-05-21T13:22:45.000Z"
              },
              {
                 "amount":0.001,
                 "rate":11111111,
                 "total":0.01,
                 "coin":"BTC",
                 "market": "BTC/USDT",
                 "solddate":"2020-05-21T13:22:45.000Z"
              }
           ],
           "sellorders":[
              {
                 "amount":0.0001,
                 "rate":111111,
                 "total":1,
                 "coin":"BTC",
                 "market": "BTC/AUD",
                 "solddate":"2020-05-21T13:22:45.000Z"
              },
              {
                 "amount":0.0001855,
                 "rate":11111,
                 "total":2,
                 "coin":"BTC",
                 "market": "BTC/USDT",
                 "solddate":"2020-05-21T13:22:45.000Z"
              }
           ]
        }
        """
        data = {'cointype': coin, 'limit': limit}
        if market_type:
            data['markettype'] = market_type
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date
        
        return self._request('/orders/market/completed', data=data, nonce=nonce)

    def wallet_balance(self, coin: str = None, nonce: int = None) -> dict:
        """
        Return the balance of the specified wallet, or all non-empty wallets
        
        :param coin: Optional coin short name, eg. BTC, ETH, LTC.
            If None, returns a list of balances for all of your wallets
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "balances":[
              {
                 "AUD":{
                    "balance":1000.11,
                    "audbalance":1000.11,
                    "rate":1
                 }
              },
              {
                 "BTC":{
                    "balance":1.1111111,
                    "audbalance":2222.22,
                    "rate":111111.11
                 }
              },
              {
                 "LTC":{
                    "balance":111.111111,
                    "audbalance":22222.22,
                    "rate":11.1111
                 }
              }]
        }
        """

        if coin:
            return self._request(f'/my/balance/{coin}', nonce=nonce)
        else:
            return self._request('/my/balances', nonce=nonce)
    
    def open_market_orders(self, coin: str = None, market_type: str = None, nonce: int = None) -> dict:
        """
        Return a list of your open market orders
        
        :param coin: (optional) coin short name, eg. BTC, ETH, LTC.
            if None, returns open market orders for all coins
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
            if None, returns open market orders for all markets
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin":"STRAT",
                 "market":"STRAT/AUD",
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "rate":45.11111,
                 "total":444444
              },
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin":"STRAT",
                 "market":"STRAT/USDT",
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "rate":45.11111,
                 "total":444444
              }]
           "sellorders":[
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin":"STRAT",
                 "market":"STRAT/AUD",
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "rate":45.11111,
                 "total":444444
              },
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin":"STRAT",
                 "market":"STRAT/USDT",
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "rate":45.11111,
                 "total":444444
              }}
           ]
        }
        """
        if coin or market_type:
            data = {}
            if coin:
                data['cointype'] = coin
            if market_type:
                data['markettype'] = market_type
            return self._request('/my/orders/market/open', data=data, nonce=nonce)
        else:
            return self._request('/my/orders/market/open', nonce=nonce)

    def open_limit_orders(self, coin: str = None, nonce: int = None) -> dict:
        """
        Return a list of your open limit orders

        :param coin: (optional) coin short name, eg. BTC, ETH, LTC.
            if None, returns open limit orders for all coins
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin": "STRAT",
                 "market":"STRAT/AUD",
                 "rate": 111.111
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "type": "buy stop"
              },
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin": "STRAT",
                 "market":"STRAT/AUD",
                 "rate": 111.111
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "type": "buy limit"
              }]
           "sellorders":[
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin": "STRAT",
                 "market":"STRAT/AUD",
                 "rate": 111.111
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "type": "stop loss"
              },
              {
                 "id": "1f1f1f1f1d1d1d1d1d1d1d1d",
                 "coin": "STRAT",
                 "market":"STRAT/AUD",
                 "rate": 111.111
                 "amount":111.1111,
                 "created":"2020-05-21T13:22:45.000Z",
                 "type": "take profit"
              }}
           ]
        }
        """
        data = {}
        if coin:
            data['cointype'] = coin
        return self._request('/my/orders/limit/open', data=data, nonce=nonce)

    def order_history(self, coin: str = None, market_type: str = None, start_date: str = None,
                      end_date: str = None, limit: int = 200, nonce: int = None) -> dict:
        """
        Return a list of your past orders
        
        :param coin: (optional) coin short name, eg. BTC, ETH, LTC.
            if None, returns past orders for all coins
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
            if None, returns past orders for all markets
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param limit: (optional) max 500 records
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "coin":"STRAT",
                 "type":"market",
                 "market":"STRAT/AUD",
                 "rate":1222.33,
                 "amount":111.1111,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":45.11111,
                 "audGst":40.11111,
                 "audtotal":444444
              },
              {
                 "coin":"STRAT",
                 "type":"instant",
                 "otc":false,
                 "market":"OMG/AUD",
                 "rate":1222.33,
                 "amount":333.33333,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":44.444444,
                 "audGst":4.444444,
                 "audtotal":5000
              }]
           "sellorders":[
             {
                 "coin":"STRAT",
                 "type":"market",
                 "market":"STRAT/AUD",
                 "rate":1222.33,
                 "amount":111.1111,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":45.11111,
                 "audGst":40.11111,
                 "audtotal":444444
              },
              {
                 "coin":"STRAT",
                 "type":"instant",
                 "otc":false,
                 "market":"OMG/AUD",
                 "rate":1222.33,
                 "amount":333.33333,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":44.444444,
                 "audGst":4.444444,
                 "audtotal":5000
              }]
           ]
        }
        """

        data = {'limit': limit}

        if coin:
            data['cointype'] = coin
        if market_type:
            data['markettype'] = market_type
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date

        return self._request('/my/orders/completed', data=data, nonce=nonce)

    def market_order_history(self, coin: str = None, market_type: str = None, start_date: str = None,
                             end_date: str = None, limit: int = 200, nonce: int = None) -> dict:
        """
        Return a list of your past market orders
        
        :param coin: (optional) coin short name, eg. BTC, ETH, LTC.
            if None, returns past market orders for all coins
        :param market_type: (optional, available markets only, default 'AUD') market coin short name, example values 'AUD', 'USDT'
            if None, returns open market orders for all markets
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param limit: (optional) max 500 records
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "buyorders":[
              {
                 "coin":"STRAT",
                 "market":"STRAT/AUD",
                 "rate":1222.33,
                 "amount":111.1111,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":45.11111,
                 "audGst":40.11111,
                 "audtotal":444444
              },
              {
                 "coin":"STRAT",
                 "market":"OMG/AUD",
                 "rate":1222.33,
                 "amount":333.33333,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":44.444444,
                 "audGst":4.444444,
                 "audtotal":5000
              }]
           "sellorders":[
             {
                 "coin":"STRAT",
                 "market":"STRAT/AUD",
                 "rate":1222.33,
                 "amount":111.1111,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":45.11111,
                 "audGst":40.11111,
                 "audtotal":444444
              },
              {
                 "coin":"STRAT",
                 "market":"OMG/AUD",
                 "rate":1222.33,
                 "amount":333.33333,
                 "total":222.2222,
                 "solddate":"2020-05-21T13:22:45.000Z",
                 "audfeeExGst":44.444444,
                 "audGst":4.444444,
                 "audtotal":5000
              }]
           ]
        }
        """

        data = {'limit': limit}
        if coin:
            data['cointype'] = coin
        if market_type:
            data['markettype'] = market_type
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date

        return self._request('/my/orders/market/completed', data=data, nonce=nonce)

    def send_receive_history(self, start_date: str = None, end_date: str = None,
                             nonce: int = None) -> dict:
        """
        Return a list of your past send/receive transactions
        
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "sendtransactions":[
              {
                 "timestamp":"2020-05-21T13:22:45.000Z",
                 "amount":1.111,
                 "coin":"ETH",
                 "address":"12345678901234567890",
                 "aud": 0.123
              },
              {
                 "timestamp":"2020-05-21T13:22:45.000Z",
                 "amount":1111.11111,
                 "coin":"RDD",
                 "address":"12345678901234567890",
                 "aud": 0.123
              }
           ],
           "receivetransactions":[
           {
                 "timestamp":"2020-05-21T13:22:45.000Z",
                 "amount":1.111,
                 "coin":"ETH",
                 "address":"12345678901234567890",
                 "aud": 0.123
              },
              {
                 "timestamp":"2020-05-21T13:22:45.000Z",
                 "amount":1111.11111,
                 "coin":"RDD",
                 "address":"12345678901234567890",
                 "aud": 0.123
              }
           ]
        }
        """
        
        data = {}
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date
        
        return self._request('/my/sendreceive', data=data, nonce=nonce)
    
    def deposit_history(self, start_date: str = None, end_date: str = None, nonce: int = None) -> dict:
        """
        Return a list of your past deposits
        
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
            "status":"ok",
           "message":"ok",
           "deposits":[
              {
                 "amount":1111,
                 "created":""2020-05-21T13:22:45.000Z",
                 "status":"completed",
                 "type":"POLi",
                 "reference":"12345678901234567890"
              },
              {
                 "amount":2000,
                 "created":"2020-05-21T13:22:45.000Z",
                 "status":"completed",
                 "type":"POLi",
                 "reference":"12345678901234567890"
              }
           ]
        }

        """

        data = {}
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date

        return self._request('/my/deposits', data=data, nonce=nonce)
    
    def withdrawal_history(self, start_date: str = None, end_date: str = None,
                           nonce: int = None) -> dict:
        """
        Return a list of your past withdrawals
        
        :param start_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param end_date: (optional) note: date is UTC date. format 'YYYY-MM-DD'
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "withdrawals":[
              {
                 "amount":10,
                 "created":"2020-05-21T13:22:45.000Z",
                 "status":"created"
              },
              {
                 "amount":20,
                 "created":"2020-05-21T13:22:45.000Z",
                 "status":"created"
              }
           ]
        }
        """

        data = {}
        if start_date:
            data['startdate'] = start_date
        if end_date:
            data['enddate'] = end_date

        return self._request('/my/withdrawals', data=data, nonce=nonce)
    
    def affiliate_payment_history(self, nonce: int = None) -> dict:
        """
        Return a list of affiliate payments you have received in the past
        
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "payments":[
              {
                 "amount":111.1111,
                 "month":"2020-05-21T13:22:45.000Z"
              },
              {
                 "amount":111.1111,
                 "month":"2020-04-21T13:22:45.000Z"
              }
           ]
        }
        """

        return self._request('/my/affiliatepayments', nonce=nonce)
    
    def referral_payment_history(self, nonce: int = None) -> dict:
        """
        Return a list of referral payments you have received in the past
        
        :param nonce: (optional) Nonce. See the docs for more detail
        :return: {
           "status":"ok",
           "message":"ok",
           "payments":[
              {
                 "amount":111.1111,
                 "coin":"BTC",
                 "audamount":10,
                 "timestamp":"2020-04-21T13:22:45.000Z"
              },
              {
                 "amount":222.22222,
                 "coin":"BTC",
                 "audamount":10,
                 "timestamp":"2020-05-21T13:22:45.000Z"
              }
           ]
        }
        """
        
        return self._request('/my/referralpayments', nonce=nonce)
