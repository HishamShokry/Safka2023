from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')

def signupMarketer(request):
    msg = None
    if request.method == 'POST':
        form = SignUpFormMarketer(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_marketer = True
            user.save()
            msg = 'User Created'
            return redirect('signin')
        else:
            msg = 'Form is not Valid!'
    else:
        form = SignUpFormMarketer()
    return render(request, 'signupMarketer.html', {'form': form, 'msg': msg})



def signupVendor(request):
    msg = None
    if request.method == 'POST':
        form = SignUpFormVendor(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_vendor = True
            user.save()
            msg = 'User Created'
            return redirect('signin')
        else:
            msg = 'Form is not Valid!'
    else:
        form = SignUpFormVendor()
    return render(request, 'signupVendor.html', {'form': form, 'msg': msg})


def signin(request):
    form = SignInForm
    msg = None
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
            if user is not None:    
                login(request, user)
                if user.is_admin:
                    return redirect('dashboard')
                elif user.is_vendor:
                    return redirect('vendor_dashboard')
                elif user.is_marketer:
                    return redirect('marketer_dashboard')
                else:
                    return redirect('dashboard')
        else:
            msg = 'البريد الاكتروني او كلمة السر غير صحيحة'
    
    return render(request, 'signin.html', {'form': form, 'msg': msg})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')








