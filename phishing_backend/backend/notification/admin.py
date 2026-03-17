from django.contrib import admin
from .models import NotificationLog

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_email",
        "message",
        "sent_at",
    )

    search_fields = ("user_email",)
    ordering = ("-sent_at",)
    list_per_page = 25
    date_hierarchy = "sent_at"
    readonly_fields = ("sent_at",)
