"""Request Scope related datastructures"""
import typing as t

from pydantic import BaseModel, Field, validator

from taktile_types.enums.http import Method


class Headers(BaseModel):
    """HTTP Request Header Information"""

    user_agent: str = Field("", alias="user-agent")
    x_github_delivery: str = Field("", alias="x-github-delivery")

    @validator("user_agent")
    def trunc(cls, val):  # pylint: disable=no-self-use,no-self-argument
        """Trims lengthy browser user-agents"""
        if val:
            return val.split()[0]
        return val


class Scope(BaseModel):
    """HTTP Request Scope Information"""

    client: t.Tuple[str, str] = ("", "")
    method: Method = Method.GET
    path: str = ""
    type: str = ""
    http_version: str = ""

    @validator("type")
    def uppercase(cls, val):  # pylint: disable=no-self-use,no-self-argument
        """Turns to upper case"""
        if val:
            return val.upper()
        return val

    def get_client(self) -> str:
        """Concatenates client information"""
        return f"{self.client[0]}:{self.client[1]}"
