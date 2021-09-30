import os
from utils import list_from_url, list_from_base, convert_from_url,  convert_from_base, history_get
from models import User, Exchange, Session
from datetime import datetime, timedelta
from forex_python.converter import CurrencyCodes
import matplotlib.pyplot as plt

url = "http://api.exchangeratesapi.io/v1/"

api_key = "61547cc7a762ed584ab57a285f7515c5"


last_update = datetime.now()-timedelta(minutes=15)

def get_list_for_base(bot, update):
    global last_update
    session = Session()
    chat_id = bot.effective_chat.id
    user = session.query(User).filter(User.user_chat_id == chat_id).first()
    if not user:
        user = User(chat_id=chat_id)
        session.add(user)
        session.commit()
    base = user.base
    if datetime.now() > last_update+timedelta(minutes=10):
        result = list_from_url(url=url, api_key=api_key, base=base)
        update.bot.send_message(chat_id=chat_id, text=result)
        last_update = datetime.now()
    else:
        exchanges = session.query(Exchange).all()
        result = list_from_base(exchanges, base=base)
        update.bot.send_message(chat_id=chat_id, text=result)


def start(bot, update):
    session = Session()
    chat_id = bot.effective_chat.id
    user = User(chat_id=chat_id)
    session.add(user)
    session.commit()
    update.bot.send_message(chat_id=chat_id, text= "Hi, I'm ExchangeBot, i will show you current exchange(your base currency is USD)")

def change_base(bot, update):
    session = Session()
    chat_id = bot.effective_chat.id
    user = session.query(User).filter(User.user_chat_id == chat_id).first()
    exchanges = session.query(Exchange.currency).all()
    print(update.args)
    print(exchanges)
    for exchange in exchanges:
        if exchange[0] == update.args[0].upper():
            user.base = update.args[0].upper()
            session.commit()
            update.bot.send_message(chat_id=chat_id,
                                    text=f"Base currency changed to {user.base}")
            break
    else:
        update.bot.send_message(chat_id=chat_id,
                                text=f"Sorry but there is no such currency")


def convert(bot, update):
    chat_id = bot.effective_chat.id
    try:
        amount = int(update.args[0])
        base = update.args[1]
        symbol = update.args[3]
        if datetime.now() > last_update + timedelta(minutes=10):
            result = convert_from_url(url=url, api_key=api_key, amount=amount, base=base, symbol=symbol)
            update.bot.send_message(chat_id=chat_id,
                                    text=result)
        else:
            session = Session()
            exchanges = session.query(Exchange).all()
            result = convert_from_base(exchanges=exchanges, amount=amount, base=base, symbol=symbol)
            update.bot.send_message(chat_id=chat_id,
                                    text=result)
    except Exception:
        update.bot.send_message(chat_id=chat_id,
                               text="you should try to use it like this '/exchange 10 USD to EUR'")



def history(bot, update):
    chat_id = bot.effective_chat.id
    try:
        base = update.args[0]
        days = int(update.args[2])
        price_row_and_days_row = history_get(url=url,
                                             api_key=api_key,
                                             base=base,
                                             days=days)
        plt.title(f"{base} changes for {days} days")
        plt.xlabel("days")
        plt.ylabel("price")
        plt.plot(price_row_and_days_row[1], price_row_and_days_row[0])
        plt.savefig("image.png")
        update.bot.send_photo(chat_id=chat_id,
                              photo=open("image.png", "rb"))
    except Exception:
        update.bot.send_message(chat_id=chat_id, text="you should try to use in like this '/history USD for 5 days'")

def help_command(bot, update):
    chat_id = bot.effective_chat.id
    update.bot.send_message(chat_id=chat_id, text="You can use "
                                                  "/list - to get list of all currencies in comparison with the main\n"
                                                  "/change_base_currency - to change your base currency (example '/change_base_currency USD')\n"
                                                  "/exchange - to show exchange one currency to another (example /exchange 10 USD to EUR)\n"
                                                  "/history - to see history of changing currency price (example /history USD for 5 days)")
