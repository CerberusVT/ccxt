# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import InvalidNonce


class bitstamp (Exchange):

    def describe(self):
        return self.deep_extend(super(bitstamp, self).describe(), {
            'id': 'bitstamp',
            'name': 'Bitstamp',
            'countries': ['GB'],
            'rateLimit': 1000,
            'version': 'v2',
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': True,
                'fetchDepositAddress': True,
                'fetchOrder': 'emulated',
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'fetchTransactions': True,
                'fetchWithdrawals': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27786377-8c8ab57e-5fe9-11e7-8ea4-2b05b6bcceec.jpg',
                'api': 'https://www.bitstamp.net/api',
                'www': 'https://www.bitstamp.net',
                'doc': 'https://www.bitstamp.net/api',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'order_book/{pair}/',
                        'ticker_hour/{pair}/',
                        'ticker/{pair}/',
                        'transactions/{pair}/',
                        'trading-pairs-info/',
                    ],
                },
                'private': {
                    'post': [
                        'balance/',
                        'balance/{pair}/',
                        'bch_withdrawal/',
                        'bch_address/',
                        'user_transactions/',
                        'user_transactions/{pair}/',
                        'open_orders/all/',
                        'open_orders/{pair}/',
                        'order_status/',
                        'cancel_order/',
                        'buy/{pair}/',
                        'buy/market/{pair}/',
                        'buy/instant/{pair}/',
                        'sell/{pair}/',
                        'sell/market/{pair}/',
                        'sell/instant/{pair}/',
                        'ltc_withdrawal/',
                        'ltc_address/',
                        'eth_withdrawal/',
                        'eth_address/',
                        'xrp_withdrawal/',
                        'xrp_address/',
                        'transfer-to-main/',
                        'transfer-from-main/',
                        'withdrawal-requests/',
                        'withdrawal/open/',
                        'withdrawal/status/',
                        'withdrawal/cancel/',
                        'liquidation_address/new/',
                        'liquidation_address/info/',
                    ],
                },
                'v1': {
                    'post': [
                        'bitcoin_deposit_address/',
                        'unconfirmed_btc/',
                        'bitcoin_withdrawal/',
                        'ripple_withdrawal/',
                        'ripple_address/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                    'tiers': {
                        'taker': [
                            [0, 0.25 / 100],
                            [20000, 0.24 / 100],
                            [100000, 0.22 / 100],
                            [400000, 0.20 / 100],
                            [600000, 0.15 / 100],
                            [1000000, 0.14 / 100],
                            [2000000, 0.13 / 100],
                            [4000000, 0.12 / 100],
                            [20000000, 0.11 / 100],
                            [20000001, 0.10 / 100],
                        ],
                        'maker': [
                            [0, 0.25 / 100],
                            [20000, 0.24 / 100],
                            [100000, 0.22 / 100],
                            [400000, 0.20 / 100],
                            [600000, 0.15 / 100],
                            [1000000, 0.14 / 100],
                            [2000000, 0.13 / 100],
                            [4000000, 0.12 / 100],
                            [20000000, 0.11 / 100],
                            [20000001, 0.10 / 100],
                        ],
                    },
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0,
                        'BCH': 0,
                        'LTC': 0,
                        'ETH': 0,
                        'XRP': 0,
                        'USD': 25,
                        'EUR': 0.90,
                    },
                    'deposit': {
                        'BTC': 0,
                        'BCH': 0,
                        'LTC': 0,
                        'ETH': 0,
                        'XRP': 0,
                        'USD': 25,
                        'EUR': 0,
                    },
                },
            },
            'exceptions': {
                'exact': {
                    'No permission found': PermissionDenied,
                    'API key not found': AuthenticationError,
                    'IP address not allowed': PermissionDenied,
                    'Invalid nonce': InvalidNonce,
                    'Invalid signature': AuthenticationError,
                    'Authentication failed': AuthenticationError,
                    'Missing key, signature and nonce parameters': AuthenticationError,
                    'Your account is frozen': PermissionDenied,
                    'Please update your profile with your FATCA information, before using API.': PermissionDenied,
                    'Order not found': OrderNotFound,
                    'Price is more than 20% below market price.': InvalidOrder,
                },
                'broad': {
                    'Minimum order size is': InvalidOrder,  # Minimum order size is 5.0 EUR.
                    'Check your account balance for details.': InsufficientFunds,  # You have only 0.00100000 BTC available. Check your account balance for details.
                    'Ensure self value has at least': InvalidAddress,  # Ensure self value has at least 25 characters(it has 4).
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetTradingPairsInfo(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            name = self.safe_string(market, 'name')
            base, quote = name.split('/')
            baseId = base.lower()
            quoteId = quote.lower()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            symbolId = baseId + '_' + quoteId
            id = self.safe_string(market, 'url_symbol')
            precision = {
                'amount': market['base_decimals'],
                'price': market['counter_decimals'],
            }
            parts = market['minimum_order'].split(' ')
            cost = parts[0]
            # cost, currency = market['minimum_order'].split(' ')
            active = (market['trading'] == 'Enabled')
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'symbolId': symbolId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': float(cost),
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        response = await self.publicGetOrderBookPair(self.extend(request, params))
        timestamp = self.safe_integer(response, 'timestamp')
        if timestamp is not None:
            timestamp *= 1000
        return self.parse_order_book(response, timestamp)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        ticker = await self.publicGetTickerPair(self.extend(request, params))
        timestamp = self.safe_integer(ticker, 'timestamp')
        if timestamp is not None:
            timestamp *= 1000
        vwap = self.safe_float(ticker, 'vwap')
        baseVolume = self.safe_float(ticker, 'volume')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def get_currency_id_from_transaction(self, transaction):
        #
        #     {
        #         "fee": "0.00000000",
        #         "btc_usd": "0.00",
        #         "datetime": XXX,
        #         "usd": 0.0,
        #         "btc": 0.0,
        #         "eth": "0.05000000",
        #         "type": "0",
        #         "id": XXX,
        #         "eur": 0.0
        #     }
        #
        if 'currency' in transaction:
            return transaction['currency'].lower()
        transaction = self.omit(transaction, [
            'fee',
            'price',
            'datetime',
            'type',
            'status',
            'id',
        ])
        ids = list(transaction.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if id.find('_') < 0:
                value = self.safe_float(transaction, id)
                if (value is not None) and(value != 0):
                    return id
        return None

    def get_market_from_trade(self, trade):
        trade = self.omit(trade, [
            'fee',
            'price',
            'datetime',
            'tid',
            'type',
            'order_id',
            'side',
        ])
        currencyIds = list(trade.keys())
        numCurrencyIds = len(currencyIds)
        if numCurrencyIds > 2:
            raise ExchangeError(self.id + ' getMarketFromTrade too many keys: ' + self.json(currencyIds) + ' in the trade: ' + self.json(trade))
        if numCurrencyIds == 2:
            marketId = currencyIds[0] + currencyIds[1]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
            marketId = currencyIds[1] + currencyIds[0]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
        return None

    def get_market_from_trades(self, trades):
        tradesBySymbol = self.index_by(trades, 'symbol')
        symbols = list(tradesBySymbol.keys())
        numSymbols = len(symbols)
        if numSymbols == 1:
            return self.markets[symbols[0]]
        return None

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         date: '1551814435',
        #         tid: '83581898',
        #         price: '0.03532850',
        #         type: '1',
        #         amount: '0.85945907'
        #     },
        #
        # fetchMyTrades, trades returned within fetchOrder(private)
        #
        #     {
        #         "usd": "6.0134400000000000",
        #         "price": "4008.96000000",
        #         "datetime": "2019-03-28 23:07:37.233599",
        #         "fee": "0.02",
        #         "btc": "0.00150000",
        #         "tid": 84452058,
        #         "type": 2
        #     }
        #
        # from fetchOrder:
        #    {fee: '0.000019',
        #     price: '0.00015803',
        #     datetime: '2018-01-07 10:45:34.132551',
        #     btc: '0.0079015000000000',
        #     tid: 42777395,
        #     type: 2,  #(0 - deposit 1 - withdrawal 2 - market trade) NOT buy/sell
        #     xrp: '50.00000000'}
        id = self.safe_string_2(trade, 'id', 'tid')
        symbol = None
        side = None
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        orderId = self.safe_string(trade, 'order_id')
        type = None
        cost = self.safe_float(trade, 'cost')
        if market is None:
            keys = list(trade.keys())
            for i in range(0, len(keys)):
                if keys[i].find('_') >= 0:
                    marketId = keys[i].replace('_', '')
                    if marketId in self.markets_by_id:
                        market = self.markets_by_id[marketId]
            # if the market is still not defined
            # try to deduce it from used keys
            if market is None:
                market = self.get_market_from_trade(trade)
        feeCost = self.safe_float(trade, 'fee')
        feeCurrency = None
        if market is not None:
            price = self.safe_float(trade, market['symbolId'], price)
            amount = self.safe_float(trade, market['baseId'], amount)
            cost = self.safe_float(trade, market['quoteId'], cost)
            feeCurrency = market['quote']
            symbol = market['symbol']
        timestamp = self.safe_string_2(trade, 'date', 'datetime')
        if timestamp is not None:
            if timestamp.find(' ') >= 0:
                # iso8601
                timestamp = self.parse8601(timestamp)
            else:
                # string unix epoch in seconds
                timestamp = int(timestamp)
                timestamp = timestamp * 1000
        # if it is a private trade
        if 'id' in trade:
            if amount is not None:
                if amount < 0:
                    side = 'sell'
                    amount = -amount
                else:
                    side = 'buy'
        else:
            side = self.safe_string(trade, 'type')
            if side == '1':
                side = 'sell'
            elif side == '0':
                side = 'buy'
        if cost is None:
            if price is not None:
                if amount is not None:
                    cost = price * amount
        if cost is not None:
            cost = abs(cost)
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'time': 'hour',
        }
        response = await self.publicGetTransactionsPair(self.extend(request, params))
        #
        #     [
        #         {
        #             date: '1551814435',
        #             tid: '83581898',
        #             price: '0.03532850',
        #             type: '1',
        #             amount: '0.85945907'
        #         },
        #         {
        #             date: '1551814434',
        #             tid: '83581896',
        #             price: '0.03532851',
        #             type: '1',
        #             amount: '11.34130961'
        #         },
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balance = await self.privatePostBalance(params)
        result = {'info': balance}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            currencyId = currency['id']
            account = self.account()
            account['free'] = self.safe_float(balance, currencyId + '_available')
            account['used'] = self.safe_float(balance, currencyId + '_reserved')
            account['total'] = self.safe_float(balance, currencyId + '_balance')
            result[code] = account
        return self.parse_balance(result)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        method = 'privatePost' + self.capitalize(side)
        request = {
            'pair': market['id'],
            'amount': self.amount_to_precision(symbol, amount),
        }
        if type == 'market':
            method += 'Market'
        else:
            request['price'] = self.price_to_precision(symbol, price)
        method += 'Pair'
        response = await getattr(self, method)(self.extend(request, params))
        order = self.parse_order(response, market)
        return self.extend(order, {
            'type': type,
        })

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'In Queue': 'open',
            'Open': 'open',
            'Finished': 'closed',
            'Canceled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    async def fetch_order_status(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privatePostOrderStatus(self.extend(request, params))
        return self.parse_order_status(self.safe_string(response, 'status'))

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {'id': id}
        response = await self.privatePostOrderStatus(self.extend(request, params))
        #
        #     {
        #         "status": "Finished",
        #         "id": 3047704374,
        #         "transactions": [
        #             {
        #                 "usd": "6.0134400000000000",
        #                 "price": "4008.96000000",
        #                 "datetime": "2019-03-28 23:07:37.233599",
        #                 "fee": "0.02",
        #                 "btc": "0.00150000",
        #                 "tid": 84452058,
        #                 "type": 2
        #             }
        #         ]
        #     }
        return self.parse_order(response, market)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        method = 'privatePostUserTransactions'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
            method += 'Pair'
        if limit is not None:
            request['limit'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        result = self.filter_by(response, 'type', '2')
        return self.parse_trades(result, market, since, limit)

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        response = await self.privatePostUserTransactions(self.extend(request, params))
        #
        #     [
        #         {
        #             "fee": "0.00000000",
        #             "btc_usd": "0.00",
        #             "id": 1234567894,
        #             "usd": 0,
        #             "btc": 0,
        #             "datetime": "2018-09-08 09:00:31",
        #             "type": "1",
        #             "xrp": "-20.00000000",
        #             "eur": 0,
        #         },
        #         {
        #             "fee": "0.00000000",
        #             "btc_usd": "0.00",
        #             "id": 1134567891,
        #             "usd": 0,
        #             "btc": 0,
        #             "datetime": "2018-09-07 18:47:52",
        #             "type": "0",
        #             "xrp": "20.00000000",
        #             "eur": 0,
        #         },
        #     ]
        #
        currency = None
        if code is not None:
            currency = self.currency(code)
        transactions = self.filter_by_array(response, 'type', ['0', '1'], False)
        return self.parseTransactions(transactions, currency, since, limit)

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if since is not None:
            request['timedelta'] = self.milliseconds() - since
        response = await self.privatePostWithdrawalRequests(self.extend(request, params))
        #
        #     [
        #         {
        #             status: 2,
        #             datetime: '2018-10-17 10:58:13',
        #             currency: 'BTC',
        #             amount: '0.29669259',
        #             address: 'aaaaa',
        #             type: 1,
        #             id: 111111,
        #             transaction_id: 'xxxx',
        #         },
        #         {
        #             status: 2,
        #             datetime: '2018-10-17 10:55:17',
        #             currency: 'ETH',
        #             amount: '1.11010664',
        #             address: 'aaaa',
        #             type: 16,
        #             id: 222222,
        #             transaction_id: 'xxxxx',
        #         },
        #     ]
        #
        return self.parseTransactions(response, None, since, limit)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchTransactions
        #
        #     {
        #         "fee": "0.00000000",
        #         "btc_usd": "0.00",
        #         "id": 1234567894,
        #         "usd": 0,
        #         "btc": 0,
        #         "datetime": "2018-09-08 09:00:31",
        #         "type": "1",
        #         "xrp": "-20.00000000",
        #         "eur": 0,
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         status: 2,
        #         datetime: '2018-10-17 10:58:13',
        #         currency: 'BTC',
        #         amount: '0.29669259',
        #         address: 'aaaaa',
        #         type: 1,
        #         id: 111111,
        #         transaction_id: 'xxxx',
        #     }
        #
        timestamp = self.parse8601(self.safe_string(transaction, 'datetime'))
        code = None
        id = self.safe_string(transaction, 'id')
        currencyId = self.get_currency_id_from_transaction(transaction)
        if currencyId in self.currencies_by_id:
            currency = self.currencies_by_id[currencyId]
        elif currencyId is not None:
            code = currencyId.upper()
            code = self.common_currency_code(code)
        feeCost = self.safe_float(transaction, 'fee')
        feeCurrency = None
        amount = None
        if currency is not None:
            amount = self.safe_float(transaction, currency['id'], amount)
            feeCurrency = currency['code']
            code = currency['code']
        elif (code is not None) and(currencyId is not None):
            amount = self.safe_float(transaction, currencyId, amount)
            feeCurrency = code
        if amount is not None:
            # withdrawals have a negative amount
            amount = abs(amount)
        status = self.parse_transaction_status_by_type(self.safe_string(transaction, 'status'))
        type = self.safe_string(transaction, 'type')
        if status is None:
            if type == '0':
                type = 'deposit'
            elif type == '1':
                type = 'withdrawal'
        else:
            type = 'withdrawal'
        txid = self.safe_string(transaction, 'transaction_id')
        address = self.safe_string(transaction, 'address')
        tag = None  # not documented
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'fee': {
                'currency': feeCurrency,
                'cost': feeCost,
                'rate': None,
            },
        }

    def parse_transaction_status_by_type(self, status):
        # withdrawals:
        # 0(open), 1(in process), 2(finished), 3(canceled) or 4(failed).
        statuses = {
            '0': 'pending',  # Open
            '1': 'pending',  # In process
            '2': 'ok',  # Finished
            '3': 'canceled',  # Canceled
            '4': 'failed',  # Failed
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        # from fetch order:
        #   {status: 'Finished',
        #     id: 731693945,
        #     transactions:
        #     [{fee: '0.000019',
        #         price: '0.00015803',
        #         datetime: '2018-01-07 10:45:34.132551',
        #         btc: '0.0079015000000000',
        #         tid: 42777395,
        #         type: 2,
        #         xrp: '50.00000000'}]}
        #
        # partially filled order:
        #   {"id": 468646390,
        #     "status": "Canceled",
        #     "transactions": [{
        #         "eth": "0.23000000",
        #         "fee": "0.09",
        #         "tid": 25810126,
        #         "usd": "69.8947000000000000",
        #         "type": 2,
        #         "price": "303.89000000",
        #         "datetime": "2017-11-11 07:22:20.710567"
        #     }]}
        #
        # from create order response:
        #     {
        #         price: '0.00008012',
        #         currency_pair: 'XRP/BTC',
        #         datetime: '2019-01-31 21:23:36',
        #         amount: '15.00000000',
        #         type: '0',
        #         id: '2814205012'
        #     }
        #
        id = self.safe_string(order, 'id')
        side = self.safe_string(order, 'type')
        if side is not None:
            side = 'sell' if (side == '1') else 'buy'
        # there is no timestamp from fetchOrder
        timestamp = self.parse8601(self.safe_string(order, 'datetime'))
        lastTradeTimestamp = None
        symbol = None
        marketId = self.safe_string(order, 'currency_pair')
        if marketId is not None:
            marketId = marketId.replace('/', '')
            marketId = marketId.lower()
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
        amount = self.safe_float(order, 'amount')
        filled = 0.0
        trades = []
        transactions = self.safe_value(order, 'transactions', [])
        feeCost = None
        cost = None
        numTransactions = len(transactions)
        if numTransactions > 0:
            feeCost = 0.0
            for i in range(0, numTransactions):
                trade = self.parse_trade(self.extend({
                    'order_id': id,
                    'side': side,
                }, transactions[i]), market)
                filled = self.sum(filled, trade['amount'])
                feeCost = self.sum(feeCost, trade['fee']['cost'])
                if cost is None:
                    cost = 0.0
                cost = self.sum(cost, trade['cost'])
                trades.append(trade)
            lastTradeTimestamp = trades[numTransactions - 1]['timestamp']
        status = self.parse_order_status(self.safe_string(order, 'status'))
        if (status == 'closed') and(amount is None):
            amount = filled
        remaining = None
        if amount is not None:
            remaining = amount - filled
        price = self.safe_float(order, 'price')
        if market is None:
            market = self.get_market_from_trades(trades)
        feeCurrency = None
        if market is not None:
            if symbol is None:
                symbol = market['symbol']
            feeCurrency = market['quote']
        if cost is None:
            if price is not None:
                cost = price * filled
        elif price is None:
            if filled > 0:
                price = cost / filled
        fee = None
        if feeCost is not None:
            if feeCurrency is not None:
                fee = {
                    'cost': feeCost,
                    'currency': feeCurrency,
                }
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': lastTradeTimestamp,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': fee,
            'info': order,
        }

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        market = None
        await self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
        response = await self.privatePostOpenOrdersAll(params)
        #     [
        #         {
        #             price: '0.00008012',
        #             currency_pair: 'XRP/BTC',
        #             datetime: '2019-01-31 21:23:36',
        #             amount: '15.00000000',
        #             type: '0',
        #             id: '2814205012',
        #         }
        #     ]
        #
        result = []
        for i in range(0, len(response)):
            order = self.parse_order(response[i], market)
            result.append(self.extend(order, {
                'status': 'open',
                'type': 'limit',
            }))
        if symbol is None:
            return self.filter_by_since_limit(result, since, limit)
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def get_currency_name(self, code):
        if code == 'BTC':
            return 'bitcoin'
        return code.lower()

    def is_fiat(self, code):
        if code == 'USD':
            return True
        if code == 'EUR':
            return True
        return False

    async def fetch_deposit_address(self, code, params={}):
        if self.is_fiat(code):
            raise NotSupported(self.id + ' fiat fetchDepositAddress() for ' + code + ' is not implemented yet')
        name = self.get_currency_name(code)
        v1 = (code == 'BTC')
        method = 'v1' if v1 else 'private'  # v1 or v2
        method += 'Post' + self.capitalize(name)
        method += 'Deposit' if v1 else ''
        method += 'Address'
        response = await getattr(self, method)(params)
        address = response if v1 else self.safe_string(response, 'address')
        tag = None if v1 else self.safe_string(response, 'destination_tag')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        if self.is_fiat(code):
            raise NotSupported(self.id + ' fiat withdraw() for ' + code + ' is not implemented yet')
        name = self.get_currency_name(code)
        request = {
            'amount': amount,
            'address': address,
        }
        v1 = (code == 'BTC')
        method = 'v1' if v1 else 'private'  # v1 or v2
        method += 'Post' + self.capitalize(name) + 'Withdrawal'
        query = params
        if code == 'XRP':
            if tag is not None:
                request['destination_tag'] = tag
                query = self.omit(params, 'destination_tag')
            else:
                raise ExchangeError(self.id + ' withdraw() requires a destination_tag param for ' + code)
        response = await getattr(self, method)(self.extend(request, query))
        return {
            'info': response,
            'id': response['id'],
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if api != 'v1':
            url += self.version + '/'
        url += self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + self.uid + self.apiKey
            signature = self.encode(self.hmac(self.encode(auth), self.encode(self.secret)))
            query = self.extend({
                'key': self.apiKey,
                'signature': signature.upper(),
                'nonce': nonce,
            }, query)
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None:
            return
        #
        #     {"error": "No permission found"}  # fetchDepositAddress returns self on apiKeys that don't have the permission required
        #     {"status": "error", "reason": {"__all__": ["Minimum order size is 5.0 EUR."]}}
        #     reuse of a nonce gives: {status: 'error', reason: 'Invalid nonce', code: 'API0004'}
        status = self.safe_string(response, 'status')
        error = self.safe_value(response, 'error')
        if (status == 'error') or (error is not None):
            errors = []
            if isinstance(error, basestring):
                errors.append(error)
            elif error is not None:
                keys = list(error.keys())
                for i in range(0, len(keys)):
                    key = keys[i]
                    value = self.safe_value(error, key)
                    if isinstance(value, list):
                        errors = self.array_concat(errors, value)
                    else:
                        errors.append(value)
            reason = self.safe_value(response, 'reason', {})
            if isinstance(reason, basestring):
                errors.append(reason)
            else:
                all = self.safe_value(reason, '__all__', [])
                for i in range(0, len(all)):
                    errors.append(all[i])
            code = self.safe_string(response, 'code')
            if code == 'API0005':
                raise AuthenticationError(self.id + ' invalid signature, use the uid for the main account if you have subaccounts')
            exact = self.exceptions['exact']
            broad = self.exceptions['broad']
            feedback = self.id + ' ' + body
            for i in range(0, len(errors)):
                value = errors[i]
                if value in exact:
                    raise exact[value](feedback)
                broadKey = self.findBroadlyMatchedKey(broad, value)
                if broadKey is not None:
                    raise broad[broadKey](feedback)
            raise ExchangeError(feedback)
