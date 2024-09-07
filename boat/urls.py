from django.urls import path

from boat.apps import BoatConfig
from boat.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, HomePageView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, DashboardView, MailingDisableView, \
    BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView, BlogDetailView

app_name = BoatConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    # Клиенты
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    # Рассылки
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing-delete'),
    path('mailings/<int:pk>/disable/', MailingDisableView.as_view(), name='mailing-disable'),

    # Message урлы (сообщения)
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message-update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),

    # рассылки и письма в одном dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Ведение блога модератором
    path('blog_list/', BlogListView.as_view(), name='blog-list'),
    path('blog_create/', BlogCreateView.as_view(), name='blog-create'),
    path('update_blog/<int:pk>/', BlogUpdateView.as_view(), name='blog-update'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='blog-delete'),
    path('detail_blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),

]
