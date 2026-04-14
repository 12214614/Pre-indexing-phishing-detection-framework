from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CrawledURL


@api_view(['POST'])
def add_url(request):

    url = request.data.get("url")

    CrawledURL.objects.create(website_url=url)

    return Response({
        "message": "URL stored successfully",
        "url": url
    })