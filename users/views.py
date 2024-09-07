import secrets

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, ListView

from users.forms import UserRegisterForm, PasswordResetConfirmForm, PasswordResetForm
from users.models import User
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

        send_mail(
            'Подтверждение почты',
            f'Для подтверждения регистрации пройдите по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

# подтверждение и перенаправление на страницу входа
def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetRequestView(FormView):
    """Отправка email для сброса пароля"""
    template_name = 'users/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            # Генерация токена для восстановления пароля
            token = secrets.token_hex(20)
            user.token = token
            user.save()

            reset_link = self.request.build_absolute_uri(
                reverse('users:password_reset_confirm', kwargs={'token': token})
            )

            send_mail(
                'Восстановление пароля',
                f'Для восстановления пароля перейдите по следующей ссылке: {reset_link}',
                EMAIL_HOST_USER,
                [email],
            )

        return super().form_valid(form)


class PasswordResetConfirmView(FormView):
    """Изменение пароля"""
    template_name = 'users/password_reset_confirm.html'
    form_class = PasswordResetConfirmForm
    success_url = reverse_lazy('users:password_reset_complete')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        token = self.kwargs.get('token')

        # Получение пользователя по токену
        user = get_object_or_404(User, token=token)
        kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        # Получаем пользователя из формы
        user = form.user

        # Сохраняем новый пароль
        user.set_password(form.cleaned_data['new_password1'])
        user.token = ''  # Очищаем токен после успешного сброса пароля
        user.save()

        # Перенаправление на страницу успешного сброса пароля
        return redirect(self.get_success_url())


class PasswordResetDoneView(TemplateView):
    """Отправка на почту сообщения для изменения пароля"""
    template_name = 'users/password_reset_done.html'


class PasswordResetCompleteView(TemplateView):
    """Подтверждение, что пароль изменен"""
    template_name = 'users/password_reset_complete.html'


class UsersListView(ListView):
    """Список пользователей сайта"""
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UsersDisableView(PermissionRequiredMixin, View):
    """Блокировка пользователей сервиса"""
    model = User
    permission_required = 'users.can_block_users'

    def post(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('users:users-list')
