from fastapi import FastAPI
from app.models import BaseModel
from db_config import engine
import uvicorn

app = FastAPI()


if __name__ == '__main__':
    BaseModel.metadata.create_all(bind=engine)
    uvicorn.run("manage:app", host="127.0.0.1", port=8000, reload=True)