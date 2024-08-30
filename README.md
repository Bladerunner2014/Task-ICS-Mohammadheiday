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
کاربر یک درخواست در /request ثبت میکنه این در خواست میره تو صف پردازش توی rabbitmq . موقع پردازش ۱۰ تا thread باز میشه و برای هر بانک ریکوءست میفرسته. در صورتی که هر کدوم از ریکوءست ها فیل بشن تا ۲ بار retry صورت میگیره. اگه تمام ریکوءست ها با موفقیت انجام بشن وضعیت ریکوءست به done تغییر میکنه.
آدرس /request/list وضعیت تمام ریکوءست هایی که کاربر فرستاده رو نمایش میده.
برای راحتی کار من authentication رو برداشتم ولی با اضافه کردن CurrentUser به تابع هر API باید اطلاعات کاربر همراه ریکوءست فرستاده بشه.
آدرس /amount باقی مانده حساب به همراه تراکنش ها رو نمایش میده. تو این API از Caching with Redis استفاده شده.
پروژه داکرایز شده ولی یه ایراد داشت اونم این بود که داده ها تو دیتابیس ذخیره نمیشدن. بهتر بود سیستم  
## Run bare metal:
Run the following command in the project root:
```bash
docker run --name test -e POSTGRES_PASSWORD=123456789 -d -p 5432:5432 postgres
```
```bash

docker run --name my-redis -d -p 6379:6379 -e REDIS_PASSWORD=kTfmjCzLLSgFnyw2OoGw redis
```
```bash
docker run -d --name my-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:management
```
```bash
alembic revision --autogenerate -m "authentication3"
```
```bash
alembic upgrade head
```
```bash
celery -A queue_handler.celery_app worker --loglevel=info

```
```bash
celery -A queue_handler.celery_app flower

```

```bash
uvicorn --reload main:app --port 8001

```


edit .env to MockService config
```bash
#MOCKSERVICE
MOCK_BASE= "http://0.0.0.0"
MOCK_ENDPOINT_ACCOUNTS="/customers/"
MOCK_PORT = 8000
```

```
**Note:**
I could not dockerize whole project!
# License
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


