import pytz
from datetime import datetime
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from boat.models import Mailing, MailingAttempt



class Command(BaseCommand):
    """Отправка рассылки"""
    def handle(self, *args, **kwargs):
        self.send_mailing()

    def send_mailing(self):
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)

        # Фильтруем рассылки по дате и статусу
        mailings = Mailing.objects.filter(first_send_time__lte=current_datetime).filter(
            status__in=[Mailing.CREATED, Mailing.STARTED]
        )

        for mailing in mailings:
            # Отправляем письмо
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()]
                )

                # Обновляем статус рассылки
                mailing.status = Mailing.COMPLETED
                mailing.save()

                # Создаем запись о попытке отправки
                MailingAttempt.objects.create(mailing=mailing, status=True, server_response="Email sent successfully")

                self.stdout.write(self.style.SUCCESS(f'Успешно отправлена рассылка ID {mailing.id}'))

            except Exception as e:
                mailing.status = Mailing.FAILED
                mailing.save()
                MailingAttempt.objects.create(mailing=mailing, status=False, server_response=str(e))
                self.stdout.write(self.style.ERROR(f'Ошибка отправки рассылки ID {mailing.id}: {e}'))

