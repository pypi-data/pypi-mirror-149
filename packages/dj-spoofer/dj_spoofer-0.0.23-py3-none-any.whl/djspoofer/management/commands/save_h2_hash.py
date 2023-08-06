from django.core.management.base import BaseCommand

from djspoofer.models import H2Fingerprint
from djspoofer import utils


class Command(BaseCommand):
    help = 'Save H2 Hash'

    def add_arguments(self, parser):
        parser.add_argument(
            "--hash",
            required=True,
            type=str,
            help="H2 Fingerprint Hash",
        )
        parser.add_argument(
            "--user-agent",
            required=True,
            type=str,
            help="User Agent",
        )
        parser.add_argument(
            "--browser-min-major-version",
            required=False,
            type=int,
            help="Browser Minimum Major Version",
        )
        parser.add_argument(
            "--browser-max-major-version",
            required=False,
            type=int,
            help="Browser Minimum Major Version",
        )

    def handle(self, *args, **kwargs):
        try:
            h2_fingerprint = self.create_h2_fingerprint(kwargs)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully saved H2 Fingerprint: {h2_fingerprint}'))

    @staticmethod
    def create_h2_fingerprint(kwargs):
        return utils.h2_hash_to_h2_fingerprint(
            user_agent=kwargs['user_agent'],
            h2_hash=kwargs['hash'],
            browser_min_major_version=kwargs.get('browser_min_major_version'),
            browser_max_major_version=kwargs.get('browser_max_major_version')
        )
