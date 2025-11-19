from django.contrib import admin
from django.urls import path, include

from mailings.views import HomeView  # добавляем


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  # главная
    path('mailings/', include('mailings.urls', namespace='mailings')),  # подключу позже
]
