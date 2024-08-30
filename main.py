from dotenv import dotenv_values
from fastapi import FastAPI, BackgroundTasks
import logging
from log import log
from schemas.schema import CustomerID, RequestAccounts
from fastapi.responses import ORJSONResponse
from handler.handler import Accounts, CustomerTransaction
from db.session import SessionDep
from constants.info_message import InfoMessage

app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post('/customers/exist', summary='check existence of customer in database')
async def get_customer(customer_id: CustomerID) -> ORJSONResponse:
    handler = Accounts()
    result = handler.check_customer_existence(customer_id=customer_id)
    return result


@app.post('/customers/transaction/list', summary='retrive all customer transactions')
async def get_all_transactions(session: SessionDep,customer_id: CustomerID) -> ORJSONResponse:
    handler = CustomerTransaction(session)
    result = handler.all_transactions(customer_id)
    return result
@app.post('/customers/transaction/request', summary='retrive all transactions related to a request id')
async def get_all_transactions(session: SessionDep,request_id:str) -> ORJSONResponse:
    handler = CustomerTransaction(session)
    result = handler.all_transactions_request(request_id)
    return result

@app.post('/customers/transaction', summary='get transactions')
async def get_customers_accounts(session: SessionDep, customer_request: RequestAccounts,
                                 background_tasks: BackgroundTasks):
    logger.info(InfoMessage.TRANSACTION_REQUEST)
    handler = Accounts()
    background_tasks.add_task(handler.get_transactions, session=session, customer_request=customer_request)
    return "result", 200


@app.post('/customers/requests', summary='get list of customer requests')
async def get_all_transactions(session: SessionDep, customer_id: CustomerID) -> ORJSONResponse:
    handler = CustomerTransaction(session)
    result = handler.all_requests(customer_id)
    return result


@app.post('/requests/status', summary='get status of customer request')
async def get_requests_list(request_id):
    pass


@app.post('/requests/detail', summary='get details of customer request')
async def get_requests_list(request_id):
    pass


log.setup_logger()
