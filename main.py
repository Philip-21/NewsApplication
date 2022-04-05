import models
import orml
from orml import Base#importin base model from sql alchemy
from fastapi import FastAPI, Response,status,HTTPException,Depends
from fastapi.params import Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #retrieving users credentials in login route
from fastapi.security import OAuth2PasswordBearer 
from orml import engine,SessionLocal,Base
from sqlalchemy.orm import Session #establishes conversation btwn the database and program
from sqlalchemy import func 
from models import Post
from pydantic import BaseModel,EmailStr,BaseSettings
from datetime import datetime, timedelta#time delta for creating expiration for jwt 
from typing import Optional,List
from passlib.context import CryptContext #library for creating hashing path
from jose import JWTError, jwt #libraray for creating a token 
import config
from config import settings
from pydantic.types import conint #library for validating particular figure(e.g 0 & 1) 
from fastapi.middleware.cors import CORSMiddleware


app =FastAPI(
    prefix="/users",
    tags=['Users','Authenticaion']
) #organizing the api docuentation
origins=["*"]#providing list of domains that should talk to our api,[*] every kind of domain that can talk to our api

app.add_middleware(#middleware is a function that runs before every request
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],#for specific http methods
allow_headers=["*"],#for specific headers
)

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



#models.Base.metadata.create_all(bind=engine)#create and connect all of our models (tables)


def get_db():
    db = SessionLocal()#Session object is responsible for talking to  the databases
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome():
    return {'message':"newspost"}


#some random operations to test our api
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)): #creates session to the database to perform some operations and closes once the request is done
    posts= db.query(models.Post)#parsing a specific model for the table we want to query, query()performs the sql select statement
    print(posts)
    return {'data':"successful"}


#using bcrypt as an hashing  algorithm for passwords stored in the database to prevent hackers
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash (password:str):
    return pwd_context.hash(password)
#a verified func to compare the plain passsword attempt then hashing it and compare it to the hashed password in the database 
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


#creating a func for JWT token 
SECRET_KEY= settings.secret_key
ALGORITHM= settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes
def create_access_token(data:dict): #data we want to encode into the token is passed as dict
    to_encode=data.copy()#data we encode in our jwt token (to_encode)
    expiretime= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#creating the expiration field
    to_encode.update({"exp":expiretime})#adding expiretime into the data we encode in our jwt token (to_encode)
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)#creating the jwt token (HEADER(algotithm)& SIGNATURE(secret_key) HAS BEEN CREATED )
    return encoded_jwt

#creating a new path operation for the user to send its registeration details(signing up)
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=Userresponse)
def create_user(user: UserCreate,db:Session = Depends(get_db)):
    hashed_password=hash(user.password)#hashing the paswword and storing it in user.password
    user.password= hashed_password #making it automatically update in the pydantic model
    new_user=models.User(**user.dict()) #converting user : UserCreate to a dictionary
    db.add(new_user) #add a brand newpost to our database 
    db.commit() #commit it to our db
    db.refresh(new_user)#restores the user  into the variable of new_user
    return new_user


#schema for token
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login") #the url endpoint
class Token(BaseModel):
    access_token:str
    token_type:str
#schema embedded into the  data of access_token
class TokenData(BaseModel): 
    id:Optional[str]=None

#creating a login path for the user 
@app.post("/login",response_model=Token)
def login (user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)): #OAuth2PasswordRequestForm stores the email into a field as username
    login_user=db.query(models.User).filter(models.User.email==user_credentials.username).first()#.first()represents one user with the specific email ,defining email as our username
    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f'Invalid Credentials')
    if not verify(user_credentials.password,login_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail=f'Invalid Credentials') #details was parsed so that it wont be easy to figure out  weather he typed the wrong password or email
    access_token= create_access_token(data={"user_id":login_user.id})#data we want to pass in the payload is the user id (TOKEN=HEADER,SIGNATURE ,PAYLOAD parsed in the variable access_token)
    return{"access_token":access_token, "token_type":"bearer"} #token type is bearer token which will be configured in the frontend     
#this func above is performing a logic  of hashing the paswod given by the user and seeing if it compares to that of the database                                 



#func to verify access token if it is still valid or hasnot expired
def verify_access_token(token:str,credentials_exception):#what the exception should be if credentials dont match
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) 
        id:str=payload.get("user_id")#getting the payload and storing in an id variable, other fields can also be added in the payload depending on the project
        if id is None:
            raise credentials_exception
        else:
            token_data= TokenData(id=id)    
    except JWTError:
        raise credentials_exception    
    return token_data      

