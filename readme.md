# NEWSCONTENT API
## A Backend Api for Posting, Commenting Liking, deleting news contents

### Stacks used 
- [FastApi](https://fastapi.tiangolo.com/) as its Python backend framework
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations
- [SqlAlchemy](https://www.sqlalchemy.org/) as its ORM
- [Postgres](https://www.postgresql.org/) as its Database


#### Prerequisite
- have a version of python 3 installed 
- create a virtual environment and run
  ```
  $ pip install -r requirements.txt 
  ```
  to install all the packages to run the application
- have Postman installed and configured on your machine 

### Getting Started 
- Start the Application with the command
```
$ uvicorn main:app --reload
```
- Perform a POST reqeust to create your account , it gets submiited and saved in the db 
- After you log in with your Credentialsand start performing actions




