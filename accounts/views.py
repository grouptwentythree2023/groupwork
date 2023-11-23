from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            print('Authenticated')
        else:
            print('Not authenticated')
        
    return render(request, 'accounts/login.html')




def logout_user(request):
    logout(request)
    
    return render()