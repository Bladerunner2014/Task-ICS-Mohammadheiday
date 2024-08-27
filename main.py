from dotenv import dotenv_values
from fastapi import FastAPI
import logging
from log import log

app = FastAPI()

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


@app.get('/customers/accounts', summary='gathering customer accounts and transactions')
async def get_customers_accounts():
    pass


log.setup_logger()
