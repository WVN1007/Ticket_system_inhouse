"""Api entry point"""

from fastapi import FastAPI
from .routers import users, tickets, devs, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(devs.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"msg": "Hello World"}
