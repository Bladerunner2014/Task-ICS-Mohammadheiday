from pydantic import BaseModel, Field
from utils.id_generator import IDGenerator
from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import List
from uuid import UUID

unique_id = IDGenerator()


class CustomerID(BaseModel):
    customer_id: int


class Banks(BaseModel):
    customer_id: CustomerID
    phone_number: str = Field(..., max_length=15)
    code: UUID
    banks: List[str]


class Transaction(BaseModel):
    date: datetime
    type: str
    amount: int
    bank: str


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class RequestAccountsInDB(BaseModel):
    request_id: str | None = Field(default_factory=lambda: unique_id.generate_custom_id("R"))
    customer_id: str
    created_at: str | None = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"))
    status: str | None = Field(default_factory=lambda: Status.PENDING)


class RequestData(BaseModel):
    base_url: str
    end_point: str
    customer_id: str
    bank_name: str
    timeout: int
    error_log_dict: dict
