"""Api entry point"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg":"Hello World"}

@app.get("/api/tickets")
def read_user_ticket():
    """read all available tickets"""
    raise NotImplementedError

@app.post("/api/tickets")
def create_user_ticket():
    """create a new ticket"""
    raise NotImplementedError

@app.put("/api/tickets/{id}")
def update_user_ticket():
    """update a ticket information"""
    raise NotImplementedError

@app.delete("/api/tickets/{id}")
def delete_user_ticket():
    raise NotImplementedError
