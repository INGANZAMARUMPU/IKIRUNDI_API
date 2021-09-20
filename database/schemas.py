# a kind of serializers 
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field

class Token(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str
	username: str
	group:str
	is_validator:bool

class RefreshedToken(BaseModel):
	access_token: str
	token_type: str

class LoginForm(BaseModel):
	username: str
	password: str

class UserBase(BaseModel):
	username: str
	firstname: str
	lastname: str
	group: int
	is_validator:bool
	is_admin:Optional[bool] = False

class UserCreate(UserBase):
	password: str

class UserUpdate(UserBase):
	password:Optional[str]

class User(UserBase):
	id: int
	is_active: bool

	class Config:
		orm_mode = True

class ContribuableCreate(BaseModel):
	firstname: str
	lastname: str
	telephone: Optional[str] = None
	CNI: Optional[str] = None
	details: Optional[str] = None

class Contribuable(ContribuableCreate):
	id: int
	is_active: bool

	class Config:
		orm_mode = True

class ModePaymentCreate(BaseModel):
	nom:str
	days:int
	reduction:float = Field(ge=0, le=0.5)
	details:str

class ModePayment(ModePaymentCreate):
	id:int

	class Config:
		orm_mode = True

class CategorieCreate(BaseModel):
	nom:str
	ponderation:int
	details:str

class Categorie(CategorieCreate):
	id:int
	validated_by_id:int=None

	class Config:
		orm_mode = True
		# validated_by = User.username

class BienCreate(BaseModel):
	lieu:str
	numero:str
	nom:str
	details:str
	categorie_id:int

class Bien(BienCreate):
	id:int
	is_active:bool
	mode_payment:Optional[ModePayment] = None
	contribuable:Optional[Contribuable] = None
	categorie:Optional[Categorie]=None
	date_affectation:Optional[date]=None

	class Config:
		orm_mode = True

class Recouvrement(BaseModel):
	id:int
	bien_id:int
	contribuable_id:int
	verified_by_id:Optional[int]
	somme:int
	maximum:int
	auto_created_at:Optional[date] = date.today()
	end_at:Optional[date] = None
	satisfied_at:Optional[datetime] = None
	bien:Bien
	contribuable:Contribuable
	verified_by:Optional[User]

	class Config:
		orm_mode = True

class Affectation(BaseModel):
	mode_payment_id:int
	contribuable_id:int
	details:str
	from_date:Optional[date] = date.today()

class OutilsCreate(BaseModel):
	nom:str
	pages:int
	escompte:int
	details:str

class Outils(OutilsCreate):
	id:int
	quantite:int

	class Config:
		orm_mode = True

class AchatCreate(BaseModel):
	outils_id:int
	prix:int
	quantite:int
	first_page:int
	last_page:int
	details:str
	date:Optional[date]

class Achat(BaseModel):
	id:int
	outils_id:int
	outils:Outils
	prix:int
	first_page:int
	last_page:int
	details:str
	date:Optional[date]
	pages_filled:int
	verified_by_id:int=None
	date_filled:Optional[date]=None

	class Config:
		orm_mode = True

class Distribution(BaseModel):
	percepteur_id:int
	fullname:Optional[str]
	items:Optional[list]
	lieu:str

class PercepteurCreate(BaseModel):
	nom:str
	prenom:str
	CNI:str
	telephone:int
	details:str

class Percepteur(PercepteurCreate):
	id:int

	class Config:
		orm_mode=True

class PerceptionCreate(BaseModel):
	revenue:int
	start_page:int
	end_page:int

class Perception(PerceptionCreate):
	id:int
	achat_id:int
	numero:str
	lieu:Optional[str]
	verified_by:User=None
	percepteur_id:int
	percepteur:Percepteur
	achat:Achat
	date:Optional[date]

	class Config:
		orm_mode=True

class DetailsRecouvrementCreate(BaseModel):
	recouvrement_id:int
	quitance_no:int
	somme:int
	date:Optional[date]

class DetailsRecouvrement(DetailsRecouvrementCreate):
	id:int
	verified_by:Optional[User]=None
	actor:User

	class Config:
		orm_mode=True

