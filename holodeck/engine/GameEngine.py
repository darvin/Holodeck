

from sqlmodel import Session, select
from ..models import Character, GameCharacter, Way, Location


class GameEngine:
    def __init__(self, db) -> None:
        self.db = db

    def move_character(self, character_id: int, location_id: int) -> bool:
        character = self.db.exec(select(Character).where(Character.id == character_id)).all()[0]
        current_location_id = character.location_id

        ways_results = self.db.exec(select(Way).where(Way.from_location_id == current_location_id, Way.to_location_id == location_id)).unique().all()
        if ways_results:
            character.location_id = location_id
            self.db.add(character)
            self.db.commit()
            return True
        else:
            return False



    def get_character(self, id:int) -> Character:
        character = self.db.exec(select(Character).where(Character.id ==id)).all()[0]

        return character.game_character

    def act(self, prompt:str):
        pass
