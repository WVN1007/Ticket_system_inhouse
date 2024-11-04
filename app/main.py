"""Api entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, tickets, devs, auth

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

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
