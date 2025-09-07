# ip_tracking/views.py

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='ALL', burst=True)
def login_view(request):
    """
    Login view that uses rate limiting.
    Limits 10 requests per minute for authenticated users.
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("You are now logged in.")
        else:
            return HttpResponse("Invalid credentials.", status=400)
    return render(request, "login.html")

@ratelimit(key='ip', rate='5/m', method='ALL', burst=True)
def anonymous_view(request):
    """
    Example of an anonymous view with rate limiting.
    Limits 5 requests per minute for anonymous users.
    """
    return HttpResponse("This is an anonymous page.")

