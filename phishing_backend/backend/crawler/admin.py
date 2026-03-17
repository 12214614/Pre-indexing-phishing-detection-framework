from django.contrib import admin
from .models import CrawledURL

@admin.register(CrawledURL)
class CrawledURLAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website_url",
        "status",
        "created_at",
    )

    list_filter = ("status",)
    search_fields = ("website_url",)
    ordering = ("-created_at",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
