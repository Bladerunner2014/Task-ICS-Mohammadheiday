import logging
from datetime import datetime, timezone
from typing import Optional, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import User
from schemas.schema import UserCreate

logger = logging.getLogger(__name__)

class DaoUser:
    def __init__(self, session: Session) -> None:
        self.db = session

    def find_by_phone_number(self, phone_number: str) -> Optional[User]:
        statement = select(User).filter_by(phone_number=phone_number)
        user = self.db.scalars(statement).first()
        return user

    def find_by_id(self, user_id: Any) -> Optional[User]:
        statement = select(User).filter_by(id=user_id)
        user = self.db.scalars(statement).first()
        return user
    def last_login(self, db_user: User):
        db_user.last_login = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.save(user=db_user)

    def create(self, user_in: UserCreate):
        db_user = User(**user_in.model_dump())
        return self.save(user=db_user)
    def save(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

