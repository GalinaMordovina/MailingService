from django.urls import path
from . import views
from django.views.decorators.cache import cache_page, cache_control


app_name = 'mailings'


urlpatterns = [
    # Клиенты
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # Сообщения
    path('messages/', cache_control(public=True, max_age=60)(views.MessageListView.as_view()), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

    # Рассылки (браузер может держать страницу до 60 сек)
    path('mailings/', cache_control(public=True, max_age=60)(views.MailingListView.as_view()), name='mailing_list'),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),

    # Попытки рассылок (кэшируем список попыток на 2 минуты)
    path('attempts/', cache_page(60 * 2)(views.AttemptListView.as_view()), name='attempt_list'),

    # Отправка рассылки вручную
    path('mailings/<int:pk>/send/', views.send_mailing_view, name='mailing_send'),
]
