from pydantic import BaseModel, Field
from utils.id_generator import IDGenerator
from datetime import datetime
from datetime import timezone
from enum import Enum
from pydantic import constr

unique_id = IDGenerator()


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class RequestAccountsInDB(BaseModel):
    request_id: str | None = Field(default_factory=lambda: unique_id.generate_custom_id("R"))
    customer_id: str
    created_at: str | None = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"))
    status: str | None = Field(default_factory=lambda: Status.PENDING)

