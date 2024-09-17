'''test api operations with SQL model'''
from sqlmodel import create_engine, SQLModel
from sqlalchemy import URL
from app.main import app
import os
from dotenv.load 
from fastapi.testclient import TestClient

client = TestClient(app)


# connect to the database

def test_create_ticket():
    """ test for creating a ticket""" 
