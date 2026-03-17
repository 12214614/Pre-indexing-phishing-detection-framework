from django.db import models
from crawler.models import CrawledURL

class URLAnalysis(models.Model):
    crawled_url = models.OneToOneField(
        CrawledURL,
        on_delete=models.CASCADE
    )

    prediction = models.CharField(max_length=20)   # phishing / legitimate / review
    confidence_score = models.FloatField()
    reason = models.TextField(blank=True, default='')

    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crawled_url.website_url} → {self.prediction}"
