
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from enums.member_type import MemberType


class Member(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True)
    name: str
    password: str
    email: EmailStr
    phone: str
    type: MemberType
    create_date: datetime = Field(default_factory=datetime.now)
