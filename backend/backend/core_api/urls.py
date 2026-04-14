from django.urls import path
from .views import SubmitURLAPIView, URLListAPIView, DashboardAPIView

urlpatterns = [
    path("submit-url/", SubmitURLAPIView.as_view(), name="submit-url"),
    path("url-list/", URLListAPIView.as_view(), name="url-list"),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]
