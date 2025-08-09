from celery import Celery

# Redis is running locally on port 6379, using DB 0
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # Redis as broker
    backend="redis://localhost:6379/1"  # for result storage
)

celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
        # Windows-specific settings
        worker_pool='solo',  # Use solo pool for Windows
        worker_concurrency=1,
    )

celery_app.autodiscover_tasks(['app.utils.reminder_utils', 'app.utils.doc_utils']) 


# Load periodic tasks from this file
celery_app.conf.beat_schedule = {
    "send-weekly-goal-reminders": {
        "task": "app.utils.reminder_utils.send_weekly_goal_reminders",
        "schedule": {
            "type": "crontab",   # run at 9:00 AM every Monday
            "minute": 0,
            "hour": 9,
            "day_of_week": 1
        }
    }
}

celery_app.conf.timezone = "Asia/Karachi"
