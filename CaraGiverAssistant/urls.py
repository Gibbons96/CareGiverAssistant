
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', include('Employee.urls')),
    path('client/', include('Client.urls')),
    path('',include('authentication.urls')),
]
