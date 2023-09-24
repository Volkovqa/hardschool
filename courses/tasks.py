from celery import shared_task
from config import settings
from django.core.mail import send_mail

from courses.models import Subscription, Course


@shared_task
def _send_email(course_pk):
    subscribers = Subscription.objects.filter(course=course_pk)
    course = Course.objects.filter(pk=course_pk)
    for subscriber in subscribers:
        send_mail(
            subject=f"Обновление курса {course}",
            message=f"В курс {course} добавлены новые материалы",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email],
            fail_silently=False
        )
        print(f'Сообщение отправлено {subscriber.user.email}')
