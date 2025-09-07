# ip_tracking/middleware.py

from datetime import datetime
from .models import RequestLog

class LogIPMiddleware:
    """
    Middleware that logs IP, timestamp, and path of every incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the IP address, timestamp, and request path
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        timestamp = datetime.now()

        # Create a log entry
        RequestLog.objects.create(ip_address=ip_address, timestamp=timestamp, path=path)

        # Proceed with the request
        response = self.get_response(request)
        return response
