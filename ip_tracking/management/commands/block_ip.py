# ip_tracking/management/commands/block_ip.py

from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Block an IP address by adding it to the blacklist'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **kwargs):
        ip_address = kwargs['ip_address']
        
        # Check if the IP is already blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f"IP {ip_address} is already blocked."))
        else:
            # Block the IP by adding it to the BlockedIP model
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f"IP {ip_address} has been blocked."))

