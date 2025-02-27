# Generated by Django 4.2.2 on 2024-09-03 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Контактный email')),
                ('full_name', models.CharField(max_length=255, verbose_name='Ф.И.О')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_send_time', models.DateTimeField(verbose_name='Дата и время первой отправки')),
                ('periodicity', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=7, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена'), ('failed', 'Неудачно'), ('disable', 'Отключена модератором')], default='created', max_length=9, verbose_name='Статус')),
                ('clients', models.ManyToManyField(to='boat.client', verbose_name='Клиенты')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['status', 'first_send_time'],
                'permissions': [('can_view_mailings', 'Can view mailings'), ('can_disable_mailings', 'Can disable mailings')],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Содержимое письма')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')),
                ('status', models.BooleanField(verbose_name='Статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boat.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='boat.message', verbose_name='Сообщение'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Укажите владельца', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
