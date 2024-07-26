from django.contrib import admin

from boat.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("full_name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
    search_fields = ("subject", "body")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "first_send_time", "periodicity", "status", "message", "get_clients")
    search_fields = ("first_send_time",)
    list_filter = ("periodicity", "status", "message",)

    def get_clients(self, obj):
        return ", ".join([client.full_name for client in obj.clients.all()])

    get_clients.short_description = 'Клиенты'


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "attempt_time", "status", "server_response")
    search_fields = ("status",)
    list_filter = ("status", "mailing",)
