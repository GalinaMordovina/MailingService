from django.contrib import admin
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner")
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_datetime", "end_datetime", "status", "is_active", "owner")
    list_filter = ("status", "is_active")
    search_fields = ("message__subject",)
    # вот тут правильно:
    filter_horizontal = ("clients",)   # это ManyToManyField


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "created_at", "status")
    list_filter = ("status", "created_at")
