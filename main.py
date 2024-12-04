from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from routers.member import member_router
from utils.database_config import DatabaseConfig
from utils.mysqldb import MySQLDatabase


log_dir = Path("/var/log/spaceplace/member")
log_dir.mkdir(parents=True, exist_ok=True)

logging.config.fileConfig('log.conf', encoding="utf-8")
logger = logging.getLogger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan started")
    # 애플리케이션 시작될 때 실행할 코드
    env_type = (
        ".env.development"
        if os.getenv("APP_ENV") == "development"
        else ".env.production"
    )
    load_dotenv(env_type)

    database = DatabaseConfig().create_database()
    await database.initialize()

    yield

    # 애플리케이션 종료될 때 실행할 코드 (필요 시 추가)
    await database.close()


app = FastAPI(lifespan=lifespan, title="멤버 API", version="ver.1")

app.include_router(member_router, prefix="/api/v1/members")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    return {"status" : "ok"}

FastAPIInstrumentor.instrument_app(app)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


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
