from pydantic import BaseModel,EmailStr
from datetime import datetime, timedelta#time delta for creating expiration for jwt 
from pydantic.types import conint #library for validating particular figure(e.g 0 & 1) 
from  typing import Optional




class PostBase(BaseModel):#declaring Post as data model which is the pydantic model or schema
    title: str
    content: str 
    comments: str 
    

#creating a model for a  user to register 
class UserCreate(BaseModel):
    email:EmailStr
    password:str


#creating a model for users to login
class UserLogin(UserCreate):
    pass

# schema for post request for creating  posts
class CreatePost(PostBase): 
    pass


 # schema for put request for updating posts    
class UpdatePost(BaseModel):
    title: str
    content: str 
    comments: str 

#schema for liking a post
class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)#<=1

#creating a user response schema for the client ,so password wont be viewed (signing up)
class Userresponse(BaseModel): 
    id:int
    email:EmailStr
    class Config:
        orm_mode= True #pydantic orm_mode tells the pydantic model to read the data even if its not a dictionary ,cause it passed as the response model in the api function  

#creating a response from the API to the User, 
class Postresponse(BaseModel):
    id:int
    title:str
    content: str
    comments: str
    published : bool = True#defining if a user publishes a post  
    created_at:datetime
    owner_id:int #foreign key that will generate the id of the users who login/signup  when they create a post
    owner: Userresponse #this will give the information of the owner of a particular post

    class Config:
        orm_mode= True #pydantic orm_mode tells the pydantic model to read the data even if its not a dictionary 


#schema to implement likes/vote to a post when an individual searches a user 
class PostOut(BaseModel):
    Post:Postresponse #post response gives the full detail of the user
    likes:int 
    class Config:
        orm_mode= True 

#schema for token
class Token(BaseModel):
    access_token:str
    token_type:str



#schema embedded into the  data of access_token
class TokenData(BaseModel): 
    id:Optional[str]=None
