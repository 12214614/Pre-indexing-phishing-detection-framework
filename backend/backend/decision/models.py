from django.db import models
from crawler.models import CrawledURL

class VerificationRequest(models.Model):

    DECISION_CHOICES = [
        ("legitimate", "Legitimate"),
        ("phishing", "Phishing"),
        ("review", "Needs Review"),
    ]

    crawled_url = models.ForeignKey(
        CrawledURL,
        on_delete=models.CASCADE,
        related_name="verification_requests"
    )

    requested_document = models.TextField(blank=True, null=True)

    final_decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES,
        default="review"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crawled_url.website_url} → {self.final_decision}"
