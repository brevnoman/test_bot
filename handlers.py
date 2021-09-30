import datetime

from telegram.ext import CommandHandler
from controller import get_list_for_base, start, change_base, convert, history

get_list_handler = CommandHandler("list", get_list_for_base)
start_handler = CommandHandler("start", start)
change_base_handler = CommandHandler("change_base_currency", change_base)
exchange_handler = CommandHandler("exchange", convert)
history_handler = CommandHandler("history", history)
