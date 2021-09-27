from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import instance, schemas
from couchbase.bucket import Bucket

router = APIRouter(
	prefix="/inyitangizo",
	tags=["inyitangizo"],
	# dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Inyitangizo)
async def create(item:schemas.Ingobotozo):
	bucket:Bucket = instance.getBucket("inyitangizo")
	bucket.insert(item.valeur, item.dict())
	return item