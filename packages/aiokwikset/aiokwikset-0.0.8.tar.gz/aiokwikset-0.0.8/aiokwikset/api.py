import json
import aioboto3
import attr
import datetime

from typing import Optional
from envs import env
from jose import jwt, JWTError
from urllib.parse import urlparse

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    ClientError, 
    ClientResponseError, 
    ClientConnectorError, 
    ServerConnectionError, 
    ClientPayloadError
)

from .errors import RequestError
from .device import Device
from .user import User
from .exceptions import TokenVerificationException

from aiokwikset.aws_kwikset import AWSKWIKSET
from aiokwikset.const import (
    LOGGER,
    POOL_ID,
    CLIENT_ID
)

DEFAULT_HEADER_USER_AGENT = 'okhttp/4.8.1'
DEFAULT_HEADER_ACCEPT_ENCODING = 'gzip'

@attr.s
class API(object):
    CUSTOM_VERIFIER_CHALLENGE = 'CUSTOM_CHALLENGE'

    username = attr.ib()
    user_pool_region = attr.ib()

    id_token = attr.ib(default=None)
    access_token = attr.ib(default=None)
    refresh_token = attr.ib(default=None)
    client_secret = attr.ib(default=None)
    expires_at = attr.ib(default=None)

    access_key = attr.ib(default=None)
    secret_key = attr.ib(default=None)
    client_callback = attr.ib(default=None)

    user_pool_id = POOL_ID
    client_id = CLIENT_ID
    aws = None

    device: Optional[Device] = None
    user: Optional[User] = None

    def get_client(self):
        if self.client_callback:
            return self.client_callback()

        boto3_client_kwargs = {}
        if self.access_key and self.secret_key:
            boto3_client_kwargs['aws_access_key_id'] = self.access_key
            boto3_client_kwargs['aws_secret_access_key'] = self.secret_key
        if self.user_pool_region:
            boto3_client_kwargs['region_name'] = self.user_pool_region

        self.session = aioboto3.Session()
        return self.session.client(
            'cognito-idp', **boto3_client_kwargs)

    @user_pool_region.default
    def generate_region_from_pool(self):
        return self.user_pool_id.split('_')[0]

    def get_session(self):
        return ClientSession()

    async def get_keys(self):
        try:
            return self.pool_jwk
        except AttributeError:
            # Check for the dictionary in environment variables.
            pool_jwk_env = env('COGNITO_JWKS', {}, var_type='dict')
            if len(pool_jwk_env.keys()) > 0:
                self.pool_jwk = pool_jwk_env
                return self.pool_jwk

            # If it is not there use the aiohttp library to get it
            async with self.get_session() as session:
                resp = await session.get(
                    'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format( # noqa
                        self.user_pool_region, self.user_pool_id
                    ))
                self.pool_jwk = await resp.json()
                return self.pool_jwk

    async def get_key(self, kid):
        keys = (await self.get_keys()).get('keys')
        key = list(filter(lambda x: x.get('kid') == kid, keys))
        return key[0]

    async def verify_token(self, token, id_name, token_use):
        kid = jwt.get_unverified_header(token).get('kid')
        unverified_claims = jwt.get_unverified_claims(token)
        token_use_verified = unverified_claims.get('token_use') == token_use
        if not token_use_verified:
            raise TokenVerificationException(
                'Your {} token use could not be verified.')
        hmac_key = await self.get_key(kid)
        try:
            verified = jwt.decode(token, hmac_key, algorithms=['RS256'],
                                  audience=unverified_claims.get('aud'),
                                  issuer=unverified_claims.get('iss'))
        except JWTError:
            raise TokenVerificationException(
                'Your {} token could not be verified.')
        setattr(self, id_name, token)
        return verified

    async def _request(self, method: str, url: str, **kwargs) -> dict:
        """Make a request against the API."""

        await self.check_token()

        kwargs.setdefault("headers", {})
        kwargs["headers"].update(
            {
                "Host": urlparse(url).netloc,
                "User-Agent": DEFAULT_HEADER_USER_AGENT,
                "Accept-Encoding": DEFAULT_HEADER_ACCEPT_ENCODING
            }
        )

        if self.id_token:
            kwargs["headers"]["Authorization"] = "Bearer {}".format(self.id_token)

        session = self.get_session()

        try:
            async with session.request(method, url, **kwargs) as resp:
                data: dict = await resp.json(content_type=None)
                resp.raise_for_status()
                return data

        except ClientResponseError as err:
            raise RequestError(f"There was a response error while requesting {url}: {err}") from err
        except ClientConnectorError as err:
            raise RequestError(f"There was a client connection error while requesting {url}: {err}") from err
        except ServerConnectionError as err:
            raise RequestError(f"There was a server connection error while requesting {url}: {err}") from err
        except ClientPayloadError as err:
            raise RequestError(f"There was a client payload error while requesting {url}: {err}") from err
        except ClientError as err:
            raise RequestError(f"There was the following error while requesting {url}: {err}") from err
        finally:
            await session.close()

    async def check_token(self, renew=True):
        """
        Checks the exp attribute of the access_token and either refreshes
        the tokens by calling the renew_access_tokens method or does nothing
        :param renew: bool indicating whether to refresh on expiration
        :return: bool indicating whether access_token has expired
        """
        if not self.access_token:
            raise AttributeError('Access Token Required to Check Token')
        now = datetime.datetime.now()
        dec_access_token = jwt.get_unverified_claims(self.access_token)

        if now > datetime.datetime.fromtimestamp(dec_access_token['exp']):
            expired = True
            if renew:
                await self.renew_access_token()
        else:
            expired = False
        return expired

    async def renew_access_token(self):
        """
        Sets a new access token on the User using the refresh token.
        """
        auth_params = {'SECRET_HASH': '', 'REFRESH_TOKEN': self.refresh_token}

        async with self.get_client() as client:
            refresh_response = await client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters=auth_params,
            )

            self._set_attributes(
                refresh_response,
                {
                    'access_token':
                    refresh_response['AuthenticationResult']['AccessToken'],
                    'id_token':
                    refresh_response['AuthenticationResult']['IdToken'],
                    'token_type':
                    refresh_response['AuthenticationResult']['TokenType']
                }
            )

            if not self.device:
                self.device = Device(self._request)

            if not self.user:
                self.user = User(self._request)

    def _set_attributes(self, response, attribute_dict):
        """
        Set user attributes based on response code
        :param response: HTTP response from Cognito
        :attribute dict: Dictionary of attribute name and values
        """
        status_code = response.get(
            'HTTPStatusCode',
            response['ResponseMetadata']['HTTPStatusCode']
        )
        if status_code == 200:
            for k, v in attribute_dict.items():
                setattr(self, k, v)

    async def authenticate(self, password):
        """
        Authenticate the user using the SRP protocol
        :param password: The user's passsword
        :return:
        """
        self.aws = AWSKWIKSET(username=self.username, password=password,
                     pool_id=self.user_pool_id,
                     client_id=self.client_id, client=self.get_client(),
                     client_secret=self.client_secret)

        pre_verification = await self.aws.authenticate_user()
        return pre_verification

    async def verify_user(self, pre_verification, code):
        challenge_responses = {'ANSWER': 'answerType:verifyCode,medium:phone,codeType:login,code:{}'.format(code),"USERNAME": self.username}

        async with self.get_client() as client:
            tokens = await client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName=self.CUSTOM_VERIFIER_CHALLENGE,
                Session=pre_verification['Session'],
                ChallengeResponses=challenge_responses)

            await self.verify_token(tokens['AuthenticationResult']['IdToken'],
                                    'id_token', 'id')
            self.refresh_token = tokens['AuthenticationResult']['RefreshToken']
            await self.verify_token(tokens['AuthenticationResult']['AccessToken'],
                                    'access_token', 'access')
            self.token_type = tokens['AuthenticationResult']['TokenType']

            if not self.device:
                self.device = Device(self._request)

            if not self.user:
                self.user = User(self._request)