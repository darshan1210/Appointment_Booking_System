from celery import shared_task
from celery.utils.log import get_task_logger
from app.background.celery_app import celery_app

logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    max_retries=3,
    name="app.celery_app.tasks.notifications.send_booking_confirmation",
    queue="critical"
)
def send_booking_confirmation(self,appointment_id: int):
    try:
        """ Make DB query on new booking """
        logger.info(f"[CONFIRM] Sent for appointment {appointment_id}")
        return {"status": "sent", "appointment_id": appointment_id}
    except Exception as exc:
        logger.warning(f"Retry {self.request.retries}/3 for appt {appointment_id}")
        raise self.retry(exec=exec,countdown= 2 ** self.request.retries * 30)
