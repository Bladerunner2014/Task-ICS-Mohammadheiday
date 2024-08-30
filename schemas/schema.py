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


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class RequestAccounts(BaseModel):
    request_id: str | None
    customer_id: CustomerID
    created_at: str | None
    status: str | None

    def __init__(self, **data):
        super().__init__(**data)
        self.request_id = unique_id.generate_custom_id('R')
        self.created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.status = Status.PENDING



