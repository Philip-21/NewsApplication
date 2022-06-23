

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, token


router = APIRouter(
    prefix="/like",
    tags=['Vote']
)




#implementing a like/vote operation path
@router.post("/",status_code=status.HTTP_201_CREATED)
def likes(like:schemas.Vote,db:Session = Depends(database.get_db),user_id:int=Depends(token.get_current_user)):#like:vote represents the schemafor Vote
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

