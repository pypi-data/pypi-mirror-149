import logging
import random

from faker import Faker
from ua_parser import user_agent_parser

from . import models, providers

logger = logging.getLogger(__name__)


fake = Faker('en_US')
fake.add_provider(providers.UsernameProvider)
fake.add_provider(providers.PhoneNumberProvider)


class FakeProfile:
    MIN_PWD_LEN = 6

    def __init__(self, username=None):
        self.username = username or fake.username()
        self.gender = random.choice(['M', 'F'])
        self.first_name = fake.first_name_male() if self.gender == 'M' else fake.first_name_female()
        self.last_name = fake.last_name()
        self.dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        self.contact_email = f'{fake.username()}@{fake.free_email_domain()}'
        self.addr_state = fake.state_abbr()
        self.us_phone_number = fake.us_e164()
        self.password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def __str__(self):
        return f'FakeProfile -> username: {self.username}, full_name: {self.full_name}'

    @property
    def full_gender(self):
        return 'MALE' if self.gender == 'M' else 'FEMALE'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def dob_yyyymmdd(self):
        return self.dob.strftime('%Y-%m-%d')


class UserAgentParser:
    class UserAgent:
        def __init__(self, data):
            self.data = data

        @property
        def family(self):
            return self.data['family']

        @property
        def major(self):
            return self.data['major']

        @property
        def minor(self):
            return self.data['minor']

        @property
        def patch(self):
            return self.data['patch']

    class OS(UserAgent):
        pass

    def __init__(self, user_agent):
        self.ua_parser = user_agent_parser.Parse(user_agent)
        self._user_agent = self.UserAgent(self.ua_parser['user_agent'])
        self._os = self.OS(self.ua_parser['os'])

    @property
    def browser(self):
        return self._user_agent.family

    @property
    def browser_major_version(self):
        return self._user_agent.major

    @property
    def os(self):
        return self._os.family

    def __str__(self):
        return f'UserAgentParser -> {self.ua_parser}'


class H2HashParser:
    class SettingsFrame:
        def __init__(self, data):
            self._data = data
            pairs = [pair.split(':') for pair in data.split(';')]
            kv_map = {str(k): int(v) for k, v in pairs}
            self.header_table_size = kv_map.get('1')
            self.push_enabled = kv_map.get('2')
            self.max_concurrent_streams = kv_map.get('3')
            self.initial_window_size = kv_map.get('4')
            self.max_frame_size = kv_map.get('5')
            self.max_header_list_size = kv_map.get('6')

    class PriorityFrame:
        def __init__(self, data):
            parts = [int(v) for v in data.split(':')]
            self.stream_id = parts[0]
            self.is_exclusive = parts[1]
            self.depends_on_id = parts[2]
            self.weight = parts[3]

    def __init__(self, hash):
        parts = hash.split('|')
        self.settings_frame = self.SettingsFrame(parts[0])
        self.window_frame = int(parts[1] or 0)
        self.priority_frame = self.PriorityFrame(parts[2])
        self.pseudo_headers = parts[3]


def h2_hash_to_h2_fingerprint(os, browser, h2_hash, browser_min_major_version=None, browser_max_major_version=None):
    h2_parser = H2HashParser(hash=h2_hash)
    return models.H2Fingerprint.objects.create(
        browser=browser,
        os=os,
        browser_min_major_version=browser_min_major_version,
        browser_max_major_version=browser_max_major_version,
        header_table_size=h2_parser.settings_frame.header_table_size,
        enable_push=bool(h2_parser.settings_frame.push_enabled),
        max_concurrent_streams=h2_parser.settings_frame.max_concurrent_streams,
        initial_window_size=h2_parser.settings_frame.initial_window_size,
        max_frame_size=h2_parser.settings_frame.max_frame_size,
        max_header_list_size=h2_parser.settings_frame.max_header_list_size,
        psuedo_header_order=h2_parser.pseudo_headers,
        window_update_increment=h2_parser.window_frame,
        priority_stream_id=h2_parser.priority_frame.stream_id,
        priority_exclusive=h2_parser.priority_frame.is_exclusive,
        priority_depends_on_id=h2_parser.priority_frame.depends_on_id,
        priority_weight=h2_parser.priority_frame.weight,
    )


def proxy_dict(proxy_url):
    if proxy_url:
        return {
            'http://': proxy_url,
            'https://': proxy_url,
        }
    return dict()
