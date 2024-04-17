from motor.motor_asyncio import AsyncIOMotorClient

from .db import MONGO_CONFIG


def create_async_mongo_client():
    return AsyncIOMotorClient(MONGO_CONFIG.build_uri())
