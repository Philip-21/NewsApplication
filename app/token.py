from jose import JWTError, jwt #libraray for creating a token 
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login") #the url endpoint



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




#func to verify access token if it is still valid or hasnot expired
def verify_access_token(token:str,credentials_exception):#what the exception should be if credentials dont match
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) 
        id:str=payload.get("user_id")#getting the payload and storing in an id variable, other fields can also be added in the payload depending on the project
        if id is None:
            raise credentials_exception
        else:
            token_data= schemas.TokenData(id=id)    
    except JWTError:
        raise credentials_exception    
    return token_data      



#this func calls the verify_access_token, this fuc calls th user from the database 
def get_current_user(token:str=Depends(oauth2_scheme)):#this func takes the token from the request automatically,extract the id ,verifys if the token is correct
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f'cannot validate credentials',headers={"WWW-Authenticate":"Bearer"})
     
    return verify_access_token(token, credentials_exception)

