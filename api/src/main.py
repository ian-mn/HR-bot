import uvicorn
from core.config import get_config
from db import auth_storage
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import auth

config = get_config()

app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    auth_storage.auth_storage = auth_storage.RedisStorage(
            host=get_config().redis_host,
            port=get_config().redis_port,
    )


@app.on_event("shutdown")
async def shutdown():
    await auth_storage.auth_storage.close()


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8010, reload=True)
