

from dataclasses import dataclass
import weakref
from copy import deepcopy
from enum import Enum
from typing import Any, AsyncGenerator, Generic, TypeVar, cast

from aiohttp import ClientSession, ClientResponse
from aiohttp.client_exceptions import ContentTypeError

from .asyncy import end_loop_workaround #type: ignore
from .asyncy import AsyncInit, AsyncLazy
from .auth import Auth
from .web import Request, Method

Json = dict[str, Any]

class APIError(Exception):
    status: int
    reason: Any

    def __init__(self, status: int, reason: Any):
        super().__init__()
        self.status = status
        self.reason = reason

    def __str__(self) -> str:
        return super().__str__() + F"\nStatus: {self.status}\nReason: {self.reason}"


async def api_err(response: ClientResponse, result: Any = None) -> APIError:
    match result:
        case {'message': msg}:
            return APIError(response.status, msg)
        case _:
            return APIError(response.status, await response.text())


class _EnumParams:
    '''
        Emulate an EnumParam for serialization into URL params.
        Separate class and hidden since Enum's have special behavior.
    '''
    params: dict[str, set[str]]

    def __init__(self):
        self.params = {}

    def __add__(self, other: 'EnumParam|_EnumParams') -> 'EnumParam':
        new_instance = deepcopy(self)
        match other:
            case EnumParam():
                other_items = [(other.get_title(), {other.value})]
            case _EnumParams():
                other_items = other.params.items()
            case _:
                raise
        for k, v in other_items:
            if k not in new_instance.params:
                new_instance.params[k] = set()
            new_instance.params[k] |= v
        return cast(EnumParam, new_instance)

    def to_dict(self, delimiter: str = ',') -> dict[str, str]:
        '''
            Convert packed parameters to a dictionary for use in a URL.
        '''
        return {
            title: delimiter.join(values)
            for title, values in self.params.items()
        }

    def __contains__(self, member: 'EnumParam') -> bool:
        return member.value in self.params[member.get_title()]


Self = TypeVar('Self')


class EnumParam(Enum):
    '''
        Collection of API url parameters which have only specific values.
        Serializes to a dictionary for use in a URL.
    '''

    def get_title(self) -> str:
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:]

    def __add__(self: Self, other: 'EnumParam|_EnumParams') -> Self:
        '''Collect with another parameter or set of parameters.'''
        # return type is compatible with EnumParam for + and to_dict and in
        return _EnumParams() + self + other  # type: ignore

    def to_dict(self, _delimiter: str = ',') -> dict[str, str]:
        '''
            Convert packed parameters to a dictionary for use in a URL.
        '''
        return {
            self.get_title(): self.value
        }

    def __contains__(self, member: 'EnumParam') -> bool:
        return self.value == member.value

def convert_url_params(p: Json | None) -> dict[str, str]:
    '''Excludes empty-valued parameters'''
    if p is None: return {}
    return {k: str(v) for k, v in p.items() if v is not None and v != ''}

T = TypeVar('T')
@dataclass
class APIObj(Generic[T]):
    _service: T

    def __init__(self, service: T):
        self._service = service

class WebAPI(AsyncInit):
    base_url: str
    session: ClientSession
    auth: Auth | None

    def __init__(self, auth: Auth | None = None):
        
        self.auth = auth

    async def _async_init(self):
        # the aiohttp context manager does no asynchronous work when entering.
        # Using the context is not necessary as long as ClientSession.close() 
        # is called.
        session = await ClientSession().__aenter__()
        self.session = session

        # Although ClientSession.close() may be a coroutine, but it is not
        # necessary to await it as of the time of writing, since it's 
        # connector objects delegate their own coroutine close() methods to 
        # only synchronous methods.
        # this method ensures that the session is closed when the WebAPI object
        # is garbage collected.
        # noinspection PyProtectedMember
        self._finalize = weakref.finalize(self, session._connector._close)  # type: ignore ## reportPrivateUsage

        end_loop_workaround()

    def close(self):
        '''Closes the http session with the API server. Should be automatic.'''
        self._finalize()

    # convert a relative path to an absolute url for this api
    def get_full_url(self, path: str) -> str:
        '''convert a relative path to an absolute url for this api'''
        return self.base_url + path

    async def _req_json(self, req: Request) -> Any:
        async with req.send(self.session) as resp:
            try:
                result = await resp.json()
            except ContentTypeError:
                result = await resp.text()
            if resp.status != 200:
                raise await api_err(resp, result)
            return result

    async def _req_text(self, req: Request) -> str:
        async with req.send(self.session) as resp:
            result = await resp.text()
            if resp.status != 200:
                raise await api_err(resp, result)
            return result

    async def _req_empty(self, req: Request) -> None:
        async with req.send(self.session) as resp:
            if resp.status != 204:
                raise await api_err(resp)

    def _prepare_req(self, method: Method, path: str, params: Json | None,
        json: Any, data: Any, headers: dict[str, str] | None = None
        ) -> Request:
        full_url = self.get_full_url(path)
        if json is not None:
            data_ = json
            data_is_json = True
        else:
            data_ = data
            data_is_json = False
        if data_ is None:
            data_: dict[str, Any] = {}
        if headers is None:
            headers = {}
        return Request(method, full_url, convert_url_params(params), headers, data_, data_is_json)

    async def _call(self, method: Method, path: str, params: Json | None,
        json: Any, data: Any, headers: dict[str, str] | None = None
        ) -> dict[str, Any]:
        req = self._prepare_req(method, path, params, json, data, headers)
        if self.auth is not None:
            req = await self.auth.sign_request(self.session, req)
        return await self._req_json(req)

    async def get_json(self, path: str, params: Json | None=None, 
        json: Any=None, data: Any=None, headers: dict[str, str] | None=None
        ) -> dict[str, Any]:
        return await self._call(Method.GET, path, params, json, data, headers)

    async def post_json(self, path: str, params: Json | None=None, 
        json: Any=None, data: Any=None, headers: dict[str, str] | None=None
        ) -> dict[str, Any]:
        return await self._call(Method.POST, path, params, json, data, headers)

    async def put_json(self, path: str, params: Json | None=None, 
        json: Any=None, data: Any=None, headers: dict[str, str] | None=None
        ) -> dict[str, Any]:
        return await self._call(Method.PUT, path, params, json, data, headers)

    async def get_text(self, path: str, params: Json | None=None,
        json: Any=None, data: Any=None, headers: dict[str, str] | None=None
        ) -> str:
        req = self._prepare_req(Method.GET, path, params, json, data, headers)
        return await self._req_text(req)

    @AsyncLazy.wrap
    # TODO: google only?
    async def paginated(self,
                        path: str,
                        params: Json,  # non-const
                        limit: int | None) -> AsyncGenerator[Any, None]:
        '''
        Return an awaitable and async iterable over google-style paginated items.
        You can also await the return value to get the entire list.
        '''
        result_count = 0

        while True:
            page = await self.get_json(path, params)

            items = page.get('items')

            if not items: break

            # result_count += len(items)
            for item in items:
                result_count += 1
                yield item
                if limit is not None and result_count >= limit:
                    return

            page_token = cast(str, page.get('nextPageToken'))
            if not page_token: break
            params['pageToken'] = page_token