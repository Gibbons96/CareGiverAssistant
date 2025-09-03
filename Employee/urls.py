
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('home/',homepage),
    path('employees/home/',EmployeeHomePage),
    path('employees/add/',EmployeeAdd),
    path('employees/view/',EmployeesView),
    path('employees/delete/<int:id>/',EmployeeDelete,name='employee_delete'),
    path('employees/update/<int:id>/',EmployeeUpdate,name='employee_update'),
]
