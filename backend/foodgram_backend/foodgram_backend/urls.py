from django.contrib import admin
from django.urls import re_path, path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api'))
]
