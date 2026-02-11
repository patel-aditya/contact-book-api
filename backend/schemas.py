from pydantic import BaseModel, EmailStr
from typing import Optional

# shared Properties
class ContactBase(BaseModel):
    name: str
    phone: str
    email: EmailStr

# create a new contact
class ContactCreate(ContactBase):
    pass


# update a contact
class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


# returning data to client
class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
