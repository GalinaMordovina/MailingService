from django.views.generic import TemplateView
# from .models import Mailing, Client  # пока их нет, позже создам

class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # пока заглушки, чтобы не падало:
        context['mailings_total'] = 0
        context['mailings_active'] = 0
        context['clients_unique'] = 0
        return context
