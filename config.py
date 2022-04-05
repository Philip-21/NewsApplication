from pydantic import BaseSettings #pydantic converts a small character to capital character automatically so it can be inline with .env 

class Settings(BaseSettings):
    database_username:str
    database_password:str
    database_hostname: str
    database_port: int
    database_name:str
    secret_key: str 
    algorithm: str
    access_token_expire_minutes:int 
    class Config:
         env_file=".env"


settings =Settings()        