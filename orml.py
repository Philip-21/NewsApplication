#creating the orm path
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
import config
from config import settings
#creating a connection string to pass to sql alchemy 
#SQLALCHEMY_DATABASE_URL= "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#creating an engine that connects sql alchemy to postgres
engine= create_engine(SQLALCHEMY_DATABASE_URL) 

#talking to SQL database
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

#defining the  baseclass i.e all the models used to craete our tables will be extending in baseclass
Base= declarative_base()










