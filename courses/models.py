from django.db import models
from users.models import User
from config import settings

NULLABLE = {
    'blank': True,
    'null': True
}


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/', verbose_name="Обложка", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course_id = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE)
    title = models.CharField(max_length=250, verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/', verbose_name="Обложка", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    CASH = "Cash"
    ONLINE = "Online"

    PAYMENT_TYPE = (
        (CASH, "Наличные"),
        (ONLINE, "Перевод")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Плательщик')
    date = models.DateField(verbose_name='Дата оплаты', auto_now_add=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, verbose_name='Оплаченный урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default=CASH, verbose_name="Способ оплаты")

    def __str__(self):
        return f"{self.user} - {self.date} - {self.course if self.course else self.lesson} - {self.amount} - {self.payment_type}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Пользователь", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"{self.user} подписан на {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
