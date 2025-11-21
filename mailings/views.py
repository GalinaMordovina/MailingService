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
        context['mailings_active'] = Mailing.objects.filter(status=Mailing.STATUS_STARTED, is_active=True).count()
        context['clients_unique'] = Client.objects.count()
        return context


# Клиенты

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        qs = Client.objects.all()
        user = self.request.user

        # Менеджер/админ с правом can_view_all_clients видит всех
        if user.is_superuser or user.has_perm('mailings.can_view_all_clients'):
            return qs

        # Обычный пользователь видит только своих
        return qs.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        qs = Client.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_clients'):
            return qs

        return qs.filter(owner=user)


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

    def get_queryset(self):
        qs = Client.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_clients'):
            return qs

        return qs.filter(owner=user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')

    def get_queryset(self):
        qs = Client.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_clients'):
            return qs

        return qs.filter(owner=user)


# Сообщения

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        qs = Message.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_messages'):
            return qs

        return qs.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        qs = Message.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_messages'):
            return qs

        return qs.filter(owner=user)


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

    def get_queryset(self):
        qs = Message.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_messages'):
            return qs

        return qs.filter(owner=user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_queryset(self):
        qs = Message.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_messages'):
            return qs

        return qs.filter(owner=user)


# Рассылки

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        qs = Mailing.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_mailings'):
            return qs

        return qs.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        qs = Mailing.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_mailings'):
            return qs

        return qs.filter(owner=user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'is_active', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ['start_datetime', 'end_datetime', 'status', 'is_active', 'message', 'clients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        qs = Mailing.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_mailings'):
            return qs

        return qs.filter(owner=user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        qs = Mailing.objects.all()
        user = self.request.user

        if user.is_superuser or user.has_perm('mailings.can_view_all_mailings'):
            return qs

        return qs.filter(owner=user)


# Попытки рассылок

class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user

        # Менеджер/админ с правом на рассылки видит все попытки
        if user.is_superuser or user.has_perm('mailings.can_view_all_mailings'):
            return Attempt.objects.all()

        # Обычный пользователь — только попытки по его рассылкам
        return Attempt.objects.filter(mailing__owner=user)


# Страница с отчётами по рассылкам

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'mailings/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Базовые выборки
        mailings_qs = Mailing.objects.all()
        attempts_qs = Attempt.objects.all()

        # Если нет прав видеть все рассылки, ограничиваемся своими
        if not (user.is_superuser or user.has_perm('mailings.can_view_all_mailings')):
            mailings_qs = mailings_qs.filter(owner=user)
            attempts_qs = attempts_qs.filter(mailing__owner=user)

        total_mailings = mailings_qs.count()
        active_mailings = mailings_qs.filter(status=Mailing.STATUS_STARTED, is_active=True).count()
        finished_mailings = mailings_qs.filter(status=Mailing.STATUS_FINISHED).count()

        total_attempts = attempts_qs.count()
        success_attempts = attempts_qs.filter(status=Attempt.STATUS_SUCCESS).count()
        failed_attempts = attempts_qs.filter(status=Attempt.STATUS_FAILED).count()

        context.update({
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'finished_mailings': finished_mailings,
            'total_attempts': total_attempts,
            'success_attempts': success_attempts,
            'failed_attempts': failed_attempts,
            'total_sent_emails': success_attempts,
            'is_manager_view': user.is_superuser or user.has_perm('mailings.can_view_all_mailings'),
        })
        return context


# Отправка рассылки

def send_mailing_view(request, pk):
    """
    Запуск отправки рассылки по кнопке на странице.
    """
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверка: владелец или менеджер/админ
    user = request.user
    if not (
            user.is_authenticated
            and (
                    mailing.owner == user
                    or user.is_superuser
                    or user.has_perm('mailings.can_view_all_mailings')
            )
    ):
        messages.error(request, 'У вас нет прав для отправки этой рассылки.')
        return redirect('mailings:mailing_detail', pk=pk)

    if request.method == 'POST':
        if not mailing.is_active:
            messages.error(request, 'Рассылка отключена. Сначала включите её.')
        else:
            send_mailing(mailing)
            messages.success(request, 'Рассылка отправлена, попытки зафиксированы.')

        return redirect('mailings:mailing_detail', pk=pk)

    # Если вдруг зайдут GET-запросом просто вернёмся на детали
    return redirect('mailings:mailing_detail', pk=pk)
