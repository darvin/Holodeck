from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid as uuid_pkg



class GameObjectImage(SQLModel, table=True):
    __tablename__ = "image"

    id: Optional[int] = Field(default=None, primary_key=True)

    # id: uuid_pkg.UUID = Field(
    #     default_factory=uuid_pkg.uuid4,
    #     primary_key=True,
    #     index=True,
    #     nullable=False,
    # )
    prompt: str = Field()
    removed: bool = Field(default=False, nullable=True)
    generated: bool = Field(default=False, nullable=True)