import logging
from ssl import TLSVersion

import httpx
from django.conf import settings
from djstarter.clients import Http2Client

from djspoofer import utils
from djspoofer.remote.proxyrack import backends

logger = logging.getLogger(__name__)


class DesktopClient(Http2Client, backends.ProxyRackProxyBackend):
    def __init__(self, fingerprint, *args, **kwargs):
        logger.info(f'Starting session with fingerprint: {fingerprint}')
        self.fingerprint = fingerprint
        self.user_agent = self.fingerprint.device_fingerprint.user_agent
        super().__init__(
            proxies=self._get_proxies(),
            verify=self._get_ssl_context(),
            *args,
            **kwargs
        )

    def init_headers(self):
        h2_fingerprint = self.fingerprint.h2_fingerprint
        return super().init_headers() | {
            'h2-fingerprint-id': h2_fingerprint.oid_str
        }

    def _get_proxies(self):
        if settings.PROXY_URL == 'False':
            return dict()
        proxy_url = settings.PROXY_URL or self.get_proxy_url(self.fingerprint)
        return utils.proxy_dict(proxy_url)

    def _get_ssl_context(self):
        tls_fingerprint = self.fingerprint.tls_fingerprint

        context = httpx.create_ssl_context(http2=True, verify=settings.SSL_VERIFY)
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(tls_fingerprint.ciphers)
        context.options = tls_fingerprint.extensions

        return context

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)


class DesktopChromeClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ua_parser = utils.UserAgentParser(self.user_agent)

    def init_headers(self):
        return super().init_headers() | {
            'user-agent': self.user_agent,
        }

    @property
    def sec_ch_ua(self):
        version = self.ua_parser.browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_mobile(self):
        return '?0'

    @property
    def sec_ch_ua_platform(self):
        platform = self.ua_parser.os
        return f'"{platform}"'


class DesktopFirefoxClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_headers(self):
        return super().init_headers() | {
            'User-Agent': self.user_agent,
        }
