import logging
import requests
from constants.info_message import InfoMessage
from constants.error_message import ErrorMessage
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from fastapi import status
from dotenv import dotenv_values
from log import log

config = dotenv_values(".env")
logger = logging.getLogger(__name__)


class RequestHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        retries = Retry(
            total=int(config["RETRY"]),
            backoff_factor=int(config["WAIT"]),
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def send_post_request(self, base_url: str, end_point: str, port: str, body: dict, timeout: str,
                          headers: dict = None) -> (dict, int):
        """
        send_post_request sends a POST request.
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)

        try:
            response = self.session.post(
                url=f"{base_url}:{port}{end_point}",
                json=body,
                headers=default_headers,
                timeout=int(timeout)
            )
            logger.info(InfoMessage.HTTP_HANDLER + "{}".format(end_point))
            return response.json(), response.status_code

        except Exception as error:
            self.logger.error("")
            self.logger.error(error)
            return {"error": "An unknown error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def send_put_request(self, base_url: str, end_point: str, port: str, body: dict, timeout: str,
                         headers: dict = None) -> (dict, int):
        """
        send_put_request sends a PUT request.
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)

        try:
            response = self.session.put(
                url=f"{base_url}:{port}{end_point}",
                json=body,
                headers=default_headers,
                timeout=int(timeout)
            )
            logger.info(InfoMessage.HTTP_HANDLER + "{}".format(end_point))

            return response.json(), response.status_code

        except Exception as error:
            self.logger.error("")
            self.logger.error(error)
            return {"error": "An unknown error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def send_get_request(self, base_url: str, port: str, end_point: str, timeout: str,
                         params: dict = None, headers: dict = None) -> (dict, int):
        """
        send_get_request sends a GET request.
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)

        try:
            response = self.session.get(
                url=f"{base_url}:{port}{end_point}",
                params=params,
                headers=default_headers,
                timeout=int(timeout)
            )
            logger.info(InfoMessage.HTTP_HANDLER + "{}".format(end_point))

            return response.json(), response.status_code

        except Exception as error:
            self.logger.error("")
            self.logger.error(error)
            return {"error": "An unknown error occurred"}, status.HTTP_500_INTERNAL_SERVER_ERROR


log.setup_logger()
