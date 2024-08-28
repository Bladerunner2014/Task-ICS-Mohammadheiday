import json
import logging
import requests
from fastapi import status
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from dotenv import dotenv_values

config = dotenv_values(".env")


class RequestHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @retry(
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
        stop=stop_after_attempt(int(config["RETRY"])),
        wait=wait_fixed(int(config["WAIT"]))
    )
    def send_post_request(self, base_url: str, end_point: str, port: str, body: dict, timeout: str,
                          error_log_dict: dict, headers: dict = None) -> (dict, int):
        """
        post_request send post request .

        :param headers:
        :param base_url: destination base_url
        :param end_point: destination end_point
        :param port: destination port
        :param body: request body
        :param timeout: request timeout
        :param error_log_dict: error log dictionary for specified destination service
        :return: returns the response
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        try:
            r = requests.post(url=base_url + ":" + port + end_point, data=json.dumps(body), headers=default_headers,
                              timeout=int(timeout))
        except requests.exceptions.Timeout as error:
            self.logger.error(error_log_dict["REQUEST_TIMEOUT"])
            self.logger.error(error)
            raise error
        except requests.exceptions.ConnectionError as error:
            self.logger.error(error_log_dict["CONNECTION_ERROR"])
            self.logger.error(error)
            raise error
        except Exception as error:
            self.logger.error(error_log_dict["REQUEST_ERROR"])
            self.logger.error(error)
            raise error
        if r.status_code in [status.HTTP_200_OK]:
            return r.json(), r.status_code
        else:
            return r.text, r.status_code

    @retry(
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
        stop=stop_after_attempt(int(config["RETRY"])),
        wait=wait_fixed(int(config["WAIT"]))
    )
    def send_put_request(self, base_url: str, end_point: str, port: str, body: dict, timeout: str,
                         error_log_dict: dict) -> (dict, int):
        """
        send_put_request sends put request .

        :param base_url: destination base_url
        :param end_point: destination end_point
        :param port: destination port
        :param body: request body
        :param timeout: request timeout
        :param error_log_dict: error log dictionary for specified destination service
        :return: returns the response
        """
        default_headers = {"Content-Type": "application/json"}
        try:
            r = requests.put(url=base_url + ":" + port + end_point, data=json.dumps(body), headers=default_headers,
                             timeout=int(timeout))
        except requests.exceptions.Timeout as error:
            self.logger.error(error_log_dict["REQUEST_TIMEOUT"])
            self.logger.error(error)
            raise error
        except requests.exceptions.ConnectionError as error:
            self.logger.error(error_log_dict["CONNECTION_ERROR"])
            self.logger.error(error)
            raise error
        except Exception as error:
            self.logger.error(error_log_dict["REQUEST_ERROR"])
            self.logger.error(error)
            raise error
        if r.status_code == status.HTTP_200_OK:
            return r.json(), r.status_code
        else:
            return r.text, r.status_code

    @retry(
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
        stop=stop_after_attempt(int(config["RETRY"])),
        wait=wait_fixed(int(config["WAIT"]))
    )
    def send_get_request(self, base_url: str, port: str, end_point: str, timeout: str, error_log_dict: dict,
                         params: dict = None, headers: dict = None):
        """
        send_get_request sends get request .

        :param headers:
        :param base_url: destination host
        :param port: destination port
        :param end_point: destination end point
        :param params: request params
        :param timeout: request timeout
        :param error_log_dict: error log dictionary for specified destination service
        :return: returns the response
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        try:
            r = requests.get(url=base_url + ":" + port + end_point, params=params, headers=default_headers,
                             timeout=int(timeout))
        except requests.exceptions.Timeout as error:
            self.logger.error(error_log_dict["REQUEST_TIMEOUT"])
            self.logger.error(error)
            raise error
        except requests.exceptions.ConnectionError as error:
            self.logger.error(error_log_dict["CONNECTION_ERROR"])
            self.logger.error(error)
            raise error
        except Exception as error:
            self.logger.error(error_log_dict["REQUEST_ERROR"])
            self.logger.error(error)
            raise error

        return r

    @staticmethod
    def create_json_from_args(**kwargs):
        return locals()["kwargs"]
