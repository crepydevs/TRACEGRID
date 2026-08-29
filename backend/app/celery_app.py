from celery import Celery
from app.config import settings

celery_app = Celery(
    "sih26151",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)
