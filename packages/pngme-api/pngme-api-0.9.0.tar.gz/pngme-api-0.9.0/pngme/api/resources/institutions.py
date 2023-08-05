from abc import ABC
from typing import List, Optional

from pydantic import BaseModel, validate_arguments

from ..cache import cache
from ..core import BaseClient

PATH = "/users/{user_uuid}/institutions"


class Institution(BaseModel):
    institution_id: str
    display_name: str
    currency: Optional[str]
    account_ids: List[str]
    account_types: List[str]


class InstitutionsMeta(BaseModel):
    user_uuid: str
    client_uuid: str


class InstitutionsResponse(BaseModel):
    meta: InstitutionsMeta
    institutions: List[Institution]

    class Config:
        fields = {"meta": "_meta"}


class BaseInstitutionsResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    @validate_arguments
    @cache
    async def _get(self, user_uuid: str) -> List[Institution]:
        async with self._client.session() as session:
            response = await session.get(PATH.format(user_uuid=user_uuid))

        assert response.status_code == 200, response.text
        return InstitutionsResponse(**response.json()).institutions


class AsyncInstitutionsResource(BaseInstitutionsResource):
    async def get(self, user_uuid: str) -> List[Institution]:
        return await self._get(user_uuid)


class SyncInstitutionsResource(BaseInstitutionsResource):
    def get(self, user_uuid: str) -> List[Institution]:
        return self._client.run(self._get(user_uuid))
