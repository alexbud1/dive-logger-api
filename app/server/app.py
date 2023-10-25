from fastapi import FastAPI
from server.database.database import database
from server.routes.user_profile import router as UserProfileRouter
from server.routes.dive import router as DiveRouter
from server.logging.logging import logger
from fastapi_pagination import add_pagination

app = FastAPI()

add_pagination(app)

app.include_router(UserProfileRouter, tags=["UserProfile"], prefix="/user_profile")
app.include_router(DiveRouter, tags=["Dive"], prefix="/dive")


@app.on_event("startup")
async def startup_db_client():
    await database.connect()
    if database.is_connected():
        logger.info("<------------  MongoDB connection established  ------------>")
    else:
        logger.warning("<------------  MongoDB connection FAILED  ------------>")


@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down FastApi application")
    await database.close_connection()