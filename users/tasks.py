import datetime

from django.utils import timezone
from celery import shared_task

from users.models import User


@shared_task
def check_user_activity():
    users = User.objects.all()
    current_time = timezone.now()
    for user in users:
        if user.last_login < current_time - datetime.timedelta(days=30):
            user.is_active = False
            user.save()
