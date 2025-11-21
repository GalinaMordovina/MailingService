from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Client, Message, Mailing, Attempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .services import send_mailing
from django.contrib.auth.mixins import LoginRequiredMixin


def is_manager(user):  # проверка роли пользователя
    return user.is_authenticated and user.groups.filter(name='Менеджеры').exists()


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

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        qs = Client.objects.all()
        if is_manager(self.request.user):
            return qs
        return qs.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        qs = Client.objects.all()
        if is_manager(self.request.user):
            return qs
        return qs.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


# Сообщения

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        qs = Message.objects.all()
        if is_manager(self.request.user):
            return qs
        return qs.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


# Рассылки

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        qs = Message.objects.all()
        if is_manager(self.request.user):
            return qs
        return qs.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


# Попытки рассылок

class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user

        # Менеджеры видят все попытки
        if user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return Attempt.objects.all()

        # Обычный пользователь только свои
        return Attempt.objects.filter(mailing__owner=user)


# Отправка рассылки

def send_mailing_view(request, pk):
    """
    Запуск отправки рассылки по кнопке на странице.
    """
    mailing = get_object_or_404(Mailing, pk=pk)

    # позже добавить проверку, что mailing.owner == request.user или что пользователь менеджер/админ

    if request.method == 'POST':
        send_mailing(mailing)
        messages.success(request, 'Рассылка отправлена, попытки зафиксированы.')
        return redirect('mailings:mailing_detail', pk=pk)

    # Если вдруг зайдут GET-запросом - просто вернёмся на детали.
    return redirect('mailings:mailing_detail', pk=pk)
