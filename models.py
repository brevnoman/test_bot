from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float

engine = create_engine('sqlite:///users_exchange.db', echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)

class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True)
    currency = Column(String(3))
    exchange = Column(Float)

    def __init__(self, currency, exchange):
        self.currency = currency
        self.exchange = exchange

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_chat_id = Column(String(255))
    base = Column(String(3), default="USD")

    def __init__(self, chat_id, base="USD"):
        self.user_chat_id = chat_id
        self.base = base

