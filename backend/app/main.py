from fastapi import FastAPI

from backend.app.api.v1.router import router
from backend.app.core.config import settings


app = FastAPI(title=settings.app_name)

app.include_router(router, prefix=settings.api_prefix)