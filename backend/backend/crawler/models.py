from django.db import models

class CrawledURL(models.Model):
    website_url = models.URLField(unique=True)

    STATUS_CHOICES = [
        ("new", "New"),
        ("processed", "Processed"),
        ("pending", "Pending"),
        ("blocked", "Blocked"),
        ("legitimate", "Legitimate"),
        ("analyzed", "Analyzed"),
        ("failed", "Failed"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.website_url
