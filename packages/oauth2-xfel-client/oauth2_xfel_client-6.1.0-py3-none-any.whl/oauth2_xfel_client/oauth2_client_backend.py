import logging
import time
from datetime import datetime

from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests import Timeout
from requests_oauthlib.oauth2_session import OAuth2Session

__author__ = 'Luis Maia <luis.maia@xfel.eu>'

log = logging.getLogger(__name__)

# Number of retries allowed before deal with the consequences!
DEF_MAX_RETRIES = 3

# Default Timeout for Request Connection and Read
DEF_TIMEOUT = 12


# requests_oauthlib supports automatically *refreshing* a token, an OAuth
# feature that doesn't require going through the full flow again.
# The XFEL services don't seem to allow this, but because we are using
# the backend flow, with no user interaction, it's relatively easy to get
# a brand new token.
# We are borrowing the parent class' auto_refresh_kwargs attribute to use
# for this purpose. refresh_token is disabled to avoid confusion.
class AutoRenewingOAuthSession(OAuth2Session):
    """OAuth session which automatically gets a new token on expiry
    """

    def request(self, method, url, *args, **kwargs):
        # If a previous token request failed, we may have no token.
        # Ensure we have one before making a request.
        if (not self.token) and url != self.auto_refresh_kwargs['token_url']:
            log.warning("Missing Oauth token - requesting one")
            self.fetch_token(**self.auto_refresh_kwargs)

        try:
            return super().request(method, url, *args, **kwargs)
        except TokenExpiredError:
            log.info("Expired Oauth token - requesting new one")
            self.fetch_token(**self.auto_refresh_kwargs)
            return super().request(method, url, *args, **kwargs)

    def refresh_token(self, *args, **kwargs):
        raise NotImplementedError(
            "Get a new token with fetch_token instead of refreshing it"
        )

    def fetch_token(self, max_retries=DEF_MAX_RETRIES, **kwargs):
        retries = max_retries
        retry_delay = 0
        while True:
            try:
                super().fetch_token(**kwargs)

            except Timeout as exp:
                # log.debug('Token request Timeout', exc_info=True)
                exp_msg = 'Exception [try {0}/{1} | timeout: {2} | ' \
                          'delay: {3}]: {4}'.format(retries,
                                                    max_retries,
                                                    kwargs['timeout'],
                                                    retry_delay, exp)
                log.debug(exp_msg, exc_info=True)
                # print('Timeout:' + '>' * 10 + exp_msg + '<' * 10)
                retries -= 1
                if retries <= 0:
                    raise

                # Sleep before retrying
                # (e.g. max_retries == 3)
                # Try 1: retry_delay = N.A.
                # Try 2: retry_delay = (3-1)/2 = 1 sec
                # Try 3: retry_delay = (3-1)/1 = 2 sec
                retry_delay = (max_retries - 1) / retries
                time.sleep(retry_delay)

                # # Increase timeout before retrying (FOR TESTING)
                # #
                # # (e.g. kwargs['max_retries'] == 3)
                # # Try 1: timeout (specified == ? || default == 3)
                # # Try 2: timeout = (3*4)/2 = 6 sec
                # # Try 3: timeout = (3*4)/1 = 12 sec
                # retry_timeout = (kwargs['max_retries'] * 4) / retries
                # kwargs['timeout'] = max(kwargs['timeout'], retry_timeout)

            except Exception as exp:
                exp_msg = 'Exception: {0}'.format(exp)
                log.debug(exp_msg, exc_info=True)
                # print('General:' + '-' * 10 + exp_msg + '-' * 10)
                raise

            else:
                log.debug('Got a new session token successfully')
                break


