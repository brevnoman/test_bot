from telegram.ext import Updater
import logging
from models import Base, engine
from handlers import get_list_handler, start_handler, change_base_handler, exchange_handler, history_handler

def main():
    updater = Updater(token="2002722331:AAED7F86tngIiuVURVdZsoVksCmYPfVyEJs")
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater.start_polling()
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_list_handler)
    dispatcher.add_handler(change_base_handler)
    dispatcher.add_handler(exchange_handler)
    dispatcher.add_handler(history_handler)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    main()