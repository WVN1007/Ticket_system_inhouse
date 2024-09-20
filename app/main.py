"""Api entry point"""

from fastapi import FastAPI
from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return {"msg": "Hello World"}
