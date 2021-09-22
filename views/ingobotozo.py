from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import schemas

router = APIRouter(
	prefix="/ingobotozo",
	tags=["ingobotozo"],
	# dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Ingobotozo)
async def create(item:schemas.Ingobotozo):
	return item