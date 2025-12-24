from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from mailings.views import HomeView  # добавляем


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cache_page(60 * 5)(HomeView.as_view()), name='home'),  # главная: кэшируем на 5 минут
    path('mailings/', include('mailings.urls', namespace='mailings')),
    path('users/', include('users.urls')),
]
