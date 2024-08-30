from pydantic import BaseModel, Field, EmailStr
from utils.id_generator import IDGenerator
from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Optional

from typing import List
from uuid import UUID

unique_id = IDGenerator()


class UserBaseSchema(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    # is_verified: Optional[bool] = Field()


class UserCreate(UserBaseSchema):
    phone_number: str
    password: str
    first_name: str
    last_name: str
    created_at: str | None

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")


class UserRead(UserBaseSchema):
    phone_number: str
    first_name: str
    last_name: str

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        return data


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    user_phone: Optional[str] = None


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
