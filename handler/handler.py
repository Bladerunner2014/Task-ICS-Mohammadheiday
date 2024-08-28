from fastapi.responses import ORJSONResponse
from fastapi import status
from dotenv import dotenv_values
import logging
from schemas.schema import CustomerID, RequestData
from log import log
from http_handler.request_handler import RequestHandler
from constants.error_message import ErrorMessage
from http_handler.fetcher import ResponseFetcher

config = dotenv_values(".env")

logger = logging.getLogger(__name__)


class Accounts:
    def __init__(self):
        self.request_handler = RequestHandler()

    def check_customer_existence(self, customer_id: CustomerID) -> ORJSONResponse:
        content, status_code = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                                     end_point=config["MOCK_ENDPOINT_ACCOUNTS"],
                                                                     port=config["MOCK_PORT"],
                                                                     timeout=config["TIMEOUT"])

        if status_code != status.HTTP_200_OK:
            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if str(customer_id.customer_id) in content["data"]:
            return ORJSONResponse(content={"message": customer_id.customer_id},
                                  status_code=status.HTTP_200_OK)
        else:
            return ORJSONResponse(content={"message": ErrorMessage.NOT_FOUND},
                                  status_code=status.HTTP_400_BAD_REQUEST)

    def get_customer_accounts(self, customer_id: CustomerID):
        results, statu_code = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                                    end_point=config[
                                                                                  "MOCK_ENDPOINT_ACCOUNTS"] + "{customer_id}".format(
                                                                        customer_id=customer_id.customer_id),
                                                                    port=config["MOCK_PORT"],
                                                                    timeout=config["TIMEOUT"],
                                                                    )
        if statu_code != status.HTTP_200_OK:
            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return results["data"]["banks"]

    def create_requests(self, customer_id: CustomerID, banks: list) -> list:
        requests_data = [
            {
                'base_url': config["MOCK_BASE"],
                'end_point': config["MOCK_ENDPOINT_ACCOUNTS"] + "4828128514"
                             + "/" + "melli" + "/transactions",
                'timeout': '15',
                'port': config["MOCK_PORT"],
            },
            {
                'base_url': config["MOCK_BASE"],
                'end_point': config["MOCK_ENDPOINT_ACCOUNTS"] + "4828128514"
                             + "/" + "mellat" + "/transactions",
                'timeout': '15',
                'port': config["MOCK_PORT"],

            },
            {
                'base_url': config["MOCK_BASE"],
                'end_point': config["MOCK_ENDPOINT_ACCOUNTS"] + "4828128514"
                             + "/" + "saderat" + "/transactions",
                'timeout': '15',
                'port': config["MOCK_PORT"],
            },
            {
                'base_url': config["MOCK_BASE"],
                'end_point': config["MOCK_ENDPOINT_ACCOUNTS"] + "4828128514"
                             + "/" + "tejarat" + "/transactions",
                'timeout': '15',
                'port': config["MOCK_PORT"],

            }
            # Add more requests as needed
        ]
        return requests_data

    # def get_transactions(self, customer_id: CustomerID):
    #     check_existence = self.check_customer_existence(customer_id=customer_id)
    #     if check_existence.status_code != status.HTTP_200_OK:
    #         return check_existence

    def send_request_to_bank(self, requests: list):
        response_fetcher = ResponseFetcher(self.request_handler)
        response_from_banks = response_fetcher.fetch_responses(requests_data=requests)
        all_successful = response_fetcher.are_all_responses_successful(response_from_banks)
        logger.info("@@@@@@@@@@@{}".format(all_successful))
        return response_from_banks

    def store_transactions(self, reminder_id: str, bank: str) -> ORJSONResponse:
        pass


log.setup_logger()
