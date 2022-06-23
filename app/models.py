#creating a model for our database
from sqlalchemy import Column, Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base): #base is a model to create table,columns,describes how our table lok like
    __tablename__ = "newspost" #primary key ia a column that uniquely identifies each row in a table

    id= Column(Integer,primary_key=True,nullable=False) #primary key ia a column that uniquely identifies each row in a table
    title= Column(String,nullable=False)
    content= Column(String,nullable=False)
    comments= Column(String, nullable=True)
    published= Column(Boolean, default=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()")) #time post is created 
    owner_id= Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) #users.id references the table name of users ,cascade deletes all the posts by a particular user based on the id
    owner=relationship("User") #creates a property for newspost when a post is retieved it fetches the users based on the owner_id and creates a relationship btwn the classes




class User(Base): #creating a table for user registration 
    __tablename__="users"
    id= Column(Integer,primary_key=True,nullable=False)
    email= Column(String, nullable=False, unique=True)#unique prevents one email from registering twice
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()")) #time post is created   



class Vote(Base): #creating a table for likes 
    __tablename__="votes"
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True) #foreign key is referencing the users table an grabbing the id field 
    post_id= Column(Integer, ForeignKey("newspost.id", ondelete="CASCADE"),primary_key=True)



 

