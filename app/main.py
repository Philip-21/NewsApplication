from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
import config
from config import settings
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, like

app =FastAPI()
origins=["*"]#providing list of domains that should talk to our api,[*] every kind of domain that can talk to our api

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],#for specific http methods
allow_headers=["*"],#for specific headers
)
#models.Base.metadata.create_all(bind=engine)#create and connect all of our models (tables)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/")
def root():
    return{"message":"Hello fastapi newsapp"}









     