from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Column, Integer, Float, Boolean, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RequestAccountsInDB(Base):
    __tablename__ = "customer_transaction_requests"
    request_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="PENDING")


class TransactionInDB(Base):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    request_id = Column(String, nullable=False)
    customer_id = Column(BigInteger, nullable=False)  # Changed to BigInteger
    url = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)

    def __init__(self, date, request_id, customer_id, url, amount, type):
        self.date = date
        self.request_id = request_id
        self.customer_id = customer_id
        self.url = url
        self.amount = amount
        self.type = type
