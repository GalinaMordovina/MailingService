from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, ProfileForm, LoginForm
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home')  # после выхода - на главную


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user
