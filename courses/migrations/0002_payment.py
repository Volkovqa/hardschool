# Generated by Django 4.2.4 on 2023-09-05 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата оплаты')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма оплаты')),
                ('payment_type', models.CharField(choices=[('Cash', 'Наличные'), ('Online', 'Перевод')], default='Cash', max_length=10, verbose_name='Способ оплаты')),
                ('course_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course', verbose_name='Оплаченный курс')),
                ('lesson_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.lesson', verbose_name='Оплаченный урок')),
                ('user_id', models.ForeignKey(on_delete=models.SET('deleted'), to=settings.AUTH_USER_MODEL, verbose_name='Плательщик')),
            ],
        ),
    ]
