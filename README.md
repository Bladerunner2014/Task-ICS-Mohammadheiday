![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

## How does it works?
## Run bare metal:
Run the following command in the project root:
```bash
docker run --name test -e POSTGRES_PASSWORD=123456789 -d -p 5432:5432 postgres

docker run -d --name my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:management

alembic revision --autogenerate -m "authentication3"

alembic upgrade head

celery -A queue_handler.celery_app flower
celery -A queue_handler.celery_app worker --loglevel=info

uvicorn --reload main:app --port 8001
```
edit .env
```bash
#MOCKSERVICE
MOCK_BASE= "http://0.0.0.0"
MOCK_ENDPOINT_ACCOUNTS="/customers/"
MOCK_PORT = 8000
```

```
**Note:**

# License
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


