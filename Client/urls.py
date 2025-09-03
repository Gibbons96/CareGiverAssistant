from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('clients/home/',ClientHomePage),
    path('clients/summary/',Summarizer),
    path('clients/employee_summary/',employee_summary),
    path('clients/employee_match/', match_employees, name='employee_match'),
]
