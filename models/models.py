from sqlalchemy import Column, Float, BigInteger

from datetime import datetime, timezone
from sqlalchemy import String, Boolean, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(String(length=11), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=256), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=256), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=None, nullable=False)


class RequestAccountsInDB(Base):
    __tablename__ = "customer_transaction_requests"
    request_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    created_at = Column(String, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="PENDING")


class TransactionInDB(Base):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
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
