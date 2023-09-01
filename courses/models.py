from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/', verbose_name="Обложка", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course_id = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name="Курс")
    title = models.CharField(max_length=250, verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/', verbose_name="Обложка", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
