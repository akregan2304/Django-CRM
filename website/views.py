from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

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
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, "You have successfully registered.Welcome!")
            return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        