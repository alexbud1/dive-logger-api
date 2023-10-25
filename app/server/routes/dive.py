from fastapi import APIRouter, Body, Response, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from server.logging.logging import logger
from server.models.dive import Dive
from server.schemas.dive import (
    DiveSchema,
)
from server.security.tokens import verify_token
from fastapi import status
import json
from server.database.database import database
from fastapi_pagination import Page, add_pagination, paginate

router = APIRouter()

@router.post("/", response_description="Dive data added into the database", status_code=status.HTTP_201_CREATED, response_model=DiveSchema)
async def add_dive_data(dive: DiveSchema = Body(...), token: str = Depends(verify_token)):
    """
    Saving dive data into database and returning the saved data.
    """
    dive = jsonable_encoder(dive)
    diver_id = await database.user_profiles.find_one({"telegram_id": dive["telegram_id"]})
    dive["diver_id"] = diver_id["_id"]

    new_dive = Dive(dive)
    await new_dive.save()
    logger.info(f"NEW DIVE: {new_dive.__repr__}")
    
    return JSONResponse(
        content=new_dive.to_json(), status_code=status.HTTP_201_CREATED
    )

@router.get("/{telegram_id}", response_description="Dive data retrieved by users telegram_id", response_model=Page[DiveSchema], status_code=status.HTTP_200_OK)
async def get_dive_data(telegram_id: int, token: str = Depends(verify_token)):
    """
    Retrieving dive data from database by users telegram_id.
    """
    dives = await Dive.get_documents_by_field("telegram_id", str(telegram_id))
    print(dives)
    if not dives:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dives with telegram_id {telegram_id} of Diver not found",
        )
    for dive in dives:
        dive["_id"] = str(dive["_id"])
    # return JSONResponse(
    #     content=dives, status_code=status.HTTP_200_OK
    # )
    return paginate(dives)
