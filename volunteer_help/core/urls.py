from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from .swagger_urls import swagger_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += swagger_urlpatterns
