from django.core.management.base import BaseCommand

from djspoofer.clients import DesktopChromeClient
from djspoofer.remote.incolumitas import incolumitas_tls_api
from djstarter import utils


class Command(BaseCommand):
    help = 'Get TLS Fingerprint'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient() as client:
                r_tls = incolumitas_tls_api.tls_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TLS Fingerprint'))
