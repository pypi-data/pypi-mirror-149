import json
import time
from http.client import HTTPException
from types import TracebackType
from typing import List, Optional, Type, Union, Tuple

import httpx

from ._urls import AUTHORIZATION_URL
from ._endpoints import *
from .types import AuthToken, User, Guild, Channel, Role, Emoji, Member


class BaseClient:
    def __init__(self, token: Optional[str]):
        self._token = token

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Type[BaseException] = None, exc_value: BaseException = None,
                 traceback: TracebackType = None):
        self._token = None

    def _auth(self, bot: bool = True):
        if (bot):
            return {"Authorization": f"Bot {self._token}"}
        else:
            return {"Authorization": f"Bearer {self._token}"}

    @staticmethod
    def auth(client_id: int, scope: List[str], redirect_uri: str):
        """
        Generates a URL to authorize the client.
        :param client_id: Client ID of the discord application
        :param scope: Scopes used for this authorization. Check https://discord.com/developers/docs/topics/oauth2 for more information.
        :param redirect_uri:
        :return:
        """
        params = {
            "client_id": client_id,
            "scope": "%20".join(scope),
            "redirect_uri": redirect_uri
        }
        return AUTHORIZATION_URL.format(**params)

    def _checkRateLimit(self, response: httpx.Response) -> Tuple[bool, int]:
        if (response.status_code == 429):
            return True, int(
                [(key, value) for (key, value) in response.headers.raw if key == b'x-ratelimit-reset-after'][0][1])
        else:
            return False, 0


class Client(BaseClient):
    def __init__(self, token: Optional[str] = None):
        super().__init__(token)

    def fetch_token(self, client_id: Union[int, str], client_secret: str, code: str, redirect_uri: str) -> AuthToken:
        """
        Fetches an authorization token from the Discord API.
        :param code: Auth code received from the authorization URL.
        :param client_id: Client ID of the discord application.
        :param client_secret: Client secret of the discord application.
        :param redirect_uri: Redirect URI of the discord application.
        :return: AuthToken object containing the authorization token.
        """
        data = {
            "client_id": str(client_id),
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        response = httpx.post("https://discordapp.com/api/oauth2/token", data=data)

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return AuthToken(**response.json())

    def getCurrentUser(self, bot: bool = True) -> User:
        response = httpx.get(CURRENT_USER, headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return User(**response.json())

    def getCurrentUserGuilds(self, bot: bool = True) -> List[Guild]:
        response = httpx.get(CURRENT_USER_GUILDS, headers=self._auth(bot))

        rateLimited, resetAfter = self._checkRateLimit(response)
        if (rateLimited):
            time.sleep(resetAfter)
            return self.getCurrentUserGuilds(bot)

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Guild(**i) for i in response.json()]

    def getGuild(self, guild_id: Union[int, str], bot: bool = True) -> Guild:
        response = httpx.get(GUILD.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return Guild(**response.json())

    def getGuildChannels(self, guild_id: Union[int, str], bot: bool = True) -> List[Channel]:
        response = httpx.get(GUILD_CHANNELS.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Channel(**i) for i in response.json()]

    def getGuildMembers(self, guild_id: Union[int, str], bot: bool = True) -> List[Member]:
        response = httpx.get(GUILD_MEMBERS.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Member(**i) for i in response.json()]

    def getGuildRoles(self, guild_id: Union[int, str], bot: bool = True) -> List[Role]:
        response = httpx.get(GUILD_ROLES.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Role(**i) for i in response.json()]


class AsyncClient(BaseClient):
    def __init__(self, token: Optional[str] = None):
        super().__init__(token)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __await__(self):
        return self.__aenter__().__await__()

    async def fetch_token(self, code: str, client_id: int, client_secret: str, redirect_uri: str) -> AuthToken:
        """
        Fetches an authorization token from the Discord API.
        :param code: Auth code received from the authorization URL.
        :param client_id: Client ID of the discord application.
        :param client_secret: Client secret of the discord application.
        :param redirect_uri: Redirect URI of the discord application.
        :return: AuthToken object containing the authorization token.
        """
        data = {
            "client_id": str(client_id),
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://discordapp.com/api/oauth2/token", data=data)

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return AuthToken(**response.json())

    async def getCurrentUser(self, bot: bool = True) -> User:
        async with httpx.AsyncClient() as client:
            response = await client.get(CURRENT_USER, headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return User(**response.json())

    async def getCurrentUserGuilds(self, bot: bool = True) -> List[Guild]:
        async with httpx.AsyncClient() as client:
            response = await client.get(CURRENT_USER_GUILDS, headers=self._auth(bot))

        rateLimited, resetAfter = self._checkRateLimit(response)
        if (rateLimited):
            time.sleep(resetAfter)
            return await self.getCurrentUserGuilds(bot)

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Guild(**i) for i in response.json()]

    async def getGuild(self, guild_id: Union[int, str], bot: bool = True) -> Guild:
        async with httpx.AsyncClient() as client:
            response = await client.get(GUILD.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return Guild(**response.json())

    async def getGuildChannels(self, guild_id: Union[int, str], bot: bool = True) -> List[Channel]:
        async with httpx.AsyncClient() as client:
            response = await client.get(GUILD_CHANNELS.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Channel(**i) for i in response.json()]

    async def getGuildMembers(self, guild_id: Union[int, str], bot: bool = True) -> List[Member]:
        async with httpx.AsyncClient() as client:
            response = await client.get(GUILD_MEMBERS.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Member(**i) for i in response.json()]

    async def getGuildRoles(self, guild_id: Union[int, str], bot: bool = True) -> List[Role]:
        async with httpx.AsyncClient() as client:
            response = await client.get(GUILD_ROLES.format(guild_id=guild_id), headers=self._auth(bot))

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        return [Role(**i) for i in response.json()]
