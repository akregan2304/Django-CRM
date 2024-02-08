from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import record

# Create your views here.
def index(request):
    records = record.objects.all()
    
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
        return render(request, 'index.html',{'records':records})
    
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
        
def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up for records
        customer_record = record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.info(request, "You must login to see the result...")
        return redirect('index')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = record.objects.get(id=pk)
        delete_it.delete()
        messages.info(request, "You have deleted the data...")
        return redirect('index')
    else:
        messages.info(request, "You must login to see the result...")
        return redirect('index')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record =form.save()
                messages.info(request, "Your data saved successfully....")
                return redirect('index')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.info(request, "You must login to do this task....")
        return render(request, 'add_record.html', {'customer_record':customer_record})
    

def edit_record(request, pk):
    if request.user.is_authenticated:
        edited = record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=edited)
        if form.is_valid():
            form.save()
            messages.info(request, "Record Has Been Updated!")
            return redirect('index')
        return render(request, 'edit.html',{'form':form})
    else:
        messages.info(request, "You must login to do this task....")
        return render('index')