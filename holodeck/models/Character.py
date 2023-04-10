from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty

from .GameObjectImage import GameObjectImage

class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    character_type: str
    character_subtype: str
    location_id: Optional[int] = Field(foreign_key="location.id", default=None)
    location: 'Location' = Relationship(back_populates="characters")

    game_items: List["GameItem"] = Relationship()
    game_character_id: Optional[int] = Field(foreign_key="gamecharacter.id")
    game_character: 'GameCharacter' = Relationship(back_populates="character")

    image_id: Optional[int] = Field(foreign_key="image.id")
    image: 'GameObjectImage' = Relationship()

    # def __init__(self, name:str, description:str, character_type:str, character_subtype:str):
    #     self.name = name
    #     self.description = description
    #     self.character_type = character_type
    #     self.character_subtype = character_subtype

    def __str__(self):
        return f"{self.name}: {self.description}"
