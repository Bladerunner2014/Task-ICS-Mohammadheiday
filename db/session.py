from db.engine import SessionLocal

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator, Annotated


async def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

SessionDep = Annotated[Session, Depends(get_session)]