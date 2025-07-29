import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Create Celery app instance
app = Celery("surveyhub")

# Load settings from Django's CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Define task routes and queues
app.conf.task_routes = {
    "core.tasks.heavy_task": {"queue": "heavy"},
    "core.tasks.light_task": {"queue": "light"},
    "core.tasks.email_task": {"queue": "email"},
}

app.conf.task_default_queue = "default"
app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("heavy", Exchange("heavy"), routing_key="heavy"),
    Queue("light", Exchange("light"), routing_key="light"),
    Queue("email", Exchange("email"), routing_key="email"),
)

# Periodic task schedule
app.conf.beat_schedule = {
    "cleanup-task": {
        "task": "core.tasks.cleanup_old_data",
        "schedule": crontab(hour=2, minute=0),
    },
    "send-daily-report": {
        "task": "core.tasks.send_daily_report",
        "schedule": crontab(hour=8, minute=30, day_of_week=1),
    },
    "health-check": {
        "task": "core.tasks.health_check",
        "schedule": 300.0,
    },
}

# Discover tasks from all registered Django app configs
app.autodiscover_tasks()


# Optional task definition (example)
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
