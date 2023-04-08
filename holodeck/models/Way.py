from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty

class Way(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    from_location_id: int = Field(foreign_key="location.id")
    # to_location_id: int = Field(foreign_key="location.id")
    from_location: 'Location' = Relationship(sa_relationship=RelationshipProperty("Location", foreign_keys=[from_location_id]))# , back_populates="ways_outgoing")
    # to_location: 'Location' = Relationship(sa_relationship=RelationshipProperty("Location", foreign_keys=[to_location_id])) #, back_populates="ways_incoming")

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description
        
    def __str__(self):
        return f"{self.name}: {self.description}"

