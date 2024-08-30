import logging
from fastapi import status, HTTPException, BackgroundTasks, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from security.utils import (verify_password, get_hash_password, create_access_token)
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from dao.user import DaoUser
from models.models import User
from schemas.schema import (UserCreate, Token, TokenPayload, UserRead)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserManager:
    def __init__(self, session: Session):
        self._dao = DaoUser(session=session)
        self.logger = logger

    async def login(self, phone_number: str, password: str) -> ORJSONResponse:
        db_user = await self.authenticate(phone_number=phone_number, password=password)
        await self.last_login(db_user)
        token = self.get_access_token(user=db_user)
        token = jsonable_encoder(token)
        self.logger.info(f"token generated for user: {phone_number!r}")
        return ORJSONResponse(content=token, status_code=status.HTTP_200_OK)

    async def register(self, bgt: BackgroundTasks, user_in: UserCreate) -> ORJSONResponse:
        db_user = await self.find_by_phone_number(phone_number=user_in.phone_number)
        # TODO: reactive inactive user
        if db_user:
            self.logger.error(f"duplicate user phone number {user_in.phone_number!r}")
            raise HTTPException(detail=ErrorMessage.PHONE_NUMBER_TAKEN,
                                status_code=status.HTTP_400_BAD_REQUEST)

        db_user = await self.create(user_in=user_in)

        db_user_encoded = jsonable_encoder(db_user)
        response_data = UserRead(**db_user_encoded).model_dump()

        return ORJSONResponse(content=response_data,
                              status_code=status.HTTP_201_CREATED)

    async def create(self, user_in: UserCreate) -> User:
        user_in.password = get_hash_password(user_in.password)
        try:
            db_user = self._dao.create(user_in=user_in)
            self.logger.info(f"user {user_in.phone_number} created")
            return db_user
        except Exception as error:
            logger.error(error)
            raise HTTPException(
                detail=ErrorMessage.REGISTRATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def find_by_phone_number(self, phone_number: str) -> User:
        return self._dao.find_by_phone_number(phone_number=phone_number)

    async def authenticate(self, phone_number: str, password: str) -> User:
        db_user = await self.find_by_phone_number(phone_number=phone_number)
        if not verify_password(password, db_user.password):
            self.logger.error(f"wrong credentials for user {phone_number!r}")
            raise HTTPException(detail=ErrorMessage.BAD_CREDENTIALS,
                                status_code=status.HTTP_400_BAD_REQUEST)
        return db_user

    async def last_login(self, db_user: User) -> None:
        self._dao.last_login(db_user)

    @staticmethod
    def get_access_token(user: User) -> Token:
        return Token(
            access_token=create_access_token(
                subject=TokenPayload(user_phone=user.phone_number),
                expires_duration=10)
        )
