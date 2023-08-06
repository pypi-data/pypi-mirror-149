
from unittest import mock

from django.test import TestCase
from httpcore._models import Origin, Request, URL
from httpcore._sync import HTTPConnection, HTTP2Connection
from httpcore.backends import sync

from djspoofer.models import H2Fingerprint


class ConnectionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.h2_fingerprint_data = {
            'os': 'Windows',
            'browser': 'Chrome',
            'browser_min_major_version': 95,
            'browser_max_major_version': 100,
            'header_table_size': 65536,
            'enable_push': True,
            'max_concurrent_streams': 1000,
            'initial_window_size': 6291456,
            'max_frame_size': 16384,
            'max_header_list_size': 262144,
            'psuedo_header_order': 'm,a,s,p',
            'window_update_increment': 15663105,
            'priority_stream_id': 1,
            'priority_exclusive': True,
            'priority_depends_on_id': 0,
            'priority_weight': 256
        }

    @mock.patch.object(sync, 'SyncStream')
    @mock.patch.object(HTTPConnection, 'handle_request')
    def test_ok(self, mock_handle_request, mock_sync_stream):
        mock_sync_stream.write.return_value = None

        h2_fingerprint = H2Fingerprint.objects.create(**self.h2_fingerprint_data)
        origin = Origin(
            scheme=b'http',
            host=b'www.example.com',
            port=80,
        )
        url = URL(
            url='http://www.example.com'
        )
        req = Request(
            url=url,
            method='GET',
            headers={
                b'host': 'www.example.com',
                b'h2-fingerprint-id': str(h2_fingerprint.oid)
            })
        http2_connection = HTTP2Connection(
            origin=origin,
            stream=mock_sync_stream(),
            keepalive_expiry=10.0
        )

        http2_connection._receive_response = lambda *args, **kwargs: (200, list())
        mock_handle_request.return_value = http2_connection.handle_request(req)
