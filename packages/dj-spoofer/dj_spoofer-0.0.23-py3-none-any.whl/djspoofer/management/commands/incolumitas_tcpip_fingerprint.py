from django.conf import settings
from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.remote.incolumitas import incolumitas_tcpip_api
from djspoofer.remote.proxyrack import utils as pr_utils


class Command(BaseCommand):
    help = 'Get TCP/IP Fingerprint'

    def add_arguments(self, parser):
        parser.add_argument(
            "--proxy-url",
            required=True,
            type=str,
            help="Set the proxy url",
        )
        parser.add_argument(
            "--proxy-args",
            required=False,
            nargs='*',
            help="Set the proxy password",
        )

    def handle(self, *args, **kwargs):
        proxy_builder = pr_utils.ProxyBuilder(
            netloc=kwargs.pop('proxy_url'),
            password=settings.PROXY_PASSWORD,
            username=settings.PROXY_USERNAME,
            **self.proxy_options(kwargs.get('proxy_args', list())),
        )
        try:
            with DesktopChromeClient(proxy_url=proxy_builder.http_url) as client:
                r_tcpip = incolumitas_tcpip_api.tcpip_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tcpip))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TCP/IP Fingerprint'))

    @staticmethod
    def proxy_options(proxy_args):
        return {args.split('=')[0]: args.split('=')[1] for args in proxy_args}
