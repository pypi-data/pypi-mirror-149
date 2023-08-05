"""Oauth2ClientBackend unitary tests"""

import unittest
from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time

from oauth2_xfel_client.oauth2_client_backend import \
    Oauth2ClientBackend as Oauth2Client
from .common.secrets import *

__author__ = 'Luis Maia <luis.maia@xfel.eu>'


class Oauth2ClientBackendTest(unittest.TestCase):
    def setUp(self):
        self.client_id = CLIENT_OAUTH2_INFO['CLIENT_ID']
        self.client_secret = CLIENT_OAUTH2_INFO['CLIENT_SECRET']
        self.scope = None
        self.auth_url = CLIENT_OAUTH2_INFO['AUTH_URL']
        self.token_url = CLIENT_OAUTH2_INFO['TOKEN_URL']
        self.refresh_url = self.token_url

        self.base_api_url = BASE_API_URL

        self.valid_token = {}
        self.invalid_token = {
            u'access_token': USER_ACCESS_TOKEN,
            u'expires_at': 1410368490.381425,
            u'expires_in': 7200,
            u'token_type': u'bearer'
        }

    @staticmethod
    def validate_token_duration(duration_s, expected=7200):
        """Check that token duration is 2 hours or just under

        Token duration should be 2 hours, but it's sometimes slightly less,
        presumably because of a delay somewhere. Allow up to 5 seconds less.
        """
        assert duration_s <= expected, \
            "Token duration ({}) should be <= {}".format(duration_s, expected)

    def test_new_session(self):
        # No session token
        client = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
        )
        tok = client.get_session_token()

        assert client.is_session_token_dt_valid(tok)
        assert not client.is_session_token_dt_valid(
            tok, datetime.now() + timedelta(seconds=7205)
        ), "Invalid session token expiring date (expect: 2h:5s in future)"

        self.assertEqual(tok['token_type'].lower(), 'bearer')
        self.assertEqual(client.headers['Authorization'],
                         'Bearer ' + tok['access_token'])

        # Token still valid, so this shouldn't create a new session
        client.check_session_token()
        self.assertEqual(client.get_session_token(), tok)

    def test_reuse_invalid_token(self):
        # Passing an invalid_token to the constructor (in param session_token)
        # will create a new token (the same happen when session_token=None)
        client = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
            session_token=self.invalid_token
        )

        current_token = client.get_session_token()

        # Checking invalid_token
        assert not client.is_session_token_dt_valid(self.invalid_token)

        # Checking current_token != invalid_token
        self.assertNotEqual(self.invalid_token['access_token'],
                            current_token['access_token'],
                            "Invalid token was successfully used")

        self.assertEqual(client.oauth_token['access_token'],
                         current_token['access_token'],
                         "oauth_token and current_token must be equal")

        self.assertNotEqual(self.invalid_token['expires_at'],
                            current_token['expires_at'],
                            "Invalid token expires_at was successfully used")
        self.assertEqual(
            client.oauth_token['expires_at'],
            datetime.fromtimestamp(current_token['expires_at']),
            "oauth_token and current_token 'expires_at' must be equal")

        self.validate_token_duration(current_token['expires_in'])

        self.assertEqual(current_token['token_type'].lower(),
                         u'bearer',
                         "Token type is 'bearer'")

        assert client.is_session_token_valid(), "Invalid session token"

        assert client.is_session_token_dt_valid(
            current_token
        ), "Invalid session token expiring date (expect: now)"

        assert not client.is_session_token_dt_valid(
            current_token,
            datetime.now() + timedelta(seconds=7205)
        ), "Invalid session token expiring date (expect: 2h:5s in future)"

    def test_reuse_valid_token(self):
        # Get a valid token
        client1 = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
        )
        c1_token = client1.get_session_token()

        # Passing a valid session_token should use it
        client2 = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
            session_token=c1_token
        )
        c2_token = client2.get_session_token()

        self.assertEqual(c2_token, c1_token,
                         "Valid session token was not used")

        self.validate_token_duration(c1_token['expires_in'])
        self.validate_token_duration(c2_token['expires_in'])

        self.assertEqual(c1_token['token_type'].lower(), 'bearer')

        self.assertEqual(c2_token['token_type'].lower(), 'bearer')

        assert client1.is_session_token_valid(), "Invalid session token"

        assert client1.is_session_token_dt_valid(
            c2_token
        ), "Invalid session token expiring date (expect: now)"

        assert not client1.is_session_token_dt_valid(
            c2_token,
            dt=datetime.now() + timedelta(seconds=7205)
        ), "Invalid session token expiring date (expect: 2h:5s in future)"

    def test_request(self):
        client = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
        )

        # .../api/me is a typical endpoint for the current EuXFEL services
        url = BASE_API_URL + 'me'
        headers = {
            'Accept': 'application/json; version=1',
            'X-User-Email': CLIENT_OAUTH2_INFO['EMAIL'],
        }
        r = client.session.get(url, headers=headers)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        j = r.json()
        self.assertEqual(j['email'], CLIENT_OAUTH2_INFO['EMAIL'])

    def test_auto_renew(self):
        client = Oauth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
            token_url=self.token_url,
            refresh_url=self.refresh_url,
            auth_url=self.auth_url,
        )
        orig_token = client.get_session_token()

        # .../api/me is a typical endpoint for the current EuXFEL services
        url = BASE_API_URL + 'me'
        headers = {
            'Accept': 'application/json; version=1',
            'X-User-Email': CLIENT_OAUTH2_INFO['EMAIL'],
        }

        # Tokens last 2 hours, so 3 hours in the future it will have expired.
        # This works because oauthlib checks the token expiry on the client
        with freeze_time(datetime.now() + timedelta(hours=3)):
            r = client.session.get(url, headers=headers)

        self.assertEqual(r.status_code, HTTPStatus.OK)

        # We should have got a new token
        self.assertNotEqual(client.get_session_token(), orig_token)


if __name__ == '__main__':
    unittest.main()
