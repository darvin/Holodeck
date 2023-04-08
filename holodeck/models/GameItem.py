from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class GameItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str = Field(default=None)
    weight: Optional[float] = Field(default=None)
    value: Optional[float] = Field(default=None)
    item_type: Optional[str] = Field(default=None)
    character_id: int = Field(foreign_key="character.id")
    character: "Character" = Relationship(back_populates="game_items")
    damage: Optional[str] = Field(default=None)
    armor: Optional[int] = Field(default=None)
    range: Optional[str] = Field(default=None)
    durability: Optional[int] = Field(default=None)
    rarity: Optional[str] = Field(default=None)
    enchantments: Optional[List[str]] = Field(default=[])
    item_id: Optional[int] = Field(foreign_key="item.id")
    item: 'Item' = Relationship()
