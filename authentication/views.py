from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def LoginPage(request):
    context = {
        "error": ""
    }

    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('/employee/home/')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Basic validation
        if not username or not password:
            context["error"] = "*All fields are required"
            return render(request, 'login.html', context)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/employee/home/')
        else:
            context["error"] = "*Invalid username or password"

    return render(request, 'login.html', context)


def LogoutUser(request):
    logout(request)
    return redirect('/')


def SignupUser(request):

    context = {
        "error": ""
    }

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Validation
        if not all([username, first_name, last_name, email, password]):
            context["error"] = "*All fields are required"
            return render(request, 'signup.html', context)

        # Check username
        if User.objects.filter(username=username).exists():
            context["error"] = "*Username already exists!"
            return render(request, 'signup.html', context)

        # Check email
        if User.objects.filter(email=email).exists():
            context["error"] = "*Email already registered!"
            return render(request, 'signup.html', context)

        # Password length validation
        if len(password) < 6:
            context["error"] = "*Password must be at least 6 characters"
            return render(request, 'signup.html', context)

        # Create user
        new_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        new_user.save()

        return redirect('/')

    return render(request, 'signup.html', context)
