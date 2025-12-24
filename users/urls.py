from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('manage/', views.user_list_view, name='user_list'),
    path('manage/<int:pk>/toggle/', views.toggle_user_active_view, name='user_toggle'),
]
