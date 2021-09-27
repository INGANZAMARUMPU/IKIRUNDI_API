from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import instance, schemas
from couchbase.bucket import Bucket

router = APIRouter(
	prefix="/indobeko",
	tags=["indobeko"],
	# dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Indobeko)
async def create(item:schemas.Indobeko):
	bucket:Bucket = instance.get_bucket("indobeko")
	bucket.insert(item.valeur, item.dict())
	return item