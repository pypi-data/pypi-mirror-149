"""Feature monitoring related datastructures"""
from __future__ import annotations

import typing as t

from pydantic import BaseModel

from taktile_types.enums.monitor import MonitorSourceType, MonitorType


class MonitorData(BaseModel):
    """MonitorData of a tracked variable"""

    value: t.List[
        t.Any
    ]  # Specifying types here will influence pydantic's json rendering
    # https://github.com/samuelcolvin/pydantic/issues/2079
    type: MonitorType


class MonitorDataV2(MonitorData):
    """MonitorData of a tracked variable v2"""

    name: str
    source_type: MonitorSourceType


MonitorDataType = t.Union[t.Dict[str, MonitorData], t.List[MonitorDataV2]]


class MonitoringPayload(BaseModel):
    """MonitoringPayload is the payload sent over the wire to ingester"""

    version: int = 1
    data: MonitorDataType
    timestamp: int
    user_agent: t.Optional[str]
    endpoint: str
    git_sha: str
    git_ref: str
    repository_id: str

    @classmethod
    def parse(cls, values: t.Dict) -> MonitoringPayload:
        """Parses based on version"""
        if values.get("version") == 2:
            values["data"] = [
                MonitorDataV2(**row) for row in values.get("data", [])
            ]
        else:
            values["data"] = {
                k: MonitorData(**v) for k, v in values.get("data", {}).items()
            }
        return MonitoringPayload(**values)


class MonitoringIngesterPayload(BaseModel):
    """Payload sent over the wire to SNS Queue"""

    message_length: int
    environment: t.Optional[str]
    message: MonitoringPayload
