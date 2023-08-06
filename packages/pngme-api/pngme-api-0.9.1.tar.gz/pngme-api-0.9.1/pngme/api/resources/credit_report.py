from abc import ABC
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import validate_arguments

from ..cache import cache
from ..core import BaseClient
from ..encoders import encode_query_params

PATH = "/creditreport/alternative"


CreditReport = Dict[str, Any]


class BaseCreditReportResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    @validate_arguments
    @cache
    async def _get(
        self, user_uuid: str, utc_time: Optional[datetime] = None
    ) -> CreditReport:
        async with self._client.session() as session:
            response = await session.get(
                PATH,
                params=encode_query_params(
                    user_uuid=user_uuid,
                    utc_time=utc_time,
                ),
            )

        assert response.status_code == 200, response.text
        credit_report: CreditReport = response.json()
        return credit_report


class AsyncCreditReportResource(BaseCreditReportResource):
    async def get(
        self, user_uuid: str, utc_time: Optional[datetime] = None
    ) -> CreditReport:
        return await self._get(
            user_uuid=user_uuid,
            utc_time=utc_time,
        )


class SyncCreditReportResource(BaseCreditReportResource):
    def get(self, user_uuid: str, utc_time: Optional[datetime] = None) -> CreditReport:
        return self._client.run(
            self._get(
                user_uuid=user_uuid,
                utc_time=utc_time,
            )
        )
