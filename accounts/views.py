from django.shortcuts import render

# Create your views here.
def Login(request):
    
    return render(request, 'accounts/login.html')