# a kind of serializers 
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum, auto

class Roles(Enum):
	ADMIN = auto()
	USER = auto()
	LITTERAIRE = auto()
	ENSEIGNENT = auto()

class Token(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	username: str
	group:str

class RefreshedToken(BaseModel):
	access_token: str
	token_type: str

class LoginForm(BaseModel):
	username: str
	password: str

class UserBase(BaseModel):
	email: str
	firstname: Optional[str]
	lastname: Optional[str]
	role: Optional[Roles] = Roles.USER
	words: Optional[int] = 0
	joined_date: Optional[date] = date.today
	words: Optional[int] = 0
	corrections: Optional[int] = 0
	faults: int
	is_admin:Optional[bool] = False
	is_active:Optional[bool] = True

class UserCreate(UserBase):
	password: str

class UserUpdate(UserBase):
	password:Optional[str]

class User(UserBase):
	id: int
	is_active: bool


