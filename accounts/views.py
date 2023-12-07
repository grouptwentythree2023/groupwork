from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(username, password)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfull')
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, 'Invalid username or password')
        
    return render(request, 'accounts/login.html')




def logout_user(request):
    logout(request)
    return redirect(reverse('login'))
    