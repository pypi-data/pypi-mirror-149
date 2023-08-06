from django.core.management.base import BaseCommand

from djspoofer import const, utils
from djspoofer.models import Proxy, Fingerprint, DeviceFingerprint, IntoliFingerprint
from djspoofer.remote.intoli import tasks


class Command(BaseCommand):
    help = 'DJ Spoofer Init'

    def handle(self, *args, **kwargs):
        try:
            proxy_url = input('Enter rotating proxy url (Example: premium.residential.proxyrack.net:10000): ')
            fingerprint_count = input('Enter number of Desktop Fingerprints to create (Default 50): ') or 50

            self.create_h2_fingerprints()
            self.create_rotating_proxy(proxy_url)
            self.store_intoli_fingerprints()
            self.create_fingerprints(count=fingerprint_count)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Initialized DJ Spoofer'))

    def create_h2_fingerprints(self):
        utils.h2_hash_to_h2_fingerprint(
            os='Windows',
            browser='Chrome',
            h2_hash='1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p',
            browser_min_major_version=80,
            browser_max_major_version=110,
        )
        utils.h2_hash_to_h2_fingerprint(
            os='Linux',
            browser='Chrome',
            h2_hash='1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p',
            browser_min_major_version=80,
            browser_max_major_version=110,
        )
        utils.h2_hash_to_h2_fingerprint(
            os='Windows',
            browser='Edge',
            h2_hash='1:65536;3:1000;4:6291456;6:262144|15663105|1:1:0:256|m,a,s,p',
            browser_min_major_version=80,
            browser_max_major_version=110,
        )
        utils.h2_hash_to_h2_fingerprint(
            os='Windows',
            browser='Firefox',
            h2_hash='1:65536;4:131072;5:16384|12517377|15:0:13:42|m,p,a,s',
            browser_min_major_version=70,
            browser_max_major_version=110,
        )
        utils.h2_hash_to_h2_fingerprint(
            os='Linux',
            browser='Firefox',
            h2_hash='1:65536;4:131072;5:16384|12517377|15:0:13:42|m,p,a,s',
            browser_min_major_version=70,
            browser_max_major_version=110,
        )
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Created H2 Fingerprints'))

    def create_rotating_proxy(self, proxy_url):
        proxy = Proxy.objects.create_rotating_proxy(url=proxy_url)
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Created Rotating Proxy: {proxy}'))

    def store_intoli_fingerprints(self):
        tasks.get_profiles(max_profiles=150, desktop_only=True, os_list=const.SUPPORTED_OS)
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Created Intoli Fingerprints'))

    def create_fingerprints(self, count):
        for i_fp in IntoliFingerprint.objects.weighted_n_desktop(count=count):
            ua_parser = utils.UserAgentParser(i_fp.user_agent)
            Fingerprint.objects.create(
                device_fingerprint=DeviceFingerprint.objects.create(
                    browser=ua_parser.browser,
                    browser_major_version=ua_parser.browser_major_version,
                    device_category=i_fp.device_category,
                    os=ua_parser.os,
                    platform=i_fp.platform,
                    screen_height=i_fp.screen_height,
                    screen_width=i_fp.screen_width,
                    user_agent=i_fp.user_agent,
                    viewport_height=i_fp.viewport_height,
                    viewport_width=i_fp.viewport_width,
                )
            )
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Created {count} Fingerprints'))
