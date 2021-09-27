from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from database import instance, schemas
from couchbase.bucket import Bucket
from .authentication import login_required

router = APIRouter(
	prefix="/indobeko",
	tags=["indobeko"],
	dependencies=[Depends(login_required)]
)

@router.post("/", response_model=schemas.Indobeko)
async def create(item:schemas.Indobeko):
	bucket:Bucket = instance.getBucket("indobeko")
	bucket.insert(item.valeur, item.dict())
	return item