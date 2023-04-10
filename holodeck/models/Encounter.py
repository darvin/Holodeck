from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import RelationshipProperty

from .Action import Action
from .Trigger import Trigger


class Encounter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    probability: float
    description: str
    actions: List[Action] = Relationship()
    location_id: int = Field(foreign_key="location.id")
    triggers: List[Trigger] = Relationship()



    # def __init__(self, probability: float, description: str, triggers: List['Trigger'], actions: List['Action']):
    #     self.probability = probability
    #     self.description = description
    #     self.triggers = triggers
    #     self.actions = actions

    def __str__(self):
        if self.triggers:
            trigger = self.triggers[0]
            trigger_str = f"{trigger.type.name}: {trigger.way}" if trigger.way else f"{trigger.type.name}: {trigger.building}"
        else:
            trigger_str = ""
        action_str = "\n".join([f"  {action}" for action in self.actions])
        return f"Encounter ({self.probability * 100}%): {self.description}\nTrigger: {trigger_str}\nActions:\n{action_str}"
