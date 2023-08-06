import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import secrets
from typing import Any

from .auth import Auth
from .web import Request, serve_one_request

import aiohttp, aiohttp.web

import urllib.parse

@dataclass
class OAuth2User:
    token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = 'Bearer'
    source_path: str | None = None
    scopes: list[str] = field(default_factory=list)

    def __init__(self, source: str | dict[str, Any], source_path: str | None = None) -> None:
        match source:
            case str(): # file path
                with open(source, 'r') as f:
                    self.__init__(json.load(f))
                    self.source_path = source
            case {
                'token': token,
                'refresh_token': refresh_token,
                'expires_at': expires_at_str,
                'token_type': token_type,
                'scopes': scopes
            }: #dumps
                self.token = token
                self.refresh_token = refresh_token
                self.expires_at = datetime.strptime(expires_at_str, '%Y-%m-%dT%H:%M:%SZ')
                self.token_type = token_type
                self.source_path = source_path
                self.scopes = scopes
            case {
                'access_token': token,
                'refresh_token': refresh_token,
                'expires_in': expires_str,
                'token_type': token_type,
                **others
            }: # OAuth 2 grant response
                expiry = (datetime.utcnow() + timedelta(seconds=int(expires_str))).replace(microsecond=0)
                self.token = token
                self.refresh_token = refresh_token
                self.expires_at = expiry
                self.token_type = token_type
                self.source_path = source_path
                if 'scope' in others:
                    self.scopes = others['scope'].split(' ')
            case _:
                raise ValueError(F"Invalid OAuth2User source: {source}")

    def to_dict(self) -> dict[str, Any]:
        return {
            'token': self.token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'token_type': self.token_type,
            'scopes': self.scopes
        }

    def save(self):
        if self.source_path:
            with open(self.source_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=4)
        else:
            raise ValueError("Cannot save OAuth2User without a path to save to")

@dataclass
class OAuth2(Auth):
    id: str
    secret: str

    auth_uri: str # flow step 1
    token_uri: str # flow step 2

    user: OAuth2User | None = None

    _refresh_task: asyncio.Task[None] | None = None

    def __init__(self, source: str | dict[str, Any], user: OAuth2User | None = None) -> None:
        match source:
            case str(): # file path
                with open(source, 'r') as f:
                    self.__init__(json.load(f))
            case { 'id': id_, 'secret': secret, 'auth_uri': auth_uri, 'token_uri': token_uri}: # dumps
                self.id = id_
                self.secret = secret
                self.auth_uri = auth_uri
                self.token_uri = token_uri
            case _:
                raise ValueError(F"Invalid OAuth2 source: {source}")
        self.user = user

    def verify_scope(self, scope: str):
        scopes = scope.split(' ')
        for scope in scopes:
            if not self.user:
                raise ValueError("User credentials must be used when scope is specified")
            if not scope in self.user.scopes:
                raise ValueError(F"User credentials do not have the scope: {scope}")
        return True

    def get_auth_url(self, redirect_uri: str, state: str, scopes: str) -> tuple[str, str]:
        challenge = secrets.token_urlsafe(54)
        params = {
            'client_id': self.id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'state': state+challenge,
            'scope': scopes,
            'access_type': 'offline'
            }
        return F"{self.auth_uri}?{urllib.parse.urlencode(params)}", challenge

    async def sign_request(self, session: aiohttp.ClientSession, request: Request) -> Request:
        if self.user is None:
            raise NotImplemented("OAuth 2 request signing without user is not yet implemented.")
        if self._refresh_task is not None:
            await asyncio.wait_for(self._refresh_task, timeout=None)
        elif datetime.utcnow() > self.user.expires_at:
            self._refresh_task = asyncio.create_task(self.refresh(session))
            await self._refresh_task
            self._refresh_task = None
        request.headers['Authorization'] = F"{self.user.token_type} {self.user.token}"
        return request

    async def refresh(self, session: aiohttp.ClientSession):
        if self.user is None:
            raise NotImplemented("Refresh without user is not implemented.")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.user.refresh_token,
            'client_id': self.id,
            'client_secret': self.secret,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        async with session.post(self.token_uri, data=data, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f'Refresh failed: {resp.status}')
            result = await resp.json()

        match result:
            case {
                'access_token': token,
                'expires_in': expires_str,
                'token_type': token_type,
                **_others
            }: # OAuth 2 refresh response
                expiry = datetime.utcnow() + timedelta(seconds=int(expires_str))
                self.user.token = token
                self.user.expires_at = expiry
                self.user.token_type = token_type
            case _:
                raise ValueError(F"Invalid OAuth2 refresh response: {result}")
        self.user.save()
         
    async def user_auth_flow(self, redirect_host: str, redirect_port: int, **kwargs: str):
        import webbrowser

        redirect_uri = F'http://{redirect_host}:{redirect_port}'

        session = aiohttp.ClientSession()

        scopes: str = kwargs['scopes']

        # step 1: get the user to authorize the application
        grant_link, challenge = self.get_auth_url(redirect_uri, '', scopes)

        webbrowser.open(grant_link, new=1, autoraise=True)

        # step 1 (cont.): wait for the user to be redirected with the code
        query = await serve_one_request(redirect_host, redirect_port, '<html><body>You can close this window now.</body></html>')

        if 'state' not in query:
            raise PermissionError("Redirect did not return any state parameter.")
        if not query['state'] == challenge:
            raise PermissionError("Redirect did not return the correct state parameter.")
        code = query['code']

        # step 2: exchange the code for access token
        grant_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.id,
            'client_secret': self.secret,
            'redirect_uri': redirect_uri,
            'scope': scopes
        }
        grant_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        async with session.post(self.token_uri, data=grant_data, headers=grant_headers) as resp:
            if resp.status != 200:
                raise Exception(f'Grant failed: {resp.status}')
            result = await resp.json()
            user = OAuth2User(result)

        self.user = user