from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def LoginPage(request):
    context={
        "error":""
    }
    if request.method=='POST':
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            
            return redirect('/employee/home/')
        else:
            context={
                "error":"*Invalid username or password"
            }
            return render(request,'login.html',context)

        
    return render(request,'login.html',context)

def LogoutUser(request):
    logout(request)
    return redirect('/')

def SignupUser(request):

    context={
        "error":""
    }

    if request.method=='POST':

        user_check=User.objects.filter(username=request.POST['username'])

        if len(user_check)>0:
            context={
                "error":"*Username already exists!"
            }
            return render(request,'signup.html',context)

        else:
            new_user=User(username=request.POST['username'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'])
            new_user.set_password(request.POST['password'])

            new_user.save()
            return redirect('/')

    return render(request,'signup.html',context)
