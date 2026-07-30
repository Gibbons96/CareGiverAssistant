from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.db.models import Q


def homepage(request):
    return render(request, 'home.html')


def EmployeeHomePage(request):
    return render(request, 'employee_main_page.html')


def EmployeeAdd(request):

    try:
        if request.method == 'POST':
            employee_form = EmployeeApplication_Form(request.POST)

            if employee_form.is_valid():
                employee_form.save()
                messages.success(request, 'Employee added successfully!')

                context = {
                    'employee_form': EmployeeApplication_Form()
                }

            else:
                messages.error(
                    request,
                    'Failed to add employee. Please check the form.'
                )

                context = {
                    'employee_form': employee_form
                }

            return render(request, 'add_employees.html', context)

        context = {
            'employee_form': EmployeeApplication_Form()
        }

        return render(request, 'add_employees.html', context)

    except Exception as e:
        messages.error(
            request,
            f'An unexpected error occurred while adding employee: {e}'
        )

        return render(
            request,
            'add_employees.html',
            {'employee_form': EmployeeApplication_Form()}
        )


def EmployeesView(request):

    try:
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
            'all_employees': all_employees
        }

        return render(request, 'employees.html', context)

    except Exception as e:
        messages.error(
            request,
            f'Unable to load employees: {e}'
        )

        return render(
            request,
            'employees.html',
            {'all_employees': []}
        )


def EmployeeDelete(request, id):

    try:
        selected_employee = EmployeeApplication.objects.get(id=id)
        selected_employee.delete()

        messages.success(
            request,
            'Employee deleted successfully!'
        )

    except EmployeeApplication.DoesNotExist:
        messages.error(
            request,
            'Employee not found.'
        )

    except Exception as e:
        messages.error(
            request,
            f'Error deleting employee: {e}'
        )

    return redirect('/employee/employees/view/')


def EmployeeUpdate(request, id):

    try:
        selected_employee = EmployeeApplication.objects.get(id=id)

        if request.method == 'POST':
            employee_form = EmployeeApplication_Form(
                request.POST,
                instance=selected_employee
            )

            if employee_form.is_valid():
                employee_form.save()

                messages.success(
                    request,
                    'Employee updated successfully!'
                )

                return redirect('/employee/employees/view/')

            else:
                messages.error(
                    request,
                    'Please correct the errors in the form.'
                )

        else:
            employee_form = EmployeeApplication_Form(
                instance=selected_employee
            )

        context = {
            'employee_form': employee_form
        }

        return render(
            request,
            'add_employees.html',
            context
        )

    except EmployeeApplication.DoesNotExist:
        messages.error(
            request,
            'Employee not found.'
        )

        return redirect('/employee/employees/view/')

    except Exception as e:
        messages.error(
            request,
            f'Error updating employee: {e}'
        )

        return redirect('/employee/employees/view/')
