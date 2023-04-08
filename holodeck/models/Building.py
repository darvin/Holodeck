from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty
from .GameObjectImage import GameObjectImage


class Building(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    enterable: bool
    location_id: Optional[int] = Field(foreign_key="location.id")
    location: 'Location' = Relationship(back_populates="buildings")

    image_id: Optional[int] = Field(foreign_key="image.id")
    image: GameObjectImage = Relationship()
    


    def __init__(self, name:str, description:str, enterable:bool):
        self.name = name
        self.description = description
        self.enterable = enterable

    def __str__(self):
        enter_str = "Enterable" if self.enterable else "Not enterable"
        return f"{self.name}: {self.description} ({enter_str})"
