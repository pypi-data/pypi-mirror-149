from django.core.management.base import BaseCommand
from httpx import Client

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint


class Command(BaseCommand):
    help = 'Test Proxies'

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Target URL for proxies",
        )
        parser.add_argument(
            "--no-proxies",
            action='store_true',
            help="Omit proxies",
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        try:
            if kwargs['no_proxies']:
                with Client() as client:
                    client.get(url)
            else:
                fingerprint = Fingerprint.objects.random_desktop()
                with DesktopChromeClient(fingerprint=fingerprint) as client:
                    client.get(url)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
