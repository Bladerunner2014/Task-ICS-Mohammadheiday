from dotenv import dotenv_values
from fastapi import FastAPI, Depends
import logging
from log import log
from schemas.schema import CustomerID, RequestAccounts
from handler.handler import Accounts, CustomerTransaction
from queue_handler.tasks import get_transactions_task
from constants.info_message import InfoMessage
from fastapi import BackgroundTasks, HTTPException, status
from fastapi.responses import ORJSONResponse
from constants.error_message import ErrorMessage
from security.auth import CurrentUser
from manager.user_manager import UserManager
from schemas.schema import UserCreate
from security.dependency import SessionDep
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post('/request/list', summary='status of requests')
async def requests(customer_id: CustomerID) -> ORJSONResponse:
    handler = CustomerTransaction()
    result = handler.requests_list(customer_id.customer_id)
    return result


@app.post('/request', summary='send request to gather transactions')
async def get_customers_accounts(customer_request: RequestAccounts,):
    logger.info(InfoMessage.TRANSACTION_REQUEST)
    get_transactions_task.delay(customer_request.dict())
    return ORJSONResponse(content={"message": "request submitted"}, status_code=status.HTTP_200_OK)


@app.post('/transactions', summary='transactions in a request id')
async def transactions(request_id: str) -> ORJSONResponse:
    handler = CustomerTransaction()
    result = handler.transactions(request_id)
    return result


@app.post('/amount', summary='get amounts of a request_id')
async def get_requests_list(request_id: str):
    handler = CustomerTransaction()
    result = handler.amounts(request_id)
    return result
#
#
# @app.post('/requests/detail', summary='get details of customer request')
# async def get_requests_list(request_id):
#     pass


@app.post("/register")
async def register(user_in: UserCreate,
                   session: SessionDep,
                   background_task: BackgroundTasks) -> ORJSONResponse:
    manager = UserManager(session=session)

    return await manager.register(user_in=user_in, bgt=background_task)


@app.post("/login")
async def login(session: SessionDep,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> ORJSONResponse:
    manager = UserManager(session=session)
    return await manager.login(phone_number=form_data.username, password=form_data.password)


log.setup_logger()
