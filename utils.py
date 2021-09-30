import datetime

import requests
from models import Exchange, Session


def list_from_url(url, api_key, base="USD"):
    session = Session()
    response = requests.request("GET", url=url+"latest", params={"access_key": api_key})
    currency_dict = response.json()['rates']
    result = f"for 1 {base}\n"
    usd_exchange = response.json()["rates"][base]
    session.query(Exchange).delete()
    for name_of_currency, currency_exchange in currency_dict.items():
        currency = Exchange(currency=name_of_currency, exchange=currency_exchange)
        session.add(currency)
        result += f"{name_of_currency}: {round(currency_exchange/usd_exchange, ndigits=2)}\n"
    session.commit()

    return result

def list_from_base(exchanges, base):
    result = f"for 1 {base}\n"
    for exchange in exchanges:
        result += f"{exchange.currency}: {exchange.exchange}\n"
    return result

def convert_from_url(url, api_key, amount, base, symbol):
    base = base.upper()
    symbol = symbol.upper()
    response = requests.request("GET", url=url + "latest", params={"access_key": api_key, "symbols":base + "," + symbol})
    currency_dict = response.json()['rates']
    exchange = currency_dict[symbol]/ currency_dict[base]
    return f"you will get {round(amount * exchange, ndigits=2)} {symbol} for {amount} {base}"

def convert_from_base(exchanges, amount, base, symbol):
    base = base.upper()
    symbol = symbol.upper()
    for exchange in exchanges:
        if exchange[0] == base:
            base_exchange = exchange[1]
        if exchange[0] == symbol:
            symbol_exchange = exchange[1]
    exchange = symbol_exchange/base_exchange
    return f"you will get {round(amount * exchange, ndigits=2)} {symbol} for {amount} {base}"


def history_get(url, api_key, base, days):
    today = datetime.date.today()
    base_row = []
    days_row = []
    for i in range(1, days+1):
        one_of_the_days =today - datetime.timedelta(days=i)
        print(one_of_the_days)
        response = requests.request("GET", url=url + str(one_of_the_days), params={"access_key": api_key, "symbols":base})
        print(response.json())
        currency_dict = response.json()['rates']
        base_row.append(currency_dict[base])
        days_row.append(str(one_of_the_days.month)+"-"+str(one_of_the_days.day))
    days_row.reverse()
    base_row.reverse()
    return (base_row, days_row)
