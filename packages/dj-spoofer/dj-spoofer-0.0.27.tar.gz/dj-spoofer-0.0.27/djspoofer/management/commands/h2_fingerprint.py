from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint
from djspoofer.remote.h2fingerprint import h2fingerprint_api


class Command(BaseCommand):
    help = 'Get H2 Fingerprint'

    def handle(self, *args, **kwargs):
        try:
            fingerprint = Fingerprint.objects.random_desktop()
            with DesktopChromeClient(fingerprint=fingerprint) as client:
                r_h2 = h2fingerprint_api.get_h2_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_h2))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting H2 Fingerprint'))
