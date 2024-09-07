from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name="Название"
                             )
    body = models.TextField(max_length=150, verbose_name="Содержимое")
    image = models.ImageField(upload_to="boat/photo", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    user = models.ForeignKey(User, verbose_name='Владелец', help_text="Укажите владельца", **NULLABLE,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Контактный email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    user = models.ForeignKey(User, verbose_name='Владелец', help_text="Укажите владельца", **NULLABLE,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Модель Сообщения для рассылки
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержимое письма")

    user = models.ForeignKey(User, verbose_name='Владелец', help_text="Укажите владельца", **NULLABLE,
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


# Модель Рассылки
class Mailing(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    PERIODICITY_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    FAILED = 'failed'
    DISABLE = 'disable'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (COMPLETED, 'Завершена'),
        (FAILED, 'Неудачно'),
        (DISABLE, 'Отключена модератором')
    ]

    first_send_time = models.DateTimeField(verbose_name="Дата и время первой отправки в формате 'YYYY-MM-DD HH:MM'")
    periodicity = models.CharField(max_length=7, choices=PERIODICITY_CHOICES, verbose_name="Периодичность")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус")
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    user = models.ForeignKey(User, verbose_name='Владелец', help_text="Укажите владельца", **NULLABLE, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status", "first_send_time"]
        permissions = [('can_view_mailings', 'Can view mailings'),
                       ('can_disable_mailings', 'Can disable mailings'),
                       ]

    def __str__(self):
        return f"Рассылка {self.id} - {self.status}"


# Модель Попытки рассылки
class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.BooleanField(verbose_name="Статус попытки")  # True - успешно, False - не успешно
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f"Attempt {self.id} for Mailing {self.mailing.id}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
