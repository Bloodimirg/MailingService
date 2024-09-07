
from django.forms import BooleanField, ModelForm

from boat.models import Mailing, Message, Client, Blog


class StyleFormMixin:
    """Миксин для стилизации форм"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Присваиваем новые классы в зависимости от типа поля
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class MailingForm(StyleFormMixin, ModelForm):
    """Формы для рассылок"""
    class Meta:
        model = Mailing
        fields = ('first_send_time', 'periodicity', 'status', 'message', 'clients')


class MessageForm(StyleFormMixin, ModelForm):
    """Формы для сообщений"""
    class Meta:
        model = Message
        fields = ('subject', 'body')

class ClientForm(StyleFormMixin, ModelForm):
    """Формы для клиентов"""
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

class BlogForm(StyleFormMixin, ModelForm):
    """Формы для постов"""
    class Meta:
        model = Blog
        fields = ('title', 'body', 'image')
