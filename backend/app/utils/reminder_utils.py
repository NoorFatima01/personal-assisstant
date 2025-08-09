from ..config.celery_app import celery_app
from ..services.reminder_services.notification_db_service import NotificationDBService
from ..services.reminder_services.email_sending_service import EmailSendingService
from ..services.user_services.user_db_service import UserDBService
from app.templates.email_templates import weekly_goal_email

notification_db_service = NotificationDBService()
user_db_service = UserDBService()

@celery_app.task
def send_weekly_goal_reminders():
    users = user_db_service.get_all_users()
    for user in users:
        notification_db_service.send_notification("Your weekly goal files upload is due!", user['email'], user['id'])
        subject, body = weekly_goal_email(user['name'], "https://upload-link.com")
        EmailSendingService.send_email(user['email'], subject, body)