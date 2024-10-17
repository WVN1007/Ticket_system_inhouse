"""test api functionalities"""

from sqlalchemy import MetaData

from app.db_model import Base

from .database_fixture import TestEngine

meta = MetaData()


def test_database_tables_creation():
    """test if all the tables are created"""

    Base.metadata.drop_all(bind=TestEngine)
    Base.metadata.create_all(bind=TestEngine)
    meta.reflect(bind=TestEngine)
    tables_test_dict = meta.tables.keys()
    assert "ticket_table" in tables_test_dict
    assert "attachment_table" in tables_test_dict
    assert "dev_table" in tables_test_dict
    assert "user_table" in tables_test_dict
