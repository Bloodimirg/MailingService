from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from boat.forms import StyleFormMixin
from users.models import User

class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации"""
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "avatar", "phone", "country")

class PasswordResetForm(forms.Form):
    """Форма сброса пароля"""
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}))


class PasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    """
    Форма для ввода нового пароля при восстановлении пароля.
    """
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class UserStatusForm(StyleFormMixin, forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput())
    is_banned = forms.BooleanField(label="Заблокировать", required=False)