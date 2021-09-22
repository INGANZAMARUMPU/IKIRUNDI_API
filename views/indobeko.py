from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import schemas

router = APIRouter(
	prefix="/indobeko",
	tags=["indobeko"],
	# dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Indobeko)
async def create(item:schemas.Indobeko):
	return item