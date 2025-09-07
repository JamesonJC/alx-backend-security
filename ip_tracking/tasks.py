# ip_tracking/tasks.py

from celery import shared_task
from django.utils.timezone import now
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    """
    Detect suspicious IPs that have exceeded the threshold of 100 requests/hour
    or are accessing sensitive paths like /admin or /login.
    """
    one_hour_ago = now() - timedelta(hours=1)

    # Query for IPs that have made more than 100 requests in the past hour
    suspicious_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
                                        .values('ip_address') \
                                        .annotate(request_count=Count('ip_address')) \
                                        .filter(request_count__gt=100)

    # Query for IPs that accessed sensitive paths like /admin or /login
    suspicious_paths = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
                                          .filter(path__in=['/admin', '/login']) \
                                          .values('ip_address') \
                                          .annotate(request_count=Count('ip_address')) \
                                          .filter(request_count__gt=5)  # More than 5 hits on sensitive paths

    # Combine both queries
    suspicious_ips = list(suspicious_ips) + list(suspicious_paths)

    # Flag suspicious IPs
    for ip in suspicious_ips:
        ip_address = ip['ip_address']
        if not SuspiciousIP.objects.filter(ip_address=ip_address).exists():
            SuspiciousIP.objects.create(ip_address=ip_address, reason="High request count or sensitive path access")

    return f"Suspicious IPs detected: {len(suspicious_ips)}"

