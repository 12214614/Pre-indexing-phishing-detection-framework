from rest_framework import serializers
from crawler.models import CrawledURL
from analysis.models import URLAnalysis
from decision.models import VerificationRequest


class CrawledURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawledURL
        fields = "__all__"


class URLAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLAnalysis
        fields = "__all__"


class VerificationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = "__all__"
