from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Client # Mailing пока его нет, позже создам


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # пока заглушки, чтобы не падало:
        context['mailings_total'] = 0
        context['mailings_active'] = 0
        context['clients_unique'] = 0
        return context


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