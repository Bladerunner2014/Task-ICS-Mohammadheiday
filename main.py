from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log
from schemas.schema import CustomerID
from fastapi.responses import ORJSONResponse
from handler.handler import Accounts

app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post('/customers/exist', summary='check existence of customer in database')
async def get_customer(customer_id: CustomerID) -> ORJSONResponse:
    handler = Accounts()
    result = handler.check_customer_existence(customer_id=customer_id)
    return result


@app.post('/customers/accounts', summary='gathering customer accounts and transactions')
async def get_customers_accounts(customer_id: CustomerID) -> ORJSONResponse:
    handler = Accounts()
    result = handler.get_customer_accounts(customer_id=customer_id)
    return result


@app.post('/customers/requests', summary='get list of customer requests')
async def get_requests_list(customer_id: CustomerID):
    pass


@app.post('/requests/status', summary='get status of customer request')
async def get_requests_list(request_id):
    pass


@app.post('/requests/detail', summary='get details of customer request')
async def get_requests_list(request_id):
    pass


log.setup_logger()
