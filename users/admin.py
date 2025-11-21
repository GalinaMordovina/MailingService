from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя."""

    model = CustomUser

    # что показывать в списке пользователей
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)

    # поля на странице редактирования пользователя
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {
            "fields": ("first_name", "last_name", "avatar", "phone", "country"),
        }),
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups"),  # user_permissions убрали
        }),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    # поля на форме создания пользователя в админке
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active",
                "groups",
            ),
        }),
    )
