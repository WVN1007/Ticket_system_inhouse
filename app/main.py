"""Api entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, tickets, devs, auth
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(devs.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"msg": "Hello World"}
