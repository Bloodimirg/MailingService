from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from boat.forms import MailingForm, MessageForm, ClientForm, BlogForm
from boat.models import Client, Mailing, Message, Blog
from boat.services import get_posts_from_cache


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
    """Информация об одном клиенте"""
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('boat:client-list')

    # привязываем клиента к пользователю
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Редактирование клиента"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('boat:client-list')


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('boat:client-list')


# ---------------------------------------------------------- CBV для рассылок

class MailingDetailView(DetailView):
    """Информация об одной рассылке"""
    model = Mailing
    template_name = 'mailings/mailing_detail.html'


class MailingCreateView(CreateView):
    """Создание рассылки с фильтрацией"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('boat:dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Фильтруем клиентов: показываем клиентов текущего пользователя
        form.fields['clients'].queryset = Client.objects.filter(
            user=self.request.user
        )
        # Фильтруем сообщения: показываем только сообщения текущего пользователя
        form.fields['message'].queryset = Message.objects.filter(
            user=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Редактирование рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def get_success_url(self):
        return reverse('boat:mailing-detail', args=[self.object.pk])

    # Фильтрация полей изменения рассылки по пользователям
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # если user админ = может видеть в форме редактирования всех клиентов и сообщения
        if self.request.user.is_superuser:
            form.fields['clients'].queryset = Client.objects.all()
            form.fields['message'].queryset = Message.objects.all()
            return form
        # иначе Фильтруем клиентов и сообщения только текущего пользователя
        else:
            form.fields['clients'].queryset = Client.objects.filter(
                user=self.request.user
            )
            form.fields['message'].queryset = Message.objects.filter(
                user=self.request.user
            )
            return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('boat:dashboard')


class MailingDisableView(PermissionRequiredMixin, View):
    """Отключение рассылки"""
    permission_required = 'boat.can_disable_mailings'
    raise_exception = True

    @staticmethod
    def post(**kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk'))
        mailing.status = Mailing.DISABLE  # Или другой статус, соответствующий отключению
        mailing.save()
        return redirect('boat:dashboard')


# ---------------------------------------------------------- CBV для писем
class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/message_form.html'
    success_url = reverse_lazy('boat:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
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
        user = self.request.user

        # Проверяем права доступа пользователя
        if user.has_perm('boat.can_view_mailings'):
            mailings = Mailing.objects.all()
            messages = Message.objects.all()
        else:
            mailings = Mailing.objects.filter(user=user)
            messages = Message.objects.filter(user=user)

        context['mailing'] = mailings
        context['messages'] = messages
        return context


# ---------------------------------------------------------CBV для блога

class BlogCreateView(CreateView):
    """Контроллер для добавления постов"""
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('boat:blog-list')


class BlogListView(ListView):
    """Контроллер для просмотра постов"""
    model = Blog
    template_name = 'blog/blog_list.html'
    paginate_by = 3

    def get_queryset(self):
        return get_posts_from_cache()

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    """Контроллер для изменения постов"""
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('boat:blog-list')


class BlogDeleteView(DeleteView):
    """Контроллер для удаления постов"""
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('boat:blog-list')


class BlogDetailView(DetailView):
    """Контроллер для просмотра одного поста"""
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
