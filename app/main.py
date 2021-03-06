import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.courses import router as v1_course_router
from app.api.industry_standards import router as v1_standards_router
from app.api.user import router as v1_user_router

API_GATEWAY_STAGE_PREFIX = os.environ.get("STAGE_PREFIX", default="")
API_GATEWAY_SERVICE_PREFIX = os.environ.get("SERVICE_PREFIX", default="")

app = FastAPI(
    title="Training Provider Admin API",
    root_path=API_GATEWAY_STAGE_PREFIX,
    openapi_url=API_GATEWAY_SERVICE_PREFIX + "/openapi.json",
    docs_url=API_GATEWAY_SERVICE_PREFIX + "/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_user_router, prefix=API_GATEWAY_SERVICE_PREFIX)
app.include_router(v1_course_router, prefix=API_GATEWAY_SERVICE_PREFIX)
app.include_router(v1_standards_router, prefix=API_GATEWAY_SERVICE_PREFIX)