class Oauth2ClientBackend(object):
    # Parameter that will store the session used to "invoke" the APIs
    session = None

    def __init__(self, client_id, client_secret, scope, token_url,
                 refresh_url=None, auth_url=None, session_token=None,
                 max_retries=DEF_MAX_RETRIES,
                 timeout=DEF_TIMEOUT,
                 ssl_verify=True):

        self.client_secret = client_secret
        self.scope = scope
        self.token_url = token_url
        self.timeout = timeout  # Only applies to getting an Oauth token
        self.max_retries = max_retries

        # Not currently in use in this Oauth2 Strategy:
        # self.refresh_url = refresh_url
        # self.auth_url = auth_url

        # REQUESTS::ssl_verify (when endpoint uses HTTPS protocol)
        #
        # 1. Verify SSL Certificate only if `ssl_verify=True` (default)
        #    * Retro-compatible with ond code:
        #      - self.ssl_verify = token_url.startswith('https://in.xfel.eu')
        #    * Valid Certificate is expected (e.g. 'https://in.xfel.eu')
        #
        # 2. Self-signed endpoints ssl_verify must be set `ssl_verify=False`
        #    because only certificates issued by a certificate authority (CA)
        #    will be accepted by REQUESTS (e.g. 'https://127.0.0.1/')
        self.ssl_verify = ssl_verify

        self.fetch_token_kwargs = dict(
            token_url=self.token_url,
            client_secret=self.client_secret,
            max_retries=self.max_retries,
            timeout=self.timeout,
            verify=self.ssl_verify
        )

        # Configure client using "Backend Application Flow" Oauth 2.0 strategy
        self.client = BackendApplicationClient(client_id)

        # Negotiate with the server and obtains a valid session_token
        # after this self.session can be used to 'invoke' APIs
        self.auth_session(session_token=session_token)

    def auth_session(self, session_token=None):
        # If a session token was passed in & it's still valid,
        # create a session using it.
        if self.is_session_token_dt_valid(session_token):
            self._re_used_existing_session_token(session_token)
            # Nothing to do. Current Token is still valid!
            pass

        # Otherwise, try to get a new session token.
        else:
            try:
                log.debug('Will try to create a new session token')
                self._create_new_session_token()

            except Exception as exp:
                exp_msg = 'Exception: {0}'.format(exp)
                log.debug(exp_msg, exc_info=True)
                # print('New session:' + '+' * 10 + exp_msg + '+' * 10)
                raise

            else:
                log.debug('Got a new session token successfully')

        return True

    def _re_used_existing_session_token(self, session_token):
        self.session = AutoRenewingOAuthSession(
            client=self.client,
            scope=self.scope,
            token=session_token,
            auto_refresh_kwargs=self.fetch_token_kwargs,
        )

    def _create_new_session_token(self):
        self.session = AutoRenewingOAuthSession(
            client=self.client,
            scope=self.scope,
            auto_refresh_kwargs=self.fetch_token_kwargs,
        )

        self.session.fetch_token(**self.fetch_token_kwargs)

    def check_session_token(self):
        if not self.is_session_token_valid():
            self.auth_session()  # Get a new session & a new token

    def get_session_token(self):
        return self.session.token

    @property
    def headers(self):
        # This isn't needed - the session automatically adds this header to
        # requests. But downstream code may expect it to exist.
        auth_token_val = 'Bearer ' + self.session.token['access_token']
        return {'Authorization': auth_token_val}

    @property
    def oauth_token(self):
        tok = self.session.token.copy()
        # Convert expires_at to a datetime object, keeping previous interface
        tok['expires_at'] = datetime.fromtimestamp(tok['expires_at'])
        return tok

    def is_session_token_valid(self):
        current_token = self.get_session_token()
        return Oauth2ClientBackend.is_session_token_dt_valid(current_token)

    @staticmethod
    def is_session_token_dt_valid(session_token, dt=None):
        # Check session_token hash
        if session_token and 'expires_at' in session_token:
            # Convert Unix timestamp (seconds from the epoch) to datetime
            expires_dt = datetime.fromtimestamp(session_token['expires_at'])

            if dt is None:
                dt = datetime.now()

            # return True:
            # 1) If expire datetime is in future (token is still valid)
            # return False:
            # 1) If expire datetime is in past (a new token must be generated)
            return expires_dt > dt

        return False
