from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlmodel import Field, Session, SQLModel, create_engine, JSON, Column




class GameCharacter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    strength: int = Field(default=None, nullable=True)
    dexterity: int = Field(default=None, nullable=True)
    intelligence: int = Field(default=None, nullable=True)
    health: int = Field(default=None, nullable=True)
    will: int = Field(default=None, nullable=True)
    perception: int = Field(default=None, nullable=True)
    advantages: List[str] = Field(sa_column=Column(JSON), default=[])
    disadvantages: List[str] = Field(sa_column=Column(JSON), default=[])
    skills: List[str] = Field(sa_column=Column(JSON), default=[])
    character: 'Character' = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="game_character"
    )

        # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True


