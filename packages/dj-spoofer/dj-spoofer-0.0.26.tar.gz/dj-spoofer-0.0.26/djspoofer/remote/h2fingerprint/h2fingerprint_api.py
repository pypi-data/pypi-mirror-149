import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import H2Error

logger = logging.getLogger(__name__)


BASE_URL = settings.H2_FINGERPRINT_API_BASE_URL


@decorators.wrap_exceptions(raise_as=H2Error)
def get_h2_fingerprint(client, *args, **kwargs):
    url = f'{BASE_URL}'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return H2FingerprintResponse(r.json())


class H2FingerprintResponse:
    def __init__(self, data):
        self.fingerprint = data['fingerprint']
        self.settings_frame = data['settings_frame']
        self.window_frame = data['window_frame']
        self.priority_frame = data['priority_frame']
        self.pseudo_headers = data['pseudo_headers']
        self.user_agent = data['user_agent']
