from fastapi.responses import ORJSONResponse
from fastapi import status

from dotenv import dotenv_values
import logging
from schemas.schema import CustomerID, Bank
from log import log
from http_handler.request_handler import RequestHandler
from constants.error_message import ErrorMessage

config = dotenv_values(".env")

logger = logging.getLogger(__name__)


class Accounts:
    def __init__(self):
        self.request_handler = RequestHandler()
        pass

    def check_customer_existence(self, customer_id: CustomerID) -> ORJSONResponse:
        results = self.request_handler.send_get_request(base_url=config[""],
                                                        end_point=config["SERVICE_GET"],
                                                        port=config["AUTO_PORT"],
                                                        timeout=config["TIMEOUT"],
                                                        error_log_dict={
                                                            "message": ErrorMessage.MOCKSERVICE})
        if results.status_code != status.HTTP_200_OK:
            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = results.json()

        if customer_id.customer_id in content["data"]:
            return ORJSONResponse(content={"message": customer_id.customer_id},
                                  status_code=status.HTTP_200_OK)

        else:
            return ORJSONResponse(content={"message": ErrorMessage.NOT_FOUND},
                                  status_code=status.HTTP_400_BAD_REQUEST)

    def get_customer_accounts(self, customer_id: CustomerID) -> ORJSONResponse:
        pass

    def send_request_to_bank(self, customer_id: CustomerID, bank: Bank) -> ORJSONResponse:
        pass

    def store_transactions(self, reminder_id: str, bank: Bank) -> ORJSONResponse:
        pass


log.setup_logger()
