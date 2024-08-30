docker run --name test -e POSTGRES_PASSWORD=123456789 -d -p 5432:5432 postgres

docker run -d --name my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:management

alembic revision --autogenerate -m "authentication3"

alembic upgrade head

celery -A queue_handler.celery_app flower


celery -A queue_handler.celery_app worker --loglevel=info

uvicorn --reload main:app --port 8001