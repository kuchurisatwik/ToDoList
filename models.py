from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Date,Boolean,DateTime,ForeignKey,TIMESTAMP,CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from datetime import datetime,timedelta
from sqlalchemy.sql.expression import text
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String,nullable = True,unique = True)
    email = Column(String,nullable = False,unique = True)
    password = Column(String, nullable = False, unique = True)
    created_at = Column(TIMESTAMP(timezone = True),
                        nullable = False,server_default = text("now()"))
    
    

class Task(Base):
    __tablename__ = 'tasks'
    
    # TASK_STATUSES = [
    #     ('pending', 'Pending'),
    #     ('in-progress', 'In Progress'),
    #     ('completed', 'Completed')
    # ]
    id = Column(Integer,primary_key = True)
    title= Column(String,nullable = False)
    description = Column(String, nullable = True)
    status = Column(String,nullable = False, default='pending')
    deadline = Column(DateTime,nullable = False,server_default = text("now()"))
    user_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"),nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),
                        nullable = False, server_default= text('now()'))
    # Many orders -> one user
    user = relationship("User")

    __table_args__ = (
        CheckConstraint(status.in_(['pending','in-progress','completed']),name = 'check_task_status'),
    )






    #relationship() is used to define how two ORM-mapped classes are related in 
    # terms of database relationships (one-to-many, many-to-one, many-to-many).