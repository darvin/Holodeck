from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

from sqlalchemy.orm import RelationshipProperty
from .Building import Building

from .Character import Character
from .Encounter import Encounter
from .Way import Way

from .GameObjectImage import GameObjectImage


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    buildings: List[Building] = Relationship()
    ways_outgoing: List[Way] = Relationship()
    # ways_incoming: List["Way"] = Relationship()
    encounters: List[Encounter] = Relationship()
    characters: List[Character] = Relationship()

    image_id: Optional[int] = Field(foreign_key="image.id")
    image: GameObjectImage = Relationship()


    # def __init__(self, name:str, description:str):
    #     self.name = name
    #     self.description = description

    def add_encounter(self, encounter):
        encounter.location_id = self.id
        self.encounters.append(encounter)

    def add_building(self, building):
        building.location_id = self.id
        self.buildings.append(building)

    def add_way(self, way):
        way.from_location_id = self.id
        self.ways_outgoing.append(way)

    def __str__(self):
        buildings_str = "\n  ".join([str(b) for b in self.buildings])
        ways_str = "\n  ".join([str(w) for w in self.ways_outgoing])
        encounters_str = "\n  ".join([str(e) for e in self.encounters])
        return f"{self.name}\n{self.description}\n\nBuildings:\n  {buildings_str}\n\nWays:\n  {ways_str}\n\nEncounters:\n  {encounters_str}"

    @property
    def objects(self):
        objects = []
        for encounter in self.encounters:
            for action in encounter.actions:
                if action.character:
                    objects.append(action.character)
                if action.item:
                    objects.append(action.item)
                if action.critter:
                    objects.append(action.critter)
        return objects

    @property
    def all_buildings(self):
        all_buildings = []
        for building in self.buildings:
            all_buildings.append(building)
        for encounter in self.encounters:
            for action in encounter.actions:
                if action.building:
                    all_buildings.append(action.building)
        return all_buildings
    

