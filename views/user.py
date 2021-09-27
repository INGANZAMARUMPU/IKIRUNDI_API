from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from couchbase.bucket import Bucket
from couchbase import exceptions
from datetime import date; import time
from database import instance, schemas

from . import authentication as Auth

router = APIRouter(
	prefix="/user",
	tags=["users"],
	dependencies=[Depends(Auth.login_required)]
)

# @router.get("/", response_model=List[schemas.User])
# async def read(skip: int = 0, limit: int = 100,
# 				db: Session = Depends(get_db),
# 				token: str = Depends(login_required)):
# 	return crud.users.list(db, skip, limit)

# @router.get("/{id}", response_model=schemas.User)
# async def get(id:int, db: Session = Depends(get_db),
# 				token: str = Depends(login_required)):
# 	item = crud.users.get(db, id)
# 	if item is None:
# 		raise HTTPException(status_code=404, detail="Details not found")
# 	return item

# @router.put("/{id}", response_model=schemas.User)
# async def change(
# 		id:int, item:schemas.UserUpdate,
# 		db: Session = Depends(get_db),
# 		token: str = Depends(login_required)
# 	):
# 	old_user = crud.users.get(db, id)
# 	if old_user is None:
# 		raise HTTPException(status_code=404, detail="Details not found")
# 	return crud.users.update(db=db, old_user=old_user, item=item)

@router.post("/", response_model=schemas.User)
async def register(item:schemas.UserEdit):
	user_dict = item.dict()

	user_dict["role"] = schemas.Roles.USER.value
	user_dict["joined_date"] = time.time()
	user_dict["words"] = 0
	user_dict["corrections"] = 0 
	user_dict["faults"] = 0
	user_dict["is_admin"] = False
	user_dict["is_active"] = True
	user_dict["password"] = Auth.get_password_hash(item.password)

	bucket:Bucket = instance.getBucket("users")
	try:
		bucket.insert(item.email, user_dict)
	except exceptions.DocumentExistsException:
		raise HTTPException(status_code=403, detail="Utilisateur déjà existant")

	return user_dict
