
from typing import Optional

from redbird.repos import MongoRepo

import pytest
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    name: str
    age: Optional[int]


class ItemWithCol(BaseModel):
    __colname__ = 'items'
    id: str
    name: str
    age: Optional[int]

def test_creation_defaults():
    pytest.importorskip("pymongo")
    repo = MongoRepo.from_uri(model=ItemWithCol, uri="mongodb://localhost:27017/pytest?authSource=admin", id_field="id")

    col = repo.get_collection()
    assert col.name == "items"
    assert col.database.name == "pytest"

def test_from_client():
    pytest.importorskip("pymongo")
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/pytest?authSource=admin")
    repo = MongoRepo.from_client(model=ItemWithCol, client=client, id_field="id", database="pytest")

    col = repo.get_collection()
    assert col.name == "items"
    assert col.database.name == "pytest"

def test_creation_passed(mongo_uri):
    pytest.importorskip("pymongo")
    repo = MongoRepo.from_uri(model=Item, uri=mongo_uri, database="pytest2", collection="items", id_field="id")

    col = repo.get_collection()
    assert col.name == "items"
    assert col.database.name == "pytest2"
