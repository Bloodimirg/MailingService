from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Контактный email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Модель Сообщения для рассылки
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Содержимое письма")

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
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    first_send_time = models.DateTimeField(verbose_name="Дата и время первой отправки")
    periodicity = models.CharField(max_length=7, choices=PERIODICITY_CHOICES, verbose_name="Периодичность")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус")
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    def __str__(self):
        return f"Рассылка {self.id} - {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


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
