from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty

from .Building import Building
from .Character import Character
from .Item import Item


class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str

    encounter_id: int = Field(foreign_key="encounter.id")

    character_id: Optional[int] = Field(foreign_key="character.id")
    character: Optional[Character] = Relationship()
    item_id: Optional[int] = Field(foreign_key="item.id")
    item: Optional[Item] = Relationship()
    building_id: Optional[int] = Field(foreign_key="building.id")
    building: Optional[Building] = Relationship()


    def __init__(self, type:str, obj=None, building:Optional[Building]=None, \
                 item:Optional[Item]=None, \
                    character:Optional['Character']=None):
        self.type = type

        if building is not None:
            self.building = building
        if item is not None:
            self.item = item
        if character is not None:
            self.character = character

        if obj is not None:
            if isinstance(obj, Character):
                self.character = obj
            elif isinstance(obj, Item):
                self.item = obj
            elif isinstance(obj, Building):
                self.building = obj
            else:
                raise ValueError("Invalid object type passed to Action.__init__")


    def __str__(self):
        components = [f"id={self.id}", f"type={self.type}"]
        if self.building:
            components.append(f"building={self.building}")
        if self.item:
            components.append(f"item={self.item}")
        if self.character:
            components.append(f"character={self.character}")
        return ", ".join(components)
