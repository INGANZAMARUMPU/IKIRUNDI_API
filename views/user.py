from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import crud, schemas
from database.connection import get_db

from .authentication import login_required

router = APIRouter(
	prefix="/user",
	tags=["users"],
	# dependencies=[Depends(login_required)]
)

@router.get("/", response_model=List[schemas.User])
async def read(skip: int = 0, limit: int = 100,
				db: Session = Depends(get_db),
				token: str = Depends(login_required)):
	return crud.users.list(db, skip, limit)

@router.get("/{id}", response_model=schemas.User)
async def get(id:int, db: Session = Depends(get_db),
				token: str = Depends(login_required)):
	item = crud.users.get(db, id)
	if item is None:
		raise HTTPException(status_code=404, detail="Details not found")
	return item

@router.put("/{id}", response_model=schemas.User)
async def change(
		id:int, item:schemas.UserUpdate,
		db: Session = Depends(get_db),
		token: str = Depends(login_required)
	):
	old_user = crud.users.get(db, id)
	if old_user is None:
		raise HTTPException(status_code=404, detail="Details not found")
	return crud.users.update(db=db, old_user=old_user, item=item)

@router.post("/", response_model=schemas.User)
async def create(item:schemas.UserCreate,
				db: Session = Depends(get_db),
				token: str = Depends(login_required)):
	return crud.users.create(db=db, item=item)

@router.post("/superuser", response_model=schemas.User)
async def create_SuperUser(item:schemas.UserCreate, db: Session = Depends(get_db)):
	admin = crud.users.getAdmin(db)
	if admin is not None:
		raise HTTPException(status_code=403, detail="you must be an admin")
	item.is_admin=True
	return crud.users.create(db=db, item=item)