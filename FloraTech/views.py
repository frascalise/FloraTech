from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "welcome/welcome.html")

@login_required
def home_view(request):
    return render(request, "home/home.html")