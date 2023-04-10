

from sqlmodel import Session, select
from ..models import Character, GameCharacter


class GameEngine:
    def __init__(self, db) -> None:
        self.db = db

    def move_character(self, character_id: int, location_id: int) -> bool:
        pass

    def get_character(self, id:int) -> Character:
        character = self.db.exec(select(Character).where(Character.id ==id)).all()[0]

        return character.game_character

    def act(self, prompt:str):
        pass
