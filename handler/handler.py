from fastapi.responses import ORJSONResponse
from dotenv import dotenv_values
import logging
from schemas.schema import CustomerID, Bank
from log import log

config = dotenv_values(".env")

logger = logging.getLogger(__name__)


class AccountsHandler:
    def __init__(self):
        pass

    def check_customer_existence(self, customer_id: CustomerID) -> ORJSONResponse:

        pass

    def get_customer_accounts(self, customer_id: CustomerID) -> ORJSONResponse:
        pass

    def send_request_to_bank(self, customer_id: CustomerID, bank: Bank) -> ORJSONResponse:
        pass

    def store_transactions(self, reminder_id: str, bank: Bank) -> ORJSONResponse:
        pass


log.setup_logger()
