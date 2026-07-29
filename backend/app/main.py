from fastapi import FastAPI
from database import get_db
from database import engine, Base
from models import User, Item
from routers.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)



@app.get('/')
def demo():
    return {'Lost and Found backend working'}


