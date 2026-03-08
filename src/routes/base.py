from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_setting, Setting


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(app_setting: Setting = Depends(get_setting)):

    app_name = app_setting.APP_NAME
    app_version = app_setting.APP_VERSION

    return {
         "app_name": app_name,
         "app_version":app_version,
    }
