from celery import shared_task
from datetime import date, timedelta

@shared_task(
    queue='reminders',
    name='tasks.reminders.send_appointment_reminder'
)
def send_appointment_reminder():
    """Fetch tomorrow's appointments and dispatch reminders."""
    tomorrow = date.today() + timedelta(days=1)
    # appointments = Appointment.objects.filter(
    #     date=tomorrow,
    #     status='confirmed',
    #     reminder_sent=False
    # )
    dispatched = 0
    # for appt in appointments:
    #     send_email_notification.delay(
    #         recipient=appt.patient_email,
    #         subject="Reminder: Your appointment is tomorrow",
    #         body=render_reminder_template(appt),
    #     )
    #     if appt.patient_phone:
    #         send_sms_notification.delay(
    #             phone_number=appt.patient_phone,
    #             message=f"Reminder: Appointment on {appt.date} at {appt.time}",
    #         )
    #     appt.reminder_sent = True
    #     appt.save(update_fields=['reminder_sent'])
    #     dispatched += 1

    return {'reminders_sent': dispatched, 'date': str(tomorrow)}
@shared_task(
    bind=True,
    queue='reminders',
    name='tasks.reminders.schedule_dynamic_reminder'
)
def schedule_dynamic_reminder(self,appointment_id: int, remind_before_hours: int = 2):
    """ Schedule a one-off reminder ETA'd to N hours before the appointment """
    from datetime import datetime, timedelta
    # appt = Appointment.
    # Change datetime to appointment date time
    remind_at = datetime.combine(datetime.now(), datetime.time()) - timedelta(hours= remind_before_hours)

    send_appointment_reminder.apply_async(
        args=[appointment_id],
        eta=remind_at,
        queue='reminders'
    )
    return {'scheduled_at': str(remind_at)}