#this func calls the verify_access_token, this fuc calls th user from the database 
def get_current_user(token:str=Depends(oauth2_scheme)):#this func takes the token from the request automatically,extract the id ,verifys if the token is correct
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f'cannot validate credentials',headers={"WWW-Authenticate":"Bearer"})
     
    return verify_access_token(token, credentials_exception)



#creating a post(create operation )
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=Postresponse)
def create_posts(post:CreatePost, db:Session = Depends(get_db),user_id:int=Depends(get_current_user)):#adding a dependency get_current_user the user has to be logged in before he can create a post ,the get_current_user calls the  verify_access_token and passes the token extracts the id and return the token data, #createPost represents a basemodel 
    createdpost=models.Post(owner_id=user_id.id,**post.dict()) #(title=post.title,content=post.content,comments=post.comments,published=post.published) it will also automatically add to the dictionaery incase more field are added in the model (table),owner_id(users id) is parsed  to conect to the user_id when a post is created it will generate the id
    db.add(createdpost) #add a brand newpost to our database 
    db.commit() #commit it to our db
    db.refresh(createdpost)#restores the new post into the variable of created post
    return createdpost

#getting the list of a post (read operation )
@app.get("/posts",response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),user_id:int=Depends(get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=""): #a limit of 10 posts is what a user can get at an instance, skip is used to skip a particular post you dont want to see
    print(limit)
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #.all() runs the sql query, implementing a search command
    #implementing a like path  when a user gets a post he can like see if its liked or not 
    results= db.query(models.Post,func.Count(models.Vote.post_id).label("likes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()  #joining the columns of vote id(models.Vote.post_id) equalsto newspost id(models.Post_id),groupt it by selecting the newspost id (models.Post)
    # func.Count(models.Vote.post_id).label("likes")=performingthe number of counts of votes on a post and labelling it as likes 
    return results

#retrieving a particular post of a user by other individuals (read operation)
@app.get("/posts/{id}",response_model=Postresponse) #response model is what the client views
def get_post(id:int, db:Session = Depends(get_db),user_id:int=Depends(get_current_user)):#user_id is parsed for individual to be logged in before getting a post
    post=db.query(models.Post).filter(models.Post.id==id).first()#gets the first instance of the id and executes 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"oops ID {id} was not found")
    else:    
        return post

#retrieving a user information or details by other individuals (read operation)
@app.get("/users/{id}",response_model=Userresponse) #from the response model defined individuals cant see the users password 
def get_user(id:int, db: Session = Depends(get_db),user_id:int=Depends(get_current_user)): #user_id is parsed for an individual to be logged in before he can retrive an information of a user
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {id} doesn't exist")
    else:
        return user    


#updating a post (update operation )
@app.put("/posts/{id}",response_model=Postresponse) 
def update_post(id:int,post:UpdatePost,db:Session = Depends(get_db),user_id:int=Depends(get_current_user)):#UpdatePost represents a basemodel,user_id is parsed for a user to be loged in before  he can update a post 
    update_query=db.query(models.Post).filter(models.Post.id==id) #performing sql queries on the Post table
    update_post=update_query.first()
    if update_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"oops ID {id} was not found")
    else:
        update_query.update(post.dict(),synchronize_session=False)
        db.commit() 
        return update_query.first()  


#deleting a post (delete operation )
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),user_id:int=Depends(get_current_user)): #user_id is parsed for a user to be loged in before  he can delete a post
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()== None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=F"post with id : {id} doesnt exist")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)    

#implementing a like/vote operation path
@app.post("/like",status_code=status.HTTP_201_CREATED)
def likes(like:Vote,db:Session = Depends(get_db),user_id:int=Depends(get_current_user)):#like:vote represents the schemafor Vote
    post=db.query(models.Post).filter(models.Post.id==like.post_id).first
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {like.post_id} does not exist")

    like_query=db.query(models.Vote).filter(models.Vote.post_id==like.post_id, #if theres a vote for a specific post_id based on a particular user_id 
    models.Vote.user_id==user_id.id) #making the class of Vote ewual to the schema of Vote which is definbed as like
    like_post= like_query.first()

    if(like.dir==1): #if the user wants to like a post 
        if like_post: #if the  user wants 2 like & has liked initially
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"user {user_id.id} has liked on post {like.post_id}")
        else: #if the user wants 2 like & hasnt liked initially
            new_like= models.Vote(post_id=like.post_id,user_id=user_id.id) 
            db.add(new_like)
            db.commit()   
            return {"successfully liked post"}
    else: #if the user wants to unlike a liked post 
        if not like_post: #if user hasnt liked initially and wants to unlike
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="hasnt liked post")  
        else: #if user has liked initially and wants to unlike
            like_query.delete(synchronize_session=False)
            db.commit()
            return {"successfully unliked post"}



     