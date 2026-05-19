from celery import Celery
from celery.schedules import crontab
from kombu import Queue
from app.core.config import get_settings

settings = get_settings()

# ── Create Celery instance ───────────────────────────────
celery_app = Celery(settings.PROJECT_NAME)

celery_app.conf.update(
    # Broker & Backend
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,

    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,

    # Reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,

    # Default Queue
    task_default_queue="notifications",

    # Queue Definitions
    task_queues=(
        Queue(
            "critical",
            routing_key="critical",
        ),
        Queue(
            "notifications",
            routing_key="notifications",
        ),
        Queue(
            "reminders",
            routing_key="reminders",
        ),
        Queue(
            "cleanup",
            routing_key="cleanup",
        ),
    ),

    # Task Routing
    task_routes={
        "app.celery_app.tasks.notifications.send_booking_confirmation": {
            "queue": "critical",
            "routing_key": "critical",
        },

        # Example routes
        "app.tasks.notifications.*": {
            "queue": "notifications",
            "routing_key": "notifications",
        },

        "app.tasks.reminders.*": {
            "queue": "reminders",
            "routing_key": "reminders",
        },

        "app.tasks.cleanup.*": {
            "queue": "cleanup",
            "routing_key": "cleanup",
        },
    },
)

