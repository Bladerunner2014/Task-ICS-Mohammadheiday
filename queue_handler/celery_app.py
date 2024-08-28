from celery import Celery


class CeleryAppFactory:
    def __init__(self, name, broker_url, backend_url):
        self.name = name
        self.broker_url = broker_url
        self.backend_url = backend_url

    def create_celery_app(self):
        capp = Celery(
            self.name,
            broker=self.broker_url,
            backend=self.backend_url,
        )

        # Optional configuration
        capp.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
        )

        return capp

# # Example usage:
# if __name__ == "__main__":
#     # Create an instance of the factory
#     factory = CeleryAppFactory(
#         name='tasks',
#         broker_url='pyamqp://guest@localhost//',
#         backend_url='redis://localhost:6379/0'
#     )
#
#     # Create the Celery app using the factory
#     celery_app = factory.create_celery_app()
