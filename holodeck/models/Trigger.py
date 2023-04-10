
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty
from .Building import Building

from .Way import Way

class TriggerType(str, Enum):
    WAY = "way"
    BUILDING = "building"

class Trigger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TriggerType
    way_id: Optional[int] = Field(foreign_key="way.id")
    way: Optional[Way] = Relationship()
    building_id: Optional[int] = Field(foreign_key="building.id")
    building: Optional[Building] = Relationship()
    encounter_id: int = Field(foreign_key="encounter.id")



    # def __init__(self, type:TriggerType, way:Optional[Way]=None, building:Optional[Building]=None):
    #     self.type = type
    #     self.way = way
    #     self.building = building

    def __str__(self):
        fields = []
        if self.id:
            fields.append(f"id={self.id}")
        if self.type:
            fields.append(f"type={self.type.name}")
        if self.way:
            fields.append(f"way={self.way.name}")
        if self.building:
            fields.append(f"building={self.building.name}")
        fields.append(f"encounter_id={self.encounter_id}")
        return f"Trigger({', '.join(fields)})"

