import asyncio
from abc import ABC
from datetime import datetime
from typing import List, Optional, Sequence, Set

from pydantic import BaseModel, validate_arguments

from ..cache import cache
from ..core import BaseClient
from ..encoders import encode_query_params

PATH = "/users/{user_uuid}/institutions/{institution_id}/balances"


class BalanceRecord(BaseModel):
    description: Optional[str]
    balance: int
    ts: int
    currency: Optional[str]
    labels: Set[str]
    account_id: str
    account_type: Optional[str]


class BalancesMeta(BaseModel):
    page: int
    utc_starttime: Optional[datetime] = None
    utc_endtime: Optional[datetime] = None
    institution_id: str
    user_uuid: str
    total_balances_count: int
    max_pages: int
    client_uuid: str


class BalancesAccount(BaseModel):
    account_id: str
    account_type: Optional[str]
    records: List[BalanceRecord]


class BalancesResponse(BaseModel):
    meta: BalancesMeta
    balances: List[BalancesAccount]

    class Config:
        fields = {"meta": "_meta"}


class BaseBalancesResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    async def _get_page(
        self,
        user_uuid: str,
        institution_id: str,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
        page: int = 1,
    ) -> BalancesResponse:
        async with self._client.session() as session:
            response = await session.get(
                PATH.format(user_uuid=user_uuid, institution_id=institution_id),
                params=encode_query_params(
                    utc_starttime=utc_starttime,
                    utc_endtime=utc_endtime,
                    labels=labels,
                    account_types=account_types,
                    page=page,
                ),
            )

        assert response.status_code == 200, response.text
        return BalancesResponse(**response.json())

    @validate_arguments
    @cache
    async def _get(
        self,
        user_uuid: str,
        institution_id: str,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
    ) -> List[BalanceRecord]:
        response = await self._get_page(
            user_uuid=user_uuid,
            institution_id=institution_id,
            utc_starttime=utc_starttime,
            utc_endtime=utc_endtime,
            labels=labels,
            account_types=account_types,
        )
        max_pages = response.meta.max_pages
        if max_pages > 1:
            coroutines = [
                self._get_page(
                    user_uuid=user_uuid,
                    institution_id=institution_id,
                    utc_starttime=utc_starttime,
                    utc_endtime=utc_endtime,
                    labels=labels,
                    account_types=account_types,
                    page=page + 2,
                )
                for page in range(max_pages - 1)
            ]
            response_pages = await asyncio.gather(*coroutines)
            responses = (response, *response_pages)
        else:
            responses = (response,)

        return [
            record
            for response in responses
            for balance_account in response.balances
            for record in balance_account.records
        ]


class AsyncBalancesResource(BaseBalancesResource):
    async def get(
        self,
        user_uuid: str,
        institution_id: str,
        *,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
    ) -> List[BalanceRecord]:
        return await self._get(
            user_uuid=user_uuid,
            institution_id=institution_id,
            utc_starttime=utc_starttime,
            utc_endtime=utc_endtime,
            labels=labels,
            account_types=account_types,
        )


class SyncBalancesResource(BaseBalancesResource):
    def get(
        self,
        user_uuid: str,
        institution_id: str,
        *,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
    ) -> List[BalanceRecord]:
        return self._client.run(
            self._get(
                user_uuid=user_uuid,
                institution_id=institution_id,
                utc_starttime=utc_starttime,
                utc_endtime=utc_endtime,
                labels=labels,
                account_types=account_types,
            )
        )
