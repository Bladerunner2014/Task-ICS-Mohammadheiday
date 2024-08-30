from celery import shared_task
from handler.handler import Accounts
from schemas.schema import RequestAccounts

@shared_task
def get_transactions_task(customer_request_data):
    handler = Accounts()
    req = RequestAccounts(**customer_request_data)

    handler.get_transactions(customer_request=req)
