import os
import uuid

from turbindo.log.logger import Logger
from turbindo.test import io as test_io


class TestCryptoManager:
    def __init__(self):
        # os.remove('testdb.db') #this should be implicit in the test system
        self.logger = Logger(f"CryptoManagerTest")

    async def async_init(self):
        await test_io.setup(recording=[])

    async def test_create_ca_crt(self):
        test_run = str(uuid.uuid4()).split('-')[0]
        ca_path = f'/tmp/ca-test-{test_run}.crt'
        key_path = f'/tmp/ca-test-{test_run}.key'

        await test_io.crypto().create_ca(
            crt_path=ca_path,
            key_path=key_path,
            country_name='US',
            state_name='NM',
            city_name='abq',
            org_name='test_org',
            common_name='test_service',
            ca_key_pw='abc123',
        )
        from os.path import exists
        assert exists(ca_path)
        assert exists(key_path)
        os.remove(ca_path)
        os.remove(key_path)
        return True

    async def test_issue_crt(self):
        test_run = str(uuid.uuid4()).split('-')[0]
        ca_crt_path = f'/tmp/ca-test-{test_run}.crt'
        ca_key_path = f'/tmp/ca-test-{test_run}.key'
        issue_cert_path = f'/tmp/issue-test-{test_run}.crt'
        issue_key_path = f'/tmp/issue-test-{test_run}.key'

        await test_io.crypto().create_ca(
            crt_path=ca_crt_path,
            key_path=ca_key_path,
            country_name='US',
            state_name='NM',
            city_name='abq',
            org_name='test_org',
            common_name='test_service',
            ca_key_pw='abc123',
        )
        from os.path import exists
        assert exists(ca_crt_path)
        assert exists(ca_key_path)
        await test_io.crypto().issue_cert(
            issue_crt_path=issue_cert_path,
            issue_key_path=issue_key_path,
            ca_crt_path=ca_crt_path,
            ca_key_path=ca_key_path,
            ca_key_pw='abc123',
            country_name='US',
            state_name='NM',
            city_name='abq',
            org_name='test_org',
            dns_name='bthz'
        )
        assert exists(issue_cert_path)
        assert exists(issue_key_path)

        os.remove(ca_crt_path)
        os.remove(ca_key_path)
        return True
