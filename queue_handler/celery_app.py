from celery import Celery

# Initialize Celery
celery_app = Celery(
    'queue_handler',
    broker='amqp://guest:guest@rabbitmq:5672//',  # RabbitMQ broker URL
    backend='rpc://',  # or any other result backend
    include=['queue_handler.tasks']  # Import your task modules here
)

# Optional configuration
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
