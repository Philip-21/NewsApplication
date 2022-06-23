from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, token
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




#creating a post(create operation )
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Postresponse)
def create_posts(post:schemas.CreatePost, db:Session = Depends(get_db),user_id:int=Depends(token.get_current_user)):#adding a dependency get_current_user the user has to be logged in before he can create a post ,the get_current_user calls the  verify_access_token and passes the token extracts the id and return the token data, #createPost represents a basemodel 
    createdpost=models.Post(owner_id=user_id.id,**post.dict()) #(title=post.title,content=post.content,comments=post.comments,published=post.published) it will also automatically add to the dictionaery incase more field are added in the model (table),owner_id(users id) is parsed  to conect to the user_id when a post is created it will generate the id
   
    db.add(createdpost) #add a brand newpost to our database 
    db.commit() #commit it to our db
    db.refresh(createdpost)#restores the new post into the variable of created post
    return createdpost




#getting the list of a post (read operation )
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),user_id:int=Depends(token.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=""): #a limit of 10 posts is what a user can get at an instance, skip is used to skip a particular post you dont want to see
    print(limit)

    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #.all() runs the sql query, implementing a search command
    #implementing a like path  when a user gets a post he can like see if its liked or not 
    results= db.query(models.Post,func.Count(models.Vote.post_id).label("likes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()  #joining the columns of vote id(models.Vote.post_id) equalsto newspost id(models.Post_id),groupt it by selecting the newspost id (models.Post)
    # func.Count(models.Vote.post_id).label("likes")=performingthe number of counts of votes on a post and labelling it as likes 
    return results






#updating a post (update operation )
@router.put("/{id}",response_model=schemas.Postresponse) 
def update_post(id:int,post:schemas.UpdatePost,db:Session = Depends(get_db),user_id:int=Depends(token.get_current_user)):#UpdatePost represents a basemodel,user_id is parsed for a user to be loged in before  he can update a post 
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
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),user_id:int=Depends(token.get_current_user)): #user_id is parsed for a user to be loged in before  he can delete a post
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()== None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=F"post with id : {id} doesnt exist")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)    


