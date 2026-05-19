from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime

class Task(Base):
    '''Class Task'''
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    descrip = Column(String)
    category = Column(String, default="General")
    statue = Column(String,default="Pending")
    created_at = Column(String)
    due_date = Column(String)

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE")) # penghubung ke user
    
    priority = Column(String,nullable=False,default="Medium")
    updated_at = Column(DateTime,nullable=False,default=datetime.now, onupdate=datetime.now)

    user = relationship("User",back_populates="task") # conect -> user.task

    def __repr__(self):
        return f"<status update: {self.updated_at}>"

class User(Base):
    '''Class user'''
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    role = Column(String,default="user")

    task = relationship("Task",back_populates="user",cascade="all,delete-orphan") # conect -> task.user

    def __repr__(self):
        return f"<usernam: {self.username}> | <role: {self.role}>"
