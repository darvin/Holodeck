from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


#this is not actual item that character might have, but archetype
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description
