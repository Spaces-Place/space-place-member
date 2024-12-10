import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from models.member import Member
from schemas.common import BaseResponse
from schemas.sign import SignUp, SignIn, SignInResponse
from schemas.member import MemberResponse
from utils.authenticate import userAuthenticate
from utils.hash_password import HashPassword
from sqlmodel import select
from utils.jwt_handler import create_jwt_token
from utils.logger import Logger
from utils.mysqldb import get_mysql_session


member_router = APIRouter(tags=["사용자"])

hash_password = HashPassword()


# 회원가입
@member_router.post(
    "/sign-up",
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="사용자 회원가입",
)
async def sign_new_member(data: SignUp, session=Depends(get_mysql_session)) -> dict:
    statement = select(Member).where(Member.user_id == data.user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="동일한 사용자가 존재합니다."
        )

    new_member = Member(
        user_id=data.user_id,
        name=data.name,
        password=hash_password.hash_password(data.password),
        email=data.email,
        phone=data.phone,
        type=data.type,
    )
    session.add(new_member)
    await session.commit()
    return BaseResponse(message="정상적으로 가입되었습니다.")


# 로그인
@member_router.post("/sign-in", response_model=SignInResponse, summary="사용자 로그인")
async def sign_in(data: SignIn, session=Depends(get_mysql_session), logger: Logger = Depends(Logger.setup_logger)) -> dict:
    statement = select(Member).where(Member.user_id == data.user_id)
    result = await session.execute(statement)
    member = result.first()[0] # 튜플 형태임
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일치하는 사용자가 존재하지 않습니다.",
        )
    
    is_verified_pw = await asyncio.to_thread(hash_password.verify_password, data.password, member.password)

    if not is_verified_pw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="패스워드가 일치하지 않습니다.",
        )
    access_token = await asyncio.to_thread(create_jwt_token, member.user_id)

    return SignInResponse(
        message="로그인에 성공했습니다.",
        user_id=member.user_id,
        access_token=access_token,
    )


# 정보조회
@member_router.get(
    "/{user_id}", response_model=MemberResponse, summary="사용자 정보 조회"
)
async def get_user(
    user_id: str,
    session=Depends(get_mysql_session),
    token_info=Depends(userAuthenticate),
):
    statement = select(Member).where(Member.user_id == user_id)
    result = await session.execute(statement)
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일치하는 사용자가 존재하지 않습니다.",
        )
    # 토큰의 user_id랑 "/users/{user_id}"의 user_id 비교한 후 다르면 예외처리
    if token_info["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="자기 자신의 정보만 확인 가능합니다.",
        )

    return MemberResponse(
        message="유저 조회 완료.",
        user_id=member.user_id,
        name=member.name,
        email=member.email,
        phone=member.phone,
        type=member.type,
    )
