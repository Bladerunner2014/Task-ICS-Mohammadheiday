from celery_app import CeleryAppFactory
from celery import Task
from typing import Callable, Any
from log import log
import logging

logger = logging.getLogger(__name__)

capp = CeleryAppFactory().create_celery_app()


class MyTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} failed due to {exc}. Retrying...")


@capp.task(bind=True, base=MyTask, max_retries=3)
def task_runner(self, func: Callable[[Any], bool], *args, **kwargs):
    try:
        # Log the start of the task
        logger.info(f"Starting task {self.request.id} with arguments: {args}, {kwargs}")

        # Call the provided function with the given arguments
        result = func(*args, **kwargs)

        # Log the success of the task
        if result:
            logger.info(f"Task {self.request.id} completed successfully.")
            return True
        else:
            logger.warning(f"Task {self.request.id} failed during execution.")
            raise ValueError("Task failed")

    except Exception as exc:
        # Log the exception
        logger.error(f"Task {self.request.id} encountered an error: {exc}")

        # Define retry intervals: 30 minutes, 6 hours, 24 hours (in seconds)
        retry_intervals = [30 * 60, 6 * 60 * 60, 24 * 60 * 60]  # [1800, 21600, 86400] seconds

        # Determine the delay for the next retry based on the current retry count
        try:
            retry_delay = retry_intervals[self.request.retries]
        except IndexError:
            logger.error(f"Task {self.request.id} exceeded max retries.")
            return False

        # Retry the task with the calculated delay
        raise self.retry(exc=exc, countdown=retry_delay)


log.setup_logger()

# def http_processor(content: str, should_fail: bool = False) -> bool:
#     # Simulate some processing logic
#     logger.info(f"Processing HTTP request with content: {content}")
#
#     # Simulate failure condition
#     if should_fail:
#         logger.warning("Simulated failure in http_processor")
#         return False
#
#     # Return True if successful
#     logger.info("http_processor completed successfully")
#     return True
