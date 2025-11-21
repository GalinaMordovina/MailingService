from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required


from .forms import SignUpForm, ProfileForm, LoginForm
from .models import CustomUser
from .utils import is_manager


User = get_user_model()


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


@user_passes_test(is_manager)
def user_list_view(request):
    """Страница со списком всех пользователей для менеджера."""
    users = User.objects.all().order_by('email')
    return render(request, 'users/user_list.html', {'users': users})


@user_passes_test(is_manager)
def toggle_user_active_view(request, pk):
    """
    Менеджер включает/выключает is_active пользователю.
    Работает только по POST.
    """
    user_obj = get_object_or_404(User, pk=pk)

    # не даём менеджеру заблокировать сам себя
    if user_obj == request.user:
        # просто вернёмся назад
        return redirect('users:user_list')

    if request.method == 'POST':
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        return redirect('users:user_list')

    # на GET просто редиректим на список
    return redirect('users:user_list')
