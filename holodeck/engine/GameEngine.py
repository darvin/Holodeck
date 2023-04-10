

from sqlmodel import Session, select
from ..models import Character


class GameEngine:
    def __init__(self, db_engine) -> None:
        self.db_engine = db_engine

    def move_character(self, character_id: int, location_id: int) -> bool:
        pass

    def get_character(self, id:int) -> Character:
        with Session(self.db_engine) as session:

            character = session.exec(select(Character).where(Character.id ==id)).all()[0]

    def act(self, prompt:str):
        pass
