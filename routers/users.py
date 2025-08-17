from fastapi import FastAPI,Depends,APIRouter,HTTPException,Body
from typing import Annotated,Optional,List
from DataBase import get_db
from sqlalchemy.orm import Session
import models,schemas,utils


router = APIRouter(
    tags = ['users']
)

@router.get("/get/user",response_model = List[schemas.ResponseToUser])
def get_user_inf(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post("/post/user",response_model = schemas.ResponseToUser)
def create_user(user: schemas.User = Body(...) , db: Session = Depends(get_db)):
    


    exists = db.query(models.User).filter(models.User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")
    
    payload = user.model_dump() 
    hash = utils.hash(payload['password'])
    payload['password']  = hash
    print(payload['password'])
    #for example, what happens in the fastapi hood
    #payload = user.model_dump()      # -> {'username': 'mintu', 'email': 'x@x.com', ...}
    
    new_user = models.User(**payload)

    #it takes each key/value pair in payload and passes them as keyword arguments to models.User.__init__, equivalent to:
    #ex: models.User(username='mintu', email='x@x.com', ...)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/get/user/{id}",response_model = schemas.ResponseToUser)
def get_user_id(id: int, db: Session = Depends(get_db)):

    data = db.query(models.User).filter(models.User.id == id).first()
    #user = data.first()

    if not data:
        raise HTTPException(status_code= 404,detail =  f"the id: {id} doesn't exist in the DB" )
    db.commit()
    return data


@router.delete("/delete/user/{id}")
def delete_user(id,db:Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.id == id)
    user_to_delete = exists.first()
    if not exists:
        raise HTTPException(status_code = 404,detail = f"there is no user with '{id}', please check the details correctly")
    db.delete(user_to_delete)
    db.commit()
    return HTTPException(status_code = 204,detail = f"the user with '{id}', fortunately deleted.")




# @router.delete("/delete/user/{id_name_email}")
# def delete_user(id_name_email: str,db:Session = Depends(get_db)):
#     exists = db.query(models.User).filter(models.User.id == int(id_name_email) or models.User.username == id_name_email or models.User.email == id_name_email)
#     user_to_delete = exists.first()
#     if not exists:
#         raise HTTPException(status_code = 404,detail = f"there is no user with '{id_name_email}', please check the details correctly")
#     db.delete(user_to_delete)
#     db.commit()
#     return HTTPException(status_code = 204,detail = f"the user with '{id_name_email}, fortunately deleted.")