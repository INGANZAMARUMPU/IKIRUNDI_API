# a kind of serializers 
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
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
	role: Roles

class RefreshedToken(BaseModel):
	access_token: str
	token_type: str

class LoginForm(BaseModel):
	username: EmailStr
	password: str

# ========== USER =========

class UserBase(BaseModel):
	email: EmailStr
	fullname: Optional[str]

class UserEdit(UserBase):
	password: str

class User(UserBase):
	role: Roles = Roles.USER
	joined_date: date
	words: int = 0
	corrections: int = 0
	faults: int = 0
	is_admin:bool = False
	is_active:bool
	password:str

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

# ========== INGOBOTOZO =========

class Inyitangizo(BaseModel):
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
	word_status:WordStatus = WordStatus.WAITING

class SensRun(BaseModel):
	mot:str
	sens:Optional[str]
	by:Optional[str]
	status:WordStatus = WordStatus.WAITING
	validated_by:Optional[str]

class SensFr(BaseModel):
	mot:str
	sens:Optional[str]
	by:Optional[str]
	status:WordStatus = WordStatus.WAITING
	validated_by:Optional[str]

class SensEn(BaseModel):
	mot:str
	sens:Optional[str]
	by:Optional[str]
	status:WordStatus = WordStatus.WAITING
	validated_by:Optional[str]
