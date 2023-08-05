from typing import TypeVar, Type, Generic, Optional, Any, AsyncIterable, Iterable

from httpx import Client as HttpxClient, AsyncClient as HttpxAsyncClient
from pydantic import BaseModel as PydanticBaseModel

from dry_core.exceptions import NotFoundError

SelectorInstance = TypeVar("SelectorInstance")


class BaseSelector(Generic[SelectorInstance]):
    model: Type[SelectorInstance]


#######################
#   API Selectors
#######################
class PaginationPageRequestParams(PydanticBaseModel):
    url: str
    query_params: Optional[dict[str, str]] = None


class BasePaginationModel(PydanticBaseModel):
    def is_next_page(self) -> bool:
        raise NotImplementedError

    def is_prev_page(self) -> bool:
        raise NotImplementedError

    @classmethod
    def get_first_page_request_params(
        cls,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> PaginationPageRequestParams:
        raise NotImplementedError

    def get_next_page_request_params(
        self,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> Optional[PaginationPageRequestParams]:
        raise NotImplementedError

    def get_prev_page_request_params(
        self,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> Optional[PaginationPageRequestParams]:
        raise NotImplementedError

    def get_page_results(self, model_class: Type) -> list[Any]:
        raise NotImplementedError


class LimitOffsetPaginationModel(BasePaginationModel):
    _default_limit: int = 50

    limit: int = _default_limit
    offset: int = 0
    count: int = 0
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[dict[str, Any]] = []

    @property
    def is_next_page(self) -> bool:
        return self.next is not None

    @property
    def is_prev_page(self) -> bool:
        return self.previous is not None

    @classmethod
    def get_first_page_request_params(
        cls,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> PaginationPageRequestParams:
        query_params = query_params or {}
        return PaginationPageRequestParams(
            url=list_api_endpoint,
            query_params=query_params
            | {
                "limit": query_params.get("limit", None) or cls._default_limit,
                "offset": query_params.get("offset", None) or 0,
            },
        )

    def get_next_page_request_params(
        self,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> Optional[PaginationPageRequestParams]:
        if not self.is_next_page:
            return
        return PaginationPageRequestParams(url=self.next, query_params=query_params)

    def get_prev_page_request_params(
        self,
        list_api_endpoint: str,
        query_params: Optional[dict[str, str]] = None,
    ) -> Optional[PaginationPageRequestParams]:
        if not self.is_prev_page:
            return
        return PaginationPageRequestParams(url=self.previous, query_params=query_params)

    def get_page_results(self, model_class: Type) -> list[Any]:
        return [model_class(**instance_data) for instance_data in self.results]


class BaseAPISelector(BaseSelector[SelectorInstance], Generic[SelectorInstance]):
    list_api_endpoint: str
    list_api_endpoint_pagination_model: Optional[Type[BasePaginationModel]] = None
    entity_api_endpoint: str

    connection_timeout: Optional[float] = 10.0
    headers: dict[str, str] = {}

    @classmethod
    def client(cls) -> HttpxClient:
        return HttpxClient(
            headers=cls.headers,
            timeout=cls.connection_timeout,
        )

    @classmethod
    def async_client(cls) -> HttpxAsyncClient:
        return HttpxAsyncClient(
            headers=cls.headers,
            timeout=cls.connection_timeout,
        )

    @classmethod
    def get(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[SelectorInstance]:
        with cls.client() as client:
            endpoint = cls.entity_api_endpoint.format(**kwargs)
            response = client.get(endpoint, params=query_params)
            if response.status_code != 200:
                if raise_exception:
                    raise NotFoundError(
                        f"Error when trying get object (HTTP status code: {response.status_code}, response: {response.text}). "
                        f"Url: {endpoint}, {query_params=}, {kwargs=}"
                    )
                else:
                    return None
            return cls.model(**response.json())

    @classmethod
    async def aget(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[SelectorInstance]:
        async with cls.async_client() as client:
            endpoint = cls.entity_api_endpoint.format(**kwargs)
            response = await client.get(endpoint, params=query_params)
            if response.status_code != 200:
                if raise_exception:
                    raise NotFoundError(f"Error when trying get object. Url: {endpoint}, {query_params=}, {kwargs=}")
                else:
                    return None
            return cls.model(**response.json())

    @classmethod
    def list_get_all_g(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Iterable[SelectorInstance]:
        with cls.client() as client:
            endpoint = cls.list_api_endpoint.format(**kwargs)
            if cls.list_api_endpoint_pagination_model is None:
                response = client.get(endpoint, params=query_params)
                yield [cls.model(**model_data) for model_data in response.json()]
            else:
                request_params = cls.list_api_endpoint_pagination_model.get_first_page_request_params(
                    endpoint, query_params=query_params
                )
                response = client.get(request_params.url, params=request_params.query_params)
                page = cls.list_api_endpoint_pagination_model(**response.json())
                yield page.get_page_results(model_class=cls.model)
                while page.is_next_page:
                    request_params = page.get_next_page_request_params(cls.list_api_endpoint, query_params=query_params)
                    response = client.get(request_params.url, params=request_params.query_params)
                    page = cls.list_api_endpoint_pagination_model(**response.json())
                    yield page.get_page_results(model_class=cls.model)

    @classmethod
    def list_get_all(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[list[SelectorInstance]]:
        results = []
        for part in cls.list_get_all_g(query_params=query_params, raise_exception=raise_exception, **kwargs):
            results += part
        return results

    @classmethod
    async def alist_get_all_g(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> AsyncIterable[list[SelectorInstance]]:
        async with cls.async_client() as client:
            endpoint = cls.list_api_endpoint.format(**kwargs)
            if cls.list_api_endpoint_pagination_model is None:
                response = await client.get(endpoint, params=query_params)
                yield [cls.model(**model_data) for model_data in response.json()]
            else:
                request_params = cls.list_api_endpoint_pagination_model.get_first_page_request_params(
                    endpoint, query_params=query_params
                )
                response = await client.get(request_params.url, params=request_params.query_params)
                page = cls.list_api_endpoint_pagination_model(**response.json())
                yield page.get_page_results(model_class=cls.model)
                while page.is_next_page:
                    request_params = page.get_next_page_request_params(cls.list_api_endpoint, query_params=query_params)
                    response = await client.get(request_params.url, params=request_params.query_params)
                    page = cls.list_api_endpoint_pagination_model(**response.json())
                    yield page.get_page_results(model_class=cls.model)

    @classmethod
    async def alist_get_all(
        cls, *, query_params: Optional[dict[str, str]] = None, raise_exception: bool = False, **kwargs
    ) -> Optional[list[SelectorInstance]]:
        results = []
        async for part in cls.alist_get_all_g(query_params=query_params, raise_exception=raise_exception, **kwargs):
            results += part
        return results
