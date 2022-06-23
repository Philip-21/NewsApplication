
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  #retrieving users credentials in login route
from sqlalchemy.orm import Session

from .. import database, schemas, models, token, utils


router = APIRouter(tags=['Authentication'])

#creating a login path for the user 
@router.post('/login', response_model=schemas.Token)
def login (user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(database.get_db)): #OAuth2PasswordRequestForm stores the email into a field as username
    login_user=db.query(models.User).filter(models.User.email==user_credentials.username).first()#.first()represents one user with the specific email ,defining email as our username
    
    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f'Invalid Credentials')

    if not utils.verify(user_credentials.password,login_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail=f'Invalid Credentials') #details was parsed so that it wont be easy to figure out  weather he typed the wrong password or email
    access_token= token.create_access_token(data={"user_id":login_user.id})#data we want to pass in the payload is the user id (TOKEN=HEADER,SIGNATURE ,PAYLOAD parsed in the variable access_token)
    return{"access_token":access_token, "token_type":"bearer"} #token type is bearer token which will be configured in the frontend     
#this func above is performing a logic  of hashing the paswod given by the user and seeing if it compares to that of the database                                 
