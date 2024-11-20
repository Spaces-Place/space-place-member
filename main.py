from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.member import member_router
from database import conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작될 때 실행할 코드
    conn()
    yield
    # 애플리케이션 종료될 때 실행할 코드 (필요 시 추가)


app = FastAPI(lifespan=lifespan, title="멤버 API", version="ver.1")

app.include_router(member_router, prefix="/api/v1/members")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용하는 URL 넣어야함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
