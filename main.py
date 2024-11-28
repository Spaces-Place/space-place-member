from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware


from routers.member import member_router
from utils.database_config import DatabaseConfig
from utils.mysqldb import MySQLDatabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan started")
    # 애플리케이션 시작될 때 실행할 코드
    env_type = '.env.development' if os.getenv('APP_ENV') == 'development' else '.env.production'
    load_dotenv(env_type)
    
    database = DatabaseConfig().create_database()
    await database.initialize()

    yield

    # 애플리케이션 종료될 때 실행할 코드 (필요 시 추가)
    await database.close()


app = FastAPI(lifespan=lifespan, title="멤버 API", version="ver.1")

health_router = APIRouter()
app.include_router(member_router, prefix="/api/v1/members")
app.include_router(health_router)

@health_router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    return {"status": "ok"}  # {"status": "ok"}로 200 OK 응답을 반환합니다.

@app.get("/", status_code=status.HTTP_200_OK)
async def root_check() -> dict:
    return {"message": "Welcome to the API!"}

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
