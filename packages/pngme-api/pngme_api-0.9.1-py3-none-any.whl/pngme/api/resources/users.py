import asyncio
from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validate_arguments

from ..cache import cache
from ..core import BaseClient
from ..encoders import encode_query_params

PATH = "/users"


class User(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: str
    primary_phone_number: str
    primary_phone_imei: Optional[str]
    secondary_phone_number: Optional[str]
    secondary_phone_imei: Optional[str]
    is_kyc_verified: bool
    device_id: str
    external_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    country_code: str


class UsersMeta(BaseModel):
    client_uuid: str
    created_before: datetime
    created_after: datetime
    search: str
    total_users_count: int
    page: int
    max_pages: int


class UsersResponse(BaseModel):
    meta: UsersMeta
    users: List[User]

    class Config:
        fields = {"meta": "_meta"}


class BaseUsersResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    async def _get_page(
        self,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
        page: int = 1,
    ) -> UsersResponse:
        async with self._client.session() as session:
            response = await session.get(
                PATH,
                params=encode_query_params(
                    created_after=created_after,
                    created_before=created_before,
                    search=search,
                    page=page,
                ),
            )

        assert response.status_code == 200, response.text
        return UsersResponse(**response.json())

    @validate_arguments
    @cache
    async def _get(
        self,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> List[User]:
        response = await self._get_page(
            created_after=created_after,
            created_before=created_before,
            search=search,
        )
        max_pages = response.meta.max_pages
        if max_pages > 1:
            coroutines = [
                self._get_page(
                    created_after=created_after,
                    created_before=created_before,
                    search=search,
                    page=page + 2,
                )
                for page in range(max_pages - 1)
            ]
            response_pages = await asyncio.gather(*coroutines)
            responses = (response, *response_pages)
        else:
            responses = (response,)

        return [user for response in responses for user in response.users]


class AsyncUsersResource(BaseUsersResource):
    async def get(
        self,
        *,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> List[User]:
        return await self._get(
            created_after=created_after,
            created_before=created_before,
            search=search,
        )


class SyncUsersResource(BaseUsersResource):
    def get(
        self,
        *,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> List[User]:
        return self._client.run(
            self._get(
                created_after=created_after,
                created_before=created_before,
                search=search,
            )
        )
