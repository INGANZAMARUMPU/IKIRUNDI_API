from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import instance, schemas
from couchbase.bucket import Bucket

router = APIRouter(
	prefix="/ingobotozo",
	tags=["ingobotozo"],
	# dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Ingobotozo)
async def create(item:schemas.Ingobotozo):
	bucket:Bucket = instance.getBucket("ingobotozo")
	bucket.insert(item.valeur, item.dict())
	return item