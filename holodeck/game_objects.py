from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class TriggerType(str, Enum):
    WAY = "way"
    BUILDING = "building"

class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    buildings: List["Building"] = Relationship()
    ways: List["Way"] = Relationship()
    encounters: List["Encounter"] = Relationship()
    characters: List["Character"] = Relationship()

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    def add_encounter(self, encounter):
        self.encounters.append(encounter)

    def add_building(self, building):
        self.buildings.append(building)

    def add_way(self, way):
        self.ways.append(way)

    def __str__(self):
        buildings_str = "\n  ".join([str(b) for b in self.buildings])
        ways_str = "\n  ".join([str(w) for w in self.ways])
        encounters_str = "\n  ".join([str(e) for e in self.encounters])
        return f"{self.name}\n{self.description}\n\nBuildings:\n  {buildings_str}\n\nWays:\n  {ways_str}\n\nEncounters:\n  {encounters_str}"

    @property
    def objects(self):
        objects = []
        for encounter in self.encounters:
            for action in encounter.actions:
                if isinstance(action, Item) or isinstance(action, Critter) or isinstance(action, Character):
                    objects.append(action)
        return objects

    @property
    def all_buildings(self):
        all_buildings = []
        for building in self.buildings:
            all_buildings.append(building)
        for encounter in self.encounters:
            for action in encounter.actions:
                if isinstance(action, Building):
                    all_buildings.append(action)
        return all_buildings
    

class Way(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location_id: int = Field(foreign_key="location.id")

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description
        
    def __str__(self):
        return f"{self.name}: {self.description}"

class Building(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    enterable: bool
    location_id: Optional[int] = Field(foreign_key="location.id")


    def __init__(self, name:str, description:str, enterable:bool):
        self.name = name
        self.description = description
        self.enterable = enterable

    def __str__(self):
        enter_str = "Enterable" if self.enterable else "Not enterable"
        return f"{self.name}: {self.description} ({enter_str})"

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description



class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location_id: Optional[int] = Field(foreign_key="location.id", default=None)


    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

class Critter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"
    
class Trigger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TriggerType
    way_id: Optional[int] = Field(foreign_key="way.id")
    way: Optional[Way] = Relationship()
    building_id: Optional[int] = Field(foreign_key="building.id")
    building: Optional[Building] = Relationship()
    encounter_id: int = Field(foreign_key="encounter.id")



    def __init__(self, type:TriggerType, way:Optional[Way]=None, building:Optional[Building]=None):
        self.type = type
        self.way = way
        self.building = building

    def __str__(self):
        trigger_str = f"{self.type_.name}: "
        for key, value in self.__dict__.items():
            if key != "type_":
                trigger_str += f"{key}={value}, "
        trigger_str = trigger_str.rstrip(", ")
        return trigger_str


class Encounter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    probability: float
    description: str
    actions: List['Action'] = Relationship()
    location_id: int = Field(foreign_key="location.id")
    triggers: List['Trigger'] = Relationship()



    def __init__(self, probability: float, description: str, triggers: List['Trigger'], actions: List['Action']):
        self.probability = probability
        self.description = description
        self.triggers = triggers
        self.actions = actions

    def __str__(self):
        if self.triggers:
            trigger = self.triggers[0]
            trigger_str = f"{trigger.type.name}: {trigger.way}" if trigger.way else f"{trigger.type.name}: {trigger.building}"
        else:
            trigger_str = ""
        action_str = "\n".join([f"  {action}" for action in self.actions])
        return f"Encounter ({self.probability * 100}%): {self.description}\nTrigger: {trigger_str}\nActions:\n{action_str}"

class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str

    encounter_id: int = Field(foreign_key="encounter.id")

    critter_id: Optional[int] = Field(foreign_key="critter.id")
    critter: Optional['Critter'] = Relationship()
    character_id: Optional[int] = Field(foreign_key="character.id")
    character: Optional['Character'] = Relationship()
    item_id: Optional[int] = Field(foreign_key="item.id")
    item: Optional['Item'] = Relationship()
    building_id: Optional[int] = Field(foreign_key="building.id")
    building: Optional['Building'] = Relationship()


    def __init__(self, type:str, obj=None, building:Optional[Building]=None, \
                 item:Optional[Item]=None, critter:Optional['Critter']=None, \
                    character:Optional['Character']=None):
        self.type = type

        if building is not None:
            self.building = building
        if item is not None:
            self.item = item
        if critter is not None:
            self.critter = critter
        if character is not None:
            self.character = character

        if obj is not None:
            if isinstance(obj, Critter):
                self.critter = obj
            elif isinstance(obj, Character):
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
        if self.critter:
            components.append(f"critter={self.critter}")
        if self.character:
            components.append(f"character={self.character}")
        return ", ".join(components)
