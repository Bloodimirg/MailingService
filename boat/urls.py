from django.urls import path

from boat.apps import BoatConfig
from boat.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, HomePageView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, DashboardView

app_name = BoatConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    # Клиенты urls
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    # Рассылки urls
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing-delete'),

    # Message урлы
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message-update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),

    # рассылки и письма в одном
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
