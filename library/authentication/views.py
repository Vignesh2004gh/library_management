from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:   # ✅ Only superuser can login
                login(request, user)
                return redirect('dashboard')   # After login, go to dashboard
            else:
                messages.error(request, "Only superuser can access this system.")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "authentication/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    return render(request, "dashboard.html")
