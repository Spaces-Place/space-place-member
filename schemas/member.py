
from pydantic import Field, EmailStr
from enums.member_type import MemberType
from schemas.common import BaseResponse


class MemberResponse(BaseResponse):
    user_id: str = Field(unique=True, description="사용자 아이디")
    name: str = Field(description="사용자 이름")
    email: EmailStr = Field(description="사용자 이메일")
    phone: str = Field(description="사용자 핸드폰 번호")
    type: MemberType = Field(description="사용자 타입")