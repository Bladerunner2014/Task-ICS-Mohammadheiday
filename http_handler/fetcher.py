import logging
from fastapi import status
from http_handler.request_handler import RequestHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
from log import log

logger = logging.getLogger(__name__)


class ResponseFetcher:
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
        self.logger = logger

    def fetch_responses(self, requests_data: list):
        responses = []
        with ThreadPoolExecutor(max_workers=len(requests_data)) as executor:
            future_to_request = {
                executor.submit(self._fetch_response, data): data
                for data in requests_data
            }
            for future in as_completed(future_to_request):
                request_data = future_to_request[future]
                try:
                    response, status_code = future.result()
                    responses.append(self._process_response(request_data, response, status_code))
                except Exception as exc:
                    responses.append(self._handle_error(request_data, exc))
        return responses

    def _fetch_response(self, request_data):
        return self.request_handler.send_get_request(**request_data)

    def _process_response(self, request_data, response, status_code):
        return {
            'url': request_data['base_url'] + ":" + request_data['port'] + request_data['end_point'],
            'status_code': status_code,
            'response': response
        }

    def _handle_error(self, request_data, exc):
        return {
            'url': request_data['base_url'] + ":" + request_data['port'] + request_data['end_point'],
            'status_code': None,
            'response': str(exc)
        }

    def are_all_responses_successful(self, responses):
        return all(resp['status_code'] == status.HTTP_200_OK for resp in responses)


log.setup_logger()
