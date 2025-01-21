# registration/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib import messages
from django.contrib.auth import logout as django_logout




# User Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# User Login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                
                # Redirect based on the user role
                if user.role == 'Patient':
                    return redirect('patient_dashboard')  
                elif user.role == 'Doctor':
                    return redirect('doctor_dashboard') 
                elif user.role == 'Admin':
                    return redirect('admin_dashboard') 
                
                
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials!")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    django_logout(request) 
    messages.success(request, "You have been logged out.")
    return redirect('login') 