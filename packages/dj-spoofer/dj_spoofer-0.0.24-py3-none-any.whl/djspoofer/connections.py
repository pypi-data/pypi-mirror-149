import collections
import logging

import h2
from h2.settings import Settings, SettingCodes
from httpcore._models import Request
from httpcore._sync import http2

from djspoofer import exceptions
from djspoofer.models import H2Fingerprint

logger = logging.getLogger(__name__)

H2_FINGERPRINT_HEADER = b'h2-fingerprint-id'


def _send_connection_init(self, request: Request) -> None:
    """
        ** Monkey Patched in apps.py **
        The HTTP/2 connection requires some initial setup before we can start
        using individual request/response streams on it.
    """
    # Need to set these manually here instead of manipulating via
    # __setitem__() otherwise the H2Connection will emit SettingsUpdate
    # frames in addition to sending the undesired defaults.
    h2_frame_fingerprint = _get_h2_fingerprint(request)
    self._h2_state.local_settings = build_h2_settings(h2_frame_fingerprint)

    self._h2_state.get_next_available_stream_id = lambda: h2_frame_fingerprint.priority_stream_id
    self._h2_state.initiate_connection()
    self._h2_state.increment_flow_control_window(h2_frame_fingerprint.window_update_increment)

    self._write_outgoing_data(request)


def _send_request_headers(self, request: Request, stream_id: int) -> None:
    """
        ** Monkey Patched in apps.py **
    """
    end_stream = not http2.has_body_headers(request)

    h2_fingerprint = _get_h2_fingerprint(request)
    headers = _get_psuedo_headers(request, h2_fingerprint=h2_fingerprint) + [
        (k.lower(), v)
        for k, v in request.headers
        if k.lower()
        not in (
            b"host",
            b"transfer-encoding",
            H2_FINGERPRINT_HEADER
        )
    ]

    self._h2_state.send_headers(
        stream_id,
        headers,
        end_stream=end_stream,
        priority_weight=h2_fingerprint.priority_weight,
        priority_depends_on=h2_fingerprint.priority_depends_on_id,
        priority_exclusive=h2_fingerprint.priority_exclusive
    )
    self._h2_state.increment_flow_control_window(h2_fingerprint.window_update_increment, stream_id=stream_id)
    self._write_outgoing_data(request)


def _get_psuedo_headers(request, h2_fingerprint):
    header_map = {
        'm': (b":method", request.method),
        'a': (b":authority", _get_authority(request)),
        's': (b":scheme", request.url.scheme),
        'p': (b":path", request.url.target),
    }
    return [header_map[k] for k in h2_fingerprint.psuedo_header_order.split(',')]


def _get_authority(request):
    """
        In HTTP/2 the ':authority' pseudo-header is used instead of 'Host'.
        In order to gracefully handle HTTP/1.1 and HTTP/2 we always require
        HTTP/1.1 style headers, and map them appropriately if we end up on
        an HTTP/2 connection.
    """
    return [v for k, v in request.headers if k.lower() == b"host"][0]


def _get_h2_fingerprint(request):
    for i, (h_key, h_val) in enumerate(request.headers):
        if h_key == H2_FINGERPRINT_HEADER:
            return H2Fingerprint.objects.get_by_oid(str(h_val, 'utf-8'))
    raise exceptions.DJSpooferError(f'Header "{H2_FINGERPRINT_HEADER}" missing')


def build_h2_settings(h2_settings_fingerprint):
    h2_fp = h2_settings_fingerprint
    initial_values = {
        SettingCodes.HEADER_TABLE_SIZE: h2_fp.header_table_size,                            # 0x01 (Required)
        SettingCodes.ENABLE_PUSH: int(h2_fp.enable_push) if h2_fp.enable_push else None,    # 0x02 (Required)
        SettingCodes.MAX_CONCURRENT_STREAMS: h2_fp.max_concurrent_streams,                  # 0x03 (Optional)
        SettingCodes.INITIAL_WINDOW_SIZE: h2_fp.initial_window_size,                        # 0x04 (Required)
        SettingCodes.MAX_FRAME_SIZE: h2_fp.max_frame_size,                                  # 0x05 (Required)
        SettingCodes.MAX_HEADER_LIST_SIZE: h2_fp.max_header_list_size,                      # 0x06 (Optional)
    }
    initial_values = {k: v for k, v in initial_values.items() if v}
    return H2Settings(initial_values=initial_values)


class H2Settings(h2.settings.Settings):
    """
        Allows for setting the settings value in any particular order.
        There is no validation of settings since validation throws errors for missing or invalid values
        Use with caution!
    """
    def __init__(self, initial_values=None):
        super().__init__()
        self._settings = {k: collections.deque([v]) for k, v in initial_values.items()}
