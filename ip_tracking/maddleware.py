# ip_tracking/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class LogIPMiddleware:
    """
    Middleware that logs IP, timestamp, and path of every incoming request.
    It also checks if the IP is blacklisted, returning 403 if so.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the IP address of the client
        ip_address = request.META.get('REMOTE_ADDR')

        # Check if the IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP is blacklisted.")

        # Log the IP address, timestamp, and request path
        path = request.path
        timestamp = datetime.now()

        # Create a log entry
        RequestLog.objects.create(ip_address=ip_address, timestamp=timestamp, path=path)

        # Proceed with the request
        response = self.get_response(request)
        return response

