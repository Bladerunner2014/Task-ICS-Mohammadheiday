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
        results = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                        end_point=config["MOCK_ENDPOINT_ACCOUNTS"],
                                                        port=config["MOCK_PORT"],
                                                        timeout=config["TIMEOUT"],
                                                        error_log_dict={
                                                            "REQUEST_ERROR": ErrorMessage.MOCKSERVICE})
        if results.status_code != status.HTTP_200_OK:
            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = results.json()
        logger.info(content["data"])

        if str(customer_id.customer_id) in content["data"]:
            return ORJSONResponse(content={"message": customer_id.customer_id},
                                  status_code=status.HTTP_200_OK)

        else:
            return ORJSONResponse(content={"message": ErrorMessage.NOT_FOUND},
                                  status_code=status.HTTP_400_BAD_REQUEST)

    def get_customer_accounts(self, customer_id: CustomerID) -> ORJSONResponse:
        results = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                        end_point=config[
                                                                      "MOCK_ENDPOINT_ACCOUNTS"] + "{customer_id}".format(
                                                            customer_id=customer_id.customer_id),
                                                        port=config["MOCK_PORT"],
                                                        timeout=config["TIMEOUT"],
                                                        error_log_dict={
                                                            "message": ErrorMessage.MOCKSERVICE})
        if results.status_code != status.HTTP_200_OK:
            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = results.json()

        return ORJSONResponse(content=content,
                              status_code=status.HTTP_200_OK)

    def create_requests(self, customer_id: CustomerID, banks: list):
        request_list = []
        for i in banks:
            r = RequestData
            r.bank_name = i
            r.customer_id = customer_id
            r.error_message = "something wrong"
            r.base_url = config["MOCK_BASE"]
            r.end_point = config["MOCK_ENDPOINT_ACCOUNTS"] + "/" + "{customer_id}".format(
                customer_id=customer_id) + "/" + "{bank}".format(bank=i)
            r.e
            request_list.append(RequestData())

    def get_transactions(self, customer_id: CustomerID):
        check_existence = self.check_customer_existence(customer_id=customer_id)
        if check_existence.status_code != status.HTTP_200_OK:
            return check_existence

    def send_request_to_bank(self, customer_id: CustomerID, banks: list) -> ORJSONResponse:
        batch_request = ResponseFetcher(self.request_handler)
        response_from_banks = batch_request.fetch_responses()

        pass

    def store_transactions(self, reminder_id: str, bank: str) -> ORJSONResponse:
        pass


log.setup_logger()
