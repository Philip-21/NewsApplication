from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, token
from ..database import get_db







router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#creating a new path operation for the user to send its registeration details(signing up)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Userresponse)
def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):

    hashed_password=utils.hash(user.password)#hashing the paswword and storing it in user.password
    user.password= hashed_password #making it automatically update in the pydantic model
    new_user=models.User(**user.dict()) #converting user : UserCreate to a dictionary
   
    db.add(new_user) #add a brand newpost to our database 
    db.commit() #commit it to our db
    db.refresh(new_user)#restores the user  into the variable of new_user
    return new_user



#retrieving a user information or details by other individuals (read operation)
@router.get("/{id}",response_model=schemas.Userresponse) #from the response model defined individuals cant see the users password 
def get_user(id:int, db: Session = Depends(get_db),user_id:int=Depends(token.get_current_user)): #user_id is parsed for an individual to be logged in before he can retrive an information of a user
    
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {id} doesn't exist")
    else:
        return user    
