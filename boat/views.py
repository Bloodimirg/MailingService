from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from boat.forms import MailingForm, MessageForm, ClientForm, BlogForm
from boat.models import Client, Mailing, Message, Blog


class HomePageView(TemplateView):
    """Главная страница"""
    template_name = 'boat/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Подсчет общего количества рассылок
        context['total_mailings'] = Mailing.objects.count()

        # Подсчет активных рассылок (например, статус "active", измените под ваши условия)
        context['active_mailings'] = Mailing.objects.filter(status__in=['created', 'started']).count()

        # Подсчет количества уникальных клиентов
        context['unique_clients'] = Client.objects.distinct().count()

        # Получение трех случайных статей из блога
        context['random_blogs'] = Blog.objects.order_by('?')[:3]

        return context


# ------------------------------------------------------------- CBV для клиентов
class ClientListView(ListView):
    """Страница списка клиентов"""
    model = Client
    template_name = 'clients/client_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Проверяем права доступа пользователя
        if user.has_perm('boat.can_view_mailings'):
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(user=user)

        context['clients'] = clients
        return context


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('boat:client-list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('boat:client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('boat:client-list')

    # CBV для рассылок


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['first_send_time', 'periodicity', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('boat:dashboard')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['first_send_time', 'periodicity', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('boat:dashboard')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('boat:dashboard')

    # CBV для писем


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'message/message_form.html'
    success_url = reverse_lazy('boat:dashboard')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'message/message_form.html'
    success_url = reverse_lazy('boat:dashboard')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/message_confirm_delete.html'
    success_url = reverse_lazy('boat:dashboard')


class DashboardView(TemplateView):
    template_name = 'boat/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context['message'] = Message.objects.all()
        return context
