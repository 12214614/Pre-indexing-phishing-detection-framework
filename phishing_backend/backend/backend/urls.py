from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def home(request):
    return HttpResponse(
        """
        <h1>PIPPF Backend is running</h1>
        <p>Frontend: <a href=\"http://localhost:3100\">http://localhost:3100</a></p>
        <p>Admin: <a href=\"/admin/\">/admin/</a></p>
        <p>API: <a href=\"/api/core/dashboard/\">/api/core/dashboard/</a></p>
        """
    )

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('crawler.urls')),
    path('api/core/', include('core_api.urls')),
]