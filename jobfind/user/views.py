from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from . models import *
from jobseeker.views import *
from employer.views import *


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'login.html')
        else:
            print(form.errors)
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    # return render(request,'signup.html')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            # return render(request,'home.html')
            if user.user_type == 'JOB_SEEKER':
                return redirect('seekerdash')
            else:
                return redirect('regemp')
        else:
            return render(request,'login.html')
    return render(request, 'login.html')


def home_view(request):
    return render(request,'home.html')

def viewadminlogin(request):
    return render(request,'admin_login.html')

def admindash(request):
    return render(request,'admin_dash.html')

def admin_login(request):
    if request.method == 'POST':
        ad_uname = "admin1"
        ad_password = "admin@123"
        name = request.POST['name']
        password = request.POST['password']
        if name == ad_uname and password == ad_password:
            return redirect('admin_dash')
        
        else:
            return redirect('admin_login_page')
        
def view_employer(request):
    pass