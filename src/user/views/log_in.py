from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from django.contrib.auth import authenticate,login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            # redirect based on role
            if user.role == "super_admin":
                return redirect("super_admin_dashboard")
            elif user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("client_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "general/login.html")