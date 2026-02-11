from fastapi import FastAPI, Depends
from database import engine, session
from schemas import Contact, ContactBase, ContactCreate, ContactUpdate
from sqlalchemy.orm import Session
from typing import List

import models

app = FastAPI()


# create database Tables
models.Base.metadata.create_all(bind = engine)

# database session provider
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# save contact
@app.post("/contacts", response_model= ContactCreate)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# can see all contacts
@app.get("/contacts")
def get_all_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

# update contacts
@app.patch("/contacts/{contact_id}",response_model= ContactUpdate)
def update_contact(contact_id: int, updated: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    
    if not contact:
        return "Contact not found"
    
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact


# delete contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()

    if contact:
        db.delete(contact)
        db.commit()
        return "contact Deleted"    
    return "Contact not found"


# search using name
@app.get("/contacts/search", response_model= List[Contact])
def search_contacts(name: str, db: Session = Depends(get_db)):
    result = db.query(models.Contact).filter(models.Contact.name.ilike(f"%{name}%")).all()

    return result





    

