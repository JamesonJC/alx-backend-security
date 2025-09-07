# ip_tracking/middleware.py

import requests
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

        # Check cache for geolocation data
        cached_geolocation = cache.get(ip_address)
        if cached_geolocation:
            country, city = cached_geolocation
        else:
            # Get geolocation data if not cached
            country, city = self.get_geolocation(ip_address)
            # Cache the geolocation for 24 hours
            cache.set(ip_address, (country, city), timeout=86400)

        # Log the IP address, timestamp, request path, country, and city
        path = request.path
        timestamp = datetime.now()

        # Create a log entry with geolocation data
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=timestamp,
            path=path,
            country=country,
            city=city
        )

        # Proceed with the request
        response = self.get_response(request)
        return response

    def get_geolocation(self, ip_address):
        """
        Fetch the geolocation (country and city) from ipinfo.io API.
        Caches the result for 24 hours to avoid repeated requests.
        """
        try:
            # You should replace this token with your own from ipinfo.io or any other geolocation service
            token = 'e9697f45bfd94a'
            url = f'https://ipinfo.io/{myaddress.me}/json?token={token}'

            # Make the API request
            response = requests.get(url)
            data = response.json()

            # Extract the country and city
            country = data.get('country', 'Unknown')
            city = data.get('city', 'Unknown')

            return country, city
        except requests.RequestException:
            return 'Unknown', 'Unknown'

