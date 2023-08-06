from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Proxy
from djspoofer.remote.ja3er import ja3er_api


class Command(BaseCommand):
    help = 'Ja3er Check'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient(proxy_url=Proxy.objects.get_sticky_proxy().http_url) as chrome_client:
                self.get_ja3_details(chrome_client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ja3er details'))

    def get_ja3_details(self, chrome_client):
        self.stdout.write(f'Spoofed User Agent: {chrome_client.user_agent}')

        self.stdout.write(utils.eye_catcher_line('JA3 Details'))
        r_json = ja3er_api.details(chrome_client)
        self.stdout.write(utils.pretty_dict(r_json.data))

        self.stdout.write(f'ssl_version: {r_json.ssl_version}')
        self.stdout.write(f'ciphers: {r_json.ciphers}')
        self.stdout.write(f'ssl_extensions: {r_json.ssl_extensions}')
        self.stdout.write(f'elliptic_curve: {r_json.elliptic_curve}')
        self.stdout.write(f'elliptic_curve_point_format: {r_json.elliptic_curve_point_format}')

        self.stdout.write(utils.eye_catcher_line('JA3 Hash Search'))
        r_search = ja3er_api.search(chrome_client, ja3_hash=r_json.ja3_hash)
        self.stdout.write(utils.pretty_dict(r_search.json()))



