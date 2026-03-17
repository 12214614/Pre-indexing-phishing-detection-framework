from django.contrib import admin
from .models import VerificationRequest

@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "crawled_url",
        "final_decision",
        "created_at",
    )

    list_filter = ("final_decision",)
    ordering = ("-created_at",)
    list_per_page = 25
    readonly_fields = ("created_at",)
