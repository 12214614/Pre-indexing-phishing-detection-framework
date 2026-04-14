from django.contrib import admin
from .models import URLAnalysis


@admin.register(URLAnalysis)
class URLAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_website_url",
        "prediction",
        "confidence_score",
        "analyzed_at",
    )

    list_filter = ("prediction",)
    search_fields = ("crawled_url__website_url",)
    ordering = ("-analyzed_at",)
    list_per_page = 25
    date_hierarchy = "analyzed_at"
    readonly_fields = ("analyzed_at",)

    def get_website_url(self, obj):
        return obj.crawled_url.website_url

    get_website_url.short_description = "Website URL"
