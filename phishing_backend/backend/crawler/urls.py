from django.urls import path
from .views import add_url

urlpatterns = [
    path("add-url/", add_url),
]