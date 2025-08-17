from fastapi import FastAPI,Depends,APIRouter,Body,HTTPException,status
from sqlalchemy.orm import Session
import  models,schemas,oauth2,DataBase
from datetime import datetime, timedelta
from typing import List

router = APIRouter(
    tags = ['tasks']
)


@router.get("/get/task",response_model  = List[schemas.ResponseToTask])
def get_tasks(db: Session  = Depends(DataBase.get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    tasks_all = db.query(models.Task)
    tasks = tasks_all.all()
    print(tasks)
    return tasks


@router.get("/get/task/{id}",response_model = schemas.ResponseToTask)
def get_task_id(id:int,db:Session = Depends(DataBase.get_db),current_user:models.User = Depends(oauth2.get_current_user)):

    exists = db.query(models.Task).filter(models.Task.id == id)
    task =  exists.first()
    if not exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"the details with the id: {id} is not present in the DB")
    return task


@router.post("/post/task",response_model = schemas.ResponseToTask)
def create_task(task: schemas.Task =Body(...), db:Session = Depends(DataBase.get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    payload = task.model_dump()
    minutes = payload['deadline']
    deadline_time = datetime.utcnow() + timedelta(minutes = minutes) 
      
    
                  # Pydantic v2; use .dict() if v1
    payload["deadline"] = deadline_time
    new_task = models.Task(**payload) 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    status_value = str(new_task.status)
    return {
        "id":new_task.id,
        "title":new_task.title,
        "description" : new_task.description,
        "status" : status_value,
        "deadline": new_task.deadline,
        "created_at": new_task.created_at,
        "user_id": new_task.user_id
    }




@router.put("/update/task/{id}",response_model = schemas.ResponseToTask)
def update_tasks(id: int, up_task: schemas.Task,db:Session = Depends(DataBase.get_db),current_user:models.User = Depends(oauth2.get_current_user)):

    payload = up_task.model_dump()
    minutes = payload['deadline']
    deadline_time = datetime.utcnow() + timedelta(minutes = minutes) 
    payload["deadline"] = deadline_time

    db_check = db.query(models.Task).filter(models.Task.id == id)
    to_update = db_check.first()
    # if not to_update:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail = f"Hey, before updating the task, can't you even check the id:'{id}', waste of my time for checking the database.")
    if to_update:
        un_pack = models.Task(**payload)
        db.add(un_pack)
        db.commit()
        db.refresh(un_pack)
        status = str(un_pack.deadline)
        return {
            'id':id,
            'title':un_pack.title,
            'description':un_pack.title,
            'status' : status,       
            'deadline': un_pack.deadline,
            'created_at': un_pack.created_at,  
            'user_id': un_pack.user_id          

        }





@router.delete("/delete/task/{id}")
def del_task_id(id:int, db:Session = Depends(DataBase.get_db),current_user:models.User = Depends(oauth2.get_current_user)):
    d = db.query(models.Task).filter(models.Task.id == id).first()
    if not d:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"the details with id: {id} is doesn't exists in the database")
    deleted = db.delete(d)
    db.commit()
    return f"gottcha, deleted the task with id: {id}"