from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("image-surveillance")  # Redirect after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect("index")  
