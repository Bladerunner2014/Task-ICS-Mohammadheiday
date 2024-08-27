from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log

app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.post('/customers/accounts', summary='gathering customer accounts and transactions')
async def get_customers_accounts(customer_id):
    pass


@app.post('/customers/requests', summary='get list of customer requests')
async def get_requests_list(customer_id):
    pass




log.setup_logger()
