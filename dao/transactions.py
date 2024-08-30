import logging
from typing import Optional, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import RequestAccountsInDB, TransactionInDB
from schemas.schema import RequestAccounts, Status
from db.engine import SessionLocal


from datetime import datetime
from typing import List, Dict
from db.session import SessionDep
logger = logging.getLogger(__name__)


class Transaction:
    def __init__(self) -> None:
        session = SessionLocal()

        self.db = session

    def find_request_by_id(self, request_id: Any) -> Optional[RequestAccountsInDB]:
        try:
            statement = select(RequestAccountsInDB).filter_by(id=request_id)
            user = self.db.scalars(statement).first()
            if user is None:
                logger.warning(f"No request found with ID: {request_id}")
            return user
        except Exception as e:
            logger.error(f"Error while finding request by ID {request_id}: {e}")
            # Optionally, you could re-raise the exception if you want it to be handled elsewhere
            # raise e

    def update_request(self, status: Status, request_id: str):
        # Query the specific row by request_id
        request = self.db.query(RequestAccountsInDB).filter_by(request_id=request_id).first()
        if request:
            # Update the status
            request.status = status
            self.db.commit()
        self.db.close()

    def create(self, request: RequestAccounts):
        try:
            request_data = jsonable_encoder(request)
            request_data["customer_id"] = request.customer_id.customer_id
            logger.info(f"Creating request with data: {request_data}")

            db_request = RequestAccountsInDB(**request_data)
            logger.info(f"data:{db_request}--> type: {type(db_request)}")

            return self.save(data=db_request)
        except Exception as e:
            logger.error(f"Error while creating request: {e}")
            # Optionally, you could re-raise the exception if you want it to be handled elsewhere
            # raise e

    def save(self, data):
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            # logger.info(f"Successfully saved data: {data}")
            return data
        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            # Optionally, you could roll back the transaction if needed
            # self.db.rollback()
            # raise e

    def store_transactions(self, data: List[Dict]):
        """
        Stores a list of transaction data into the database.
        :param data: List of dictionaries containing transaction data.
        """

        for entry in data:

            customer_id = entry['customer_id']
            request_id = entry['request_id']
            url = entry['url']

            for transaction in entry['response']:
                date = datetime.fromisoformat(transaction['date'])
                type = transaction['type']
                amount = transaction['amount']

                new_transaction = TransactionInDB(
                    date=date,
                    request_id=request_id,
                    customer_id=customer_id,
                    url=url,
                    amount=amount,
                    type=type
                )

                self.save(new_transaction)

    def get_all_transactions(self, customer_id: int):
        """
        Retrieve all rows from the transactions table and return them as a list of dictionaries.

        :param session: SQLAlchemy session to interact with the database.
        :return: List of dictionaries representing each row in the transactions table.
        """
        # Query all transactions
        transactions = self.db.query(TransactionInDB).filter(TransactionInDB.customer_id == customer_id).all()
        # Convert each row into a dictionary
        transactions_list = []
        for transaction in transactions:
            transaction_dict = {
                'id': transaction.id,
                'date': transaction.date,
                'request_id': transaction.request_id,
                'customer_id': transaction.customer_id,
                'url': transaction.url,
                'amount': transaction.amount,
                'type': transaction.type,
            }
            transactions_list.append(transaction_dict)

        return transactions_list

    def get_all_transactions_request(self, request_id: str):
        """
        Retrieve all rows from the transactions table and return them as a list of dictionaries.

        :param session: SQLAlchemy session to interact with the database.
        :return: List of dictionaries representing each row in the transactions table.
        """
        # Query all transactions
        transactions = self.db.query(TransactionInDB).filter(TransactionInDB.request_id == request_id).all()
        # Convert each row into a dictionary
        transactions_list = []
        for transaction in transactions:
            transaction_dict = {
                'id': transaction.id,
                'date': transaction,
                'request_id': transaction.request_id,
                'customer_id': transaction.customer_id,
                'url': transaction.url,
                'amount': transaction.amount,
                'type': transaction.type,
            }
            transactions_list.append(transaction_dict)

        return transactions_list

    def get_all_requests(self, customer_id: int):
        """
            Retrieve all rows from the customer_transaction_requests table and return them as a list of dictionaries.

            :param session: SQLAlchemy session to interact with the database.
            :return: List of dictionaries representing each row in the customer_transaction_requests table.
            """
        # Query all records from the customer_transaction_requests table
        request_accounts = self.db.query(RequestAccountsInDB).filter(TransactionInDB.customer_id == customer_id).all()

        # Convert each record into a dictionary
        request_accounts_list = []
        for request_account in request_accounts:
            request_account_dict = {
                'request_id': request_account.request_id,
                'customer_id': request_account.customer_id,
                'created_at': request_account.created_at,
                'status': request_account.status
            }
            request_accounts_list.append(request_account_dict)

        return request_accounts_list
