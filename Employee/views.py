from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.db.models import Q


def homepage(request):
    return render(request,'home.html')

def EmployeeHomePage(request):
    return render(request,'employee_main_page.html')

'''
def EmployeeAdd(request):

    context={
        'employee_form':EmployeeApplication_Form()
    }

    if request.method=='POST':
        employee_form=EmployeeApplication_Form(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            
        
    return render(request,'add_employees.html',context)

'''
def EmployeeAdd(request):
    if request.method == 'POST':
        employee_form = EmployeeApplication_Form(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, 'Employee added successfully!')
            
            context = {
                'employee_form': EmployeeApplication_Form()
            }
            return render(request, 'add_employees.html', context)
        else:
            messages.error(request, 'Failed to add employee. Please check the form.')
            context = {'employee_form': employee_form} 
            return render(request, 'add_employees.html', context)

    context = {
                'employee_form': EmployeeApplication_Form()
    }
    return render(request, 'add_employees.html', context)


'''
def EmployeesView(request):
    context={
        "all_employees": EmployeeApplication.objects.all()
    }

    return render(request,'employees.html',context)
'''

def EmployeesView(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        all_employees = EmployeeApplication.objects.filter(
            Q(forenames__icontains=search_query) |
            Q(surname__icontains=search_query) |
            Q(pps_number__icontains=search_query)
        )
    else:
        all_employees = EmployeeApplication.objects.all()

    context = {
        "all_employees": all_employees
    }

    return render(request, 'employees.html', context)


def EmployeeDelete(request, id):
    selected_employee=EmployeeApplication.objects.get(id=id)
    selected_employee.delete()

    return redirect("/employee/employees/view/")


def EmployeeUpdate(request, id):
    selected_employee=EmployeeApplication.objects.get(id=id)
    

    context={
        'employee_form':EmployeeApplication_Form(instance=selected_employee)
    }
    if request.method=='POST':
        employee_form=EmployeeApplication_Form(request.POST,instance=selected_employee)

        if employee_form.is_valid():
            employee_form.save()
            return redirect("/employee/employees/view/")

    return render(request,'add_employees.html',context)


