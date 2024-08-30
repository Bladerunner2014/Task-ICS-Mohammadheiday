from celery import Celery
from dotenv import dotenv_values

config = dotenv_values(".env")
host = config["RABBITMQ_HOST"]
# Initialize Celery
celery_app = Celery(
    'queue_handler',
    broker=f'amqp://guest:guest@{host}:5672//',  # RabbitMQ broker URL
    backend='rpc://',  # or any other result backend
    include=['queue_handler.tasks']  # Import your task modules here
)

# Optional configuration
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
