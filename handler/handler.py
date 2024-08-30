from fastapi.responses import ORJSONResponse
from fastapi import status
from dotenv import dotenv_values
import logging
from schemas.schema import CustomerID, RequestAccounts, Status
from log import log
from http_handler.request_handler import RequestHandler
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from http_handler.fetcher import ResponseFetcher
from dao.transactions import Transaction

config = dotenv_values(".env")

logger = logging.getLogger(__name__)


class CustomerTransaction:
    def __init__(self):
        self.transaction_dao = Transaction()

    def all_transactions(self, customer_id: CustomerID):
        res = self.transaction_dao.get_all_transactions(customer_id=customer_id.customer_id)
        return ORJSONResponse(content={"data": res},
                              status_code=status.HTTP_200_OK)

    def all_transactions_request(self, request_id: str):
        res = self.transaction_dao.get_all_transactions_request(request_id=request_id)
        return ORJSONResponse(content={"data": res},
                              status_code=status.HTTP_200_OK)

    def all_requests(self, customer_id: CustomerID):
        res = self.transaction_dao.get_all_requests(customer_id=customer_id.customer_id)
        return ORJSONResponse(content={"data": res},
                              status_code=status.HTTP_200_OK)
class Accounts:
    def __init__(self):
        self.request_handler = RequestHandler()

    def check_customer_existence(self, customer_id: CustomerID) -> ORJSONResponse:
        content, status_code = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                                     end_point=config["MOCK_ENDPOINT_ACCOUNTS"],
                                                                     port=config["MOCK_PORT"],
                                                                     timeout=config["TIMEOUT"])

        if status_code != status.HTTP_200_OK:
            logger.info(ErrorMessage.EXTERNAL_SERVICE)

            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if str(customer_id.customer_id) in content["data"]:
            return ORJSONResponse(content={"message": customer_id.customer_id},
                                  status_code=status.HTTP_200_OK)
        else:
            logger.info(ErrorMessage.NOT_FOUND)

            return ORJSONResponse(content={"message": ErrorMessage.NOT_FOUND},
                                  status_code=status.HTTP_400_BAD_REQUEST)

    def get_bank_accounts(self, customer_id: CustomerID):
        logger.info(InfoMessage.BANK_ACCOUNTS)
        results, statu_code = self.request_handler.send_get_request(base_url=config["MOCK_BASE"],
                                                                    end_point=config[
                                                                                  "MOCK_ENDPOINT_ACCOUNTS"] + "{customer_id}".format(
                                                                        customer_id=customer_id.customer_id),
                                                                    port=config["MOCK_PORT"],
                                                                    timeout=config["TIMEOUT"],
                                                                    )
        if statu_code != status.HTTP_200_OK:
            logger.info(ErrorMessage.EXTERNAL_SERVICE)

            return ORJSONResponse(content={"message": ErrorMessage.EXTERNAL_SERVICE},
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return results["data"]["banks"]

    def create_requests(self, customer_id: CustomerID, banks: list) -> list:
        logger.info(InfoMessage.PREPARING_MESSAGES)
        requests_data = []
        for bank in banks:
            req = {
                'base_url': config["MOCK_BASE"],
                'end_point': config["MOCK_ENDPOINT_ACCOUNTS"] + "{customer_id}".format(
                    customer_id=str((customer_id.customer_id)))
                             + "/" + "{bank}".format(bank=bank) + "/transactions",
                'timeout': '15',
                'port': config["MOCK_PORT"]
            }

            requests_data.append(req)
        return requests_data

    def get_transactions(self, customer_request: RequestAccounts):
        check_existence = self.check_customer_existence(customer_id=customer_request.customer_id)
        if check_existence.status_code != status.HTTP_200_OK:
            return check_existence
        self.store_request( customer_request=customer_request)
        bank_accounts = self.get_bank_accounts(customer_id=customer_request.customer_id)
        reqs = self.create_requests(customer_id=customer_request.customer_id, banks=bank_accounts)
        transactions, stat = self.send_request_to_bank(reqs, request_id=customer_request.request_id,
                                                       customer_id=int(customer_request.customer_id.customer_id))
        self.store_transactions(transactions=transactions)
        self.update_request_status( request_id=customer_request.request_id, stat=stat)
        pass

    def send_request_to_bank(self, requests: list, request_id: str, customer_id):
        response_fetcher = ResponseFetcher(self.request_handler)
        response_from_banks = response_fetcher.fetch_responses(requests_data=requests, request_id=request_id,
                                                               customer_id=customer_id)
        all_successful = response_fetcher.are_all_responses_successful(response_from_banks)
        return response_from_banks, all_successful

    def store_request(self, customer_request: RequestAccounts):
        transaction_dao = Transaction()
        logger.info(InfoMessage.STORE_TO_DB)
        transaction_dao.create(request=customer_request)

        pass

    def store_transactions(self,  transactions):
        transaction_dao = Transaction()
        logger.info(InfoMessage.STORE_TO_DB)
        transaction_dao.store_transactions(transactions)
        # logger.info(transactions)

        pass

    def update_request_status(self, request_id: str, stat):
        transaction_dao = Transaction()
        if stat:
            transaction_dao.update_request(request_id=request_id, status=Status.DONE)
        else:
            transaction_dao.update_request(request_id=request_id, status=Status.FAILED)




log.setup_logger()
