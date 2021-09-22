# a kind of serializers 
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum, auto

class Roles(Enum):
	ADMIN = "admin"
	USER = "user"
	LITTERAIRE = "litteraire"
	ENSEIGNENT = "enseignent"

class WordTypes(Enum):
	VERBE = "verbe"
	NOM = "nom"
	ADJECTIF = "adjectif"
	INTERJECTION = "interjection"
	ADVERBE = "adverbe"
	INCONNUE = "inconnue"

class WordStatus(Enum):
	WAITING = auto()
	VALIDATED = auto()
	REJECTED = auto()

class Imvugo(Enum):
	IKAKAMISHA = "ikakamisha"
	ITUVYA = "ituvya"
	ISANZWE = "isanzwe"

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
	fullname: Optional[str]

class UserCreate(UserBase):
	password: str

class UserUpdate(UserBase):
	role: Optional[Roles] = Roles.USER
	joined_date: Optional[date]
	words: Optional[int] = 0
	corrections: Optional[int] = 0
	faults: Optional[int] = 0
	is_admin:Optional[bool] = False
	is_active:Optional[bool] = True
	password:Optional[str]

class User(UserBase):
	id: int
	role: Optional[Roles] = Roles.USER
	joined_date: Optional[date]
	words: Optional[int] = 0
	corrections: Optional[int] = 0
	faults: Optional[int] = 0
	is_admin:Optional[bool] = False
	is_active:Optional[bool] = True

# ========== INDOBEKO =========

class Indobeko(BaseModel):
	valeur:str
	sens_run:Optional[List[Optional[str]]] = None
	sens_fr:Optional[List[Optional[str]]] = None
	sens_en:Optional[List[Optional[str]]] = None

# ========== INGOBOTOZO =========

class Ingobotozo(BaseModel):
	valeur:str
	sens_run:List[str]
	sens_fr:List[str]
	sens_en:List[str]

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
