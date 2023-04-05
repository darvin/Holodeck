# flake8: noqa E501
from asyncio import get_event_loop
from typing import TYPE_CHECKING, Awaitable

from .. import models as m

if TYPE_CHECKING:
    from ..api_client import ApiClient


class _DefaultApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_route_generate_image_image_get(self, prompt: str, negative_prompt:str,  api_token: str) -> Awaitable[m.Any]:
        query_params = {"prompt": str(prompt), "negative_prompt": str(negative_prompt), "api_token": str(api_token)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/image",
            params=query_params,
        )

    def _build_for_route_generate_image_verified_image_verified_get(
        self, prompt: str, negative_prompt: str, api_token: str, max_attempts: int = None
    ) -> Awaitable[m.Any]:
        query_params = {
            "prompt": str(prompt),
            "api_token": str(api_token),
            "negative_prompt": str(negative_prompt),
        }
        if max_attempts is not None:
            query_params["max_attempts"] = str(max_attempts)

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/image_verified",
            params=query_params,
        )

    def _build_for_route_root_get(
        self,
    ) -> Awaitable[m.Any]:
        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/",
        )


class AsyncDefaultApi(_DefaultApi):
    async def route_generate_image_image_get(self, prompt: str, negative_prompt:str, api_token: str) -> m.Any:
        return await self._build_for_route_generate_image_image_get(prompt=prompt, negative_prompt=negative_prompt, api_token=api_token)

    async def route_generate_image_verified_image_verified_get(
        self, prompt: str, negative_prompt:str, api_token: str, max_attempts: int = None
    ) -> m.Any:
        return await self._build_for_route_generate_image_verified_image_verified_get(
            prompt=prompt, negative_prompt=negative_prompt, api_token=api_token, max_attempts=max_attempts
        )

    async def route_root_get(
        self,
    ) -> m.Any:
        return await self._build_for_route_root_get()


class SyncDefaultApi(_DefaultApi):
    def route_generate_image_image_get(self, prompt: str, negative_prompt:str,  api_token: str) -> m.Any:
        coroutine = self._build_for_route_generate_image_image_get(prompt=prompt, negative_prompt=negative_prompt, api_token=api_token)
        return get_event_loop().run_until_complete(coroutine)

    def route_generate_image_verified_image_verified_get(
        self, prompt: str, negative_prompt:str,  api_token: str, max_attempts: int = None
    ) -> m.Any:
        coroutine = self._build_for_route_generate_image_verified_image_verified_get(
            prompt=prompt, negative_prompt=negative_prompt, api_token=api_token, max_attempts=max_attempts
        )
        return get_event_loop().run_until_complete(coroutine)

    def route_root_get(
        self,
    ) -> m.Any:
        coroutine = self._build_for_route_root_get()
        return get_event_loop().run_until_complete(coroutine)
