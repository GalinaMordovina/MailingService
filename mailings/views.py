from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Client, Message, Mailing  # Attempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .services import send_mailing


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # чтобы не падало можно временно поставить "значения = 0":
        context['mailings_total'] = Mailing.objects.count()
        context['mailings_active'] = Mailing.objects.filter(status=Mailing.STATUS_STARTED).count()
        context['clients_unique'] = Client.objects.count()
        return context


# Клиенты

class ClientListView(ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


# Сообщения

class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


# Рассылки

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


def send_mailing_view(request, pk):
    """
    Запуск отправки рассылки по кнопке на странице.
    """
    mailing = get_object_or_404(Mailing, pk=pk)

    if request.method == 'POST':
        send_mailing(mailing)
        messages.success(request, 'Рассылка отправлена, попытки зафиксированы.')
        return redirect('mailings:mailing_detail', pk=pk)

    # Если вдруг зайдут GET-запросом - просто вернёмся на детали.
    return redirect('mailings:mailing_detail', pk=pk)
