from celery import Celery
from src.config import settings

app = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend=settings.RABBITMQ_URL,
)

app.conf.task_default_queue = settings.RABBITMQ_QUEUE
app.conf.task_default_exchange = ""
app.conf.task_default_routing_key = settings.RABBITMQ_QUEUE

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]

app.conf.task_routes = {
    "src.service.upload_image": {"queue": settings.RABBITMQ_QUEUE},
    "src.service.download_image_url": {"queue": settings.RABBITMQ_QUEUE},
}

app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True
