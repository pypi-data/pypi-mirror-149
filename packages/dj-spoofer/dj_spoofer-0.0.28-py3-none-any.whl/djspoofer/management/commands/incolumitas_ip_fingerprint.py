from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint, Proxy
from djspoofer.remote.incolumitas import incolumitas_api


class Command(BaseCommand):
    help = 'Get IP Fingerprint'

    def add_arguments(self, parser):
        parser.add_argument(
            "--ip_addr",
            required=False,
            type=str,
            help="Set the proxy url",
        )

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient() as client:
                r_tls = incolumitas_api.ip_fingerprint(client, ip_addr=kwargs.get('ip_addr'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TLS Fingerprint'))
