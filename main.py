from dotenv import dotenv_values
from fastapi import FastAPI, BackgroundTasks
import logging
from log import log
from schemas.schema import CustomerID, RequestAccounts
from fastapi.responses import ORJSONResponse
from handler.handler import Accounts, CustomerTransaction
from queue_handler.tasks import get_transactions_task
from constants.info_message import InfoMessage
from fastapi import status


app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post('/customers/exist', summary='check existence of customer in database')
async def get_customer(customer_id: CustomerID) -> ORJSONResponse:
    handler = Accounts()
    result = handler.check_customer_existence(customer_id=customer_id)
    return result


@app.post('/customers/transaction/list', summary='retrive all customer transactions')
async def get_all_transactions(customer_id: CustomerID) -> ORJSONResponse:
    handler = CustomerTransaction()
    result = handler.all_transactions(customer_id)
    return result


@app.post('/customers/transaction/request', summary='retrive all transactions related to a request id')
async def get_all_transactions(request_id: str) -> ORJSONResponse:
    handler = CustomerTransaction()
    result = handler.all_transactions_request(request_id)
    return result


@app.post('/customers/transaction', summary='get transactions')
async def get_customers_accounts(customer_request: RequestAccounts,
                                 background_tasks: BackgroundTasks):
    logger.info(InfoMessage.TRANSACTION_REQUEST)
    get_transactions_task.delay(customer_request.dict())
    return ORJSONResponse(content={"request_id":customer_request.request_id},status_code=status.HTTP_200_OK)


@app.post('/customers/requests', summary='get list of customer requests')
async def get_all_transactions(customer_id: CustomerID) -> ORJSONResponse:
    handler = CustomerTransaction()
    result = handler.all_requests(customer_id)
    return result


@app.post('/requests/status', summary='get status of customer request')
async def get_requests_list(request_id):
    pass


@app.post('/requests/detail', summary='get details of customer request')
async def get_requests_list(request_id):
    pass


log.setup_logger()
