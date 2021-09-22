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

class WordTypes(Enum):
	VERBE = auto()
	NOM = auto()
	ADJECTIF = auto()
	INTERJECTION = auto()
	ADVERBE = auto()
	INCONNUE = auto()

class WordStatus(Enum):
	WAITING = auto()
	VALIDATED = auto()
	REJECTED = auto()

# ========== AUTH =========

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

# ========== USER =========

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

# ========== INDOBEKO =========

class Indobeko(BaseModel):
	valeur:str
	sens_run:Optional[str]
	sens_fr:Optional[str]
	sens_en:Optional[str]
	run_by:Optional[str]
	fr_by:Optional[str]
	en_by:Optional[str]
	run_by:List[str]
	fr_by:List[str]
	en_by:List[str]
	date:Optional[date] = date.today

# ========== INGOBOTOZO =========

class Ingobotozo(BaseModel):
	valeur:str
	sens_run:Optional[str]
	sens_fr:Optional[str]
	sens_en:Optional[str]
	date:Optional[date] = date.today

# ========= MOTS =========

class Mot(BaseModel):
	mot:str
	categorie:WordTypes = WordTypes.INCONNUE
	singulars:List[str]
	plurals:List[str]
	imvugo:Imvugo
	base:str
	synonyme:List[str]
	sens_run:Optional[str]
	sens_fr:Optional[str]
	sens_en:Optional[str]
	run_by:Optional[str]
	fr_by:Optional[str]
	en_by:Optional[str]
	run_validated_by:Optional[str]
	fr_validated_by:Optional[str]
	en_validated_by:Optional[str]
	word_status:WordStatus = WordStatus.WAITING
	run_status:WordStatus = WordStatus.WAITING
	fr_status:WordStatus = WordStatus.WAITING
	en_status:WordStatus = WordStatus.WAITING
