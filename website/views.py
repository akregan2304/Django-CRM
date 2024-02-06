from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.info(request, "You have been Logged In")
            return redirect('index')
        
        else:
            messages.info(request, "Loggin error, Please check your Username/Password.")
            return redirect('index')
    
    else:
        return render(request, 'index.html')
    
def logout_user(request):
        logout(request)
        messages.info(request, "You Have Been Logged Out.....")
        return redirect('index')
    
def register_user(request):
    return render(request, 'register.html')
        