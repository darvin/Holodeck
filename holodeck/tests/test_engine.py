
"""
class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    character_type: str
    character_subtype: str
    location_id: Optional[int] = Field(foreign_key="location.id", default=None)
    location: 'Location' = Relationship(back_populates="characters")

    game_items: List["GameItem"] = Relationship()
    game_character_id: Optional[int] = Field(foreign_key="gamecharacter.id")
    game_character: 'GameCharacter' = Relationship(back_populates="character")

    image_id: Optional[int] = Field(foreign_key="image.id")
    image: 'GameObjectImage' = Relationship()




class GameCharacter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    strength: int = Field(default=None, nullable=True)
    dexterity: int = Field(default=None, nullable=True)
    intelligence: int = Field(default=None, nullable=True)
    health: int = Field(default=None, nullable=True)
    will: int = Field(default=None, nullable=True)
    perception: int = Field(default=None, nullable=True)
    advantages: List[str] = Field(default=[], nullable=True)
    disadvantages: List[str] = Field(default=[], nullable=True)
    skills: List[str] = Field(default=[], nullable=True)
    character: 'Character' = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="game_character"
    )




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

#this is not actual item that character might have, but archetype
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    buildings: List[Building] = Relationship()
    ways_outgoing: List[Way] = Relationship()
    # ways_incoming: List["Way"] = Relationship()
    encounters: List[Encounter] = Relationship()
    characters: List[Character] = Relationship()



class Encounter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    probability: float
    description: str
    actions: List[Action] = Relationship()
    location_id: int = Field(foreign_key="location.id")
    triggers: List[Trigger] = Relationship()

class TriggerType(str, Enum):
    WAY = "way"
    BUILDING = "building"

class Trigger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: TriggerType
    way_id: Optional[int] = Field(foreign_key="way.id")
    way: Optional[Way] = Relationship()
    building_id: Optional[int] = Field(foreign_key="building.id")
    building: Optional[Building] = Relationship()
    encounter_id: int = Field(foreign_key="encounter.id")



class Building(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    enterable: bool
    location_id: Optional[int] = Field(foreign_key="location.id")
    location: 'Location' = Relationship(back_populates="buildings")

    


class Way(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    from_location_id: int = Field(foreign_key="location.id")
    # to_location_id: int = Field(foreign_key="location.id")
    from_location: 'Location' = Relationship(sa_relationship=RelationshipProperty("Location", foreign_keys=[from_location_id]))# , back_populates="ways_outgoing")
    # to_location: 'Location' = Relationship(sa_relationship=RelationshipProperty("Location", foreign_keys=[to_location_id])) #, back_populates="ways_incoming")

"""

import random
import pytest

from sqlmodel import SQLModel, Session, create_engine

from ..models import Building, \
       Character, GameCharacter, Location, \
        GameItem, Item, Way, Encounter, Trigger, \
            Action, TriggerType
from ..engine import GameEngine, GameLLMResponse



db_filepath = ".data/test2db.db"
sqlite_url = f"sqlite+pysqlite:///{db_filepath}"

import os
if os.path.exists(db_filepath):
    os.remove(db_filepath)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

SQLModel.metadata.create_all(engine)

db = Session(engine)
game_engine = GameEngine(db=db)


def seed_character():
    name_list = ["Gandalf", "Merlin", "Dumbledore", "Gandalf", "Morgoth", "Saruman"]
    description_list = ["A wise old wizard", "A powerful magician", "A cunning enchanter"]
    adv_list = ["Magical Aptitude", "Staff Mastery", "Fire Magic", "Water Magic"]
    dis_list = ["Old Age", "No Armor", "Cursed"]
    skills_list = ["Magic", "Staff", "Alchemy", "Herblore"]
    
    name = random.choice(name_list)
    description = random.choice(description_list)
    strength = random.randint(1, 20)
    dexterity = random.randint(1, 20)
    intelligence = random.randint(1, 20)
    health = random.randint(50, 150)
    will = random.randint(1, 20)
    perception = random.randint(1, 20)
    advantages = random.sample(adv_list, random.randint(1, 2))
    disadvantages = random.sample(dis_list, random.randint(1, 2))
    skills = random.sample(skills_list, random.randint(1, 2))

    fantasy_character = Character(
        name=name,
        description=description,
        character_type="character",
        character_subtype="player",
    )
    

    game_character = GameCharacter(
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        health=health,
        will=will,
        perception=perception,
        advantages=advantages,
        disadvantages=disadvantages,
        skills=skills,
        character=fantasy_character,
    )
    db.add(game_character, fantasy_character)
    db.commit()
    db.refresh(game_character)
    return game_character



import random

def seed_building(location_id):
    name=f"{random.choice(['Ruined', 'Abandoned', 'Haunted'])} {random.choice(['Keep', 'Tower', 'Castle'])}"
    description=f"A {random.choice(['crumbling', 'mysterious', 'forbidding'])} structure {random.choice(['overgrown with vines', 'haunted by spirits', 'surrounded by mist'])}."
    building = Building(
        name=name,
        description=description,
        location_id=location_id,
        enterable=random.choice([True, False])
    )
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


def test_get_my_character():
    """
    Retrieve current player character object.

    Check that the character object returned is of the expected type and has the expected properties.
    Return an error if there is no active player character.
    """
    game_character = seed_character()

    # Retrieve the character from the database
    c = game_engine.get_character(id=game_character.character.id)

    # Check that the character object returned is of the expected type and has the expected properties
    assert isinstance(c.character, Character)
    assert isinstance(c, GameCharacter)
    assert c.character.name == game_character.character.name
    assert c.character.description == game_character.character.description
    assert c.character.character_type == game_character.character.character_type
    assert c.character.character_subtype == game_character.character.character_subtype
    assert c.strength == game_character.strength
    assert c.dexterity == game_character.dexterity
    assert c.intelligence == game_character.intelligence
    assert c.health == game_character.health
    assert c.will == game_character.will
    assert c.perception == game_character.perception
    assert set(c.advantages) == set(game_character.advantages)
    assert set(c.disadvantages) == set(game_character.disadvantages)
    assert set(c.skills) == set(game_character.skills)


import random

def seed_location_with_buildings():
    location = Location(
        name=f"{random.choice(['Misty', 'Frosty', 'Shadow'])} {random.choice(['Caverns', 'Peaks', 'Valley'])}",
        description=f"A {random.choice(['sinister', 'majestic', 'enchanted'])} location {random.choice(['shrouded in mist', 'blanketed in snow', 'overrun with creatures'])}.",
    )
    db.add(location)
    db.commit()
    db.refresh(location)

    # Add some buildings to the location
    building1 = Building(
        name=f"{random.choice(['Ruined', 'Abandoned', 'Haunted'])} {random.choice(['Keep', 'Tower', 'Castle'])}",
        description=f"A {random.choice(['crumbling', 'mysterious', 'forbidding'])} structure {random.choice(['overgrown with vines', 'haunted by spirits', 'surrounded by mist'])}.",
        enterable=True,
        location=location,
    )
    building2 = Building(
        name=f"{random.choice(['Goblin', 'Troll', 'Orc'])} {random.choice(['Lair', 'Den', 'Nest'])}",
        description=f"A {random.choice(['foul-smelling', 'dangerous', 'filthy'])} den {random.choice(['crawling with vermin', 'strewn with garbage', 'decorated with trophies of past victims'])}.",
        enterable=True,
        location=location,
    )
    db.add_all([building1, building2])
    db.commit()
    db.refresh_all()

    # Add some ways leading to and from the location
    encounter = Encounter(
        probability=1.0,
        description="A group of monsters emerges from the shadows, brandishing rusty weapons and snarling menacingly.",
        location=location,
    )



    way1 = Way(
        name="Eventful Way",
        description="A treacherous path through the mountains, winding its way down to the valley below.",
        from_location=location,
        to_location=None,
    )
    way2 = Way(
        name="Non-eventful Way",
        description="A safe, but long, path leading to a nearby village.",
        from_location=location,
        to_location=None,
    )
    db.add_all([way1, way2])

    trigger = Trigger(type=TriggerType.WAY, way=way1, encounter=encounter)
    db.add_all([location, encounter, trigger])

    db.commit()
    db.refresh_all()

    return location

def seed_location():
    location = Location(
        name=f"{random.choice(['Misty', 'Frosty', 'Shadow'])} {random.choice(['Caverns', 'Peaks', 'Valley'])}",
        description=f"A {random.choice(['sinister', 'majestic', 'enchanted'])} location {random.choice(['shrouded in mist', 'blanketed in snow', 'overrun with creatures'])}.",
    )
    db.add(location)
    db.commit()
    db.refresh(location)

    return location



def seed_way(from_location_id, to_location_id=None):
    way = Way(
        name=f"{random.choice(['Eventful', 'Non-eventful', 'Safe', 'Dangerous'])} {random.choice(['Path', 'Trail', 'Road'])}",
        description=f"A {random.choice(['treacherous', 'scenic', 'winding', 'straight'])} route {random.choice(['through the mountains', 'across the plains', 'along the coast', 'into the forest'])}.",
        from_location_id=from_location_id,
        to_location_id=to_location_id,
    )
    db.add(way)
    db.commit()
    db.refresh(way)

    return way


def seed_encounter(location_id):
    encounter = Encounter(
        probability=1.0,
        description=f"{random.choice(['A group of monsters emerges from the shadows, brandishing rusty weapons and snarling menacingly.', 'You suddenly feel a chill run down your spine.', 'You hear a faint whispering in the wind.', 'You see a figure in the distance, beckoning you forward.'])}",
        location_id=location_id,
    )
    db.add(encounter)
    db.commit()
    db.refresh(encounter)

    return encounter


def test_get_current_location():
    """
    Retrieve the current location of the player character.

    Check that the location object returned is of the expected type and has the expected properties.
    Return an error if the player character is not currently located anywhere.
    """
    game_character = seed_character()
    location = seed_location()
    building1 = seed_building(location_id=location.id)
    building2 = seed_building(location_id=location.id)
    way1 = seed_way(from_location_id=location.id, to_location_id=seed_location().id)
    encounter = seed_encounter(location_id=location.id)

    game_character.character.location_id = location.id
    db.add(game_character)
    db.commit()
    db.refresh(game_character)

    # Retrieve the current location of the player character
    c = game_engine.get_character(id=game_character.character.id)
    assert c is not None
    l = c.character.location
    assert l == location

    # Check that the location object returned is of the expected type and has the expected properties
    assert isinstance(l, Location)
    assert l.name == location.name
    assert l.description == location.description
    assert len(l.buildings) == 2
    assert building1 in l.buildings
    assert building2 in l.buildings
    assert len(l.ways_outgoing) == 1
    assert way1 in l.ways_outgoing
    assert len(l.encounters) == 1
    assert encounter in l.encounters

import random


def seed_game_item():
    # Define possible properties for the game item
    item_names = [
        "Sword of Flame",
        "Staff of Ice",
        "Bow of Thunder",
        "Dagger of Shadows",
        "Mace of Light",
        "Axe of Fury",
        "Wand of Magic",
        "Scepter of Power",
        "Hammer of Justice",
        "Shield of Protection",
    ]
    item_descriptions = [
        "A powerful weapon imbued with magical fire.",
        "A staff that harnesses the power of ice to freeze enemies.",
        "A bow that shoots arrows of lightning to strike foes.",
        "A small but deadly blade that can be used to strike from the shadows.",
        "A heavy mace that delivers crushing blows to enemies of good.",
        "A double-edged axe that embodies the fury of the storm.",
        "A wand that can cast spells with great precision and accuracy.",
        "A scepter that channels the very essence of magic.",
        "A hammer that metes out justice with each swing.",
        "A shield that protects its bearer from harm.",
    ]
    item_weights = [1, 1, 1, 2, 2, 2, 3, 3, 4, 5]  # Higher weights for more powerful items
    item_rarities = ["common", "uncommon", "rare", "epic", "legendary"]
    item_effects = [
        "Deals bonus damage to undead enemies.",
        "Grants the wielder temporary invisibility.",
        "Restores health when used to strike a killing blow.",
        "Allows the wielder to summon a temporary ally.",
        "Boosts the wielder's defense against elemental attacks.",
        "Increases the wielder's movement speed.",
        "Reveals hidden secrets and passages.",
        "Causes the wielder's attacks to ignore armor.",
        "Inflicts a random status effect on enemies.",
        "Allows the wielder to fly temporarily.",
    ]

    # Randomly select properties for the game item
    name = random.choice(item_names)
    description = random.choice(item_descriptions)
    weight = random.choices(item_weights, weights=item_weights, k=1)[0]
    rarity = random.choices(item_rarities, weights=[5, 3, 1, 0.1, 0.01], k=1)[0]
    effect = random.choice(item_effects)

    # Create the game item object
    game_item = GameItem(name=name, description=description, weight=weight, rarity=rarity, effect=effect)

    db.add(game_item)
    db.commit()
    db.refresh(game_item)

    return game_item


def test_move_to_other_location_existing():
    """
    Move player character to a different location that exists.

    Check that the player character's location is correctly updated after the move.
    Return an error if the destination location does not exist.
    """

def test_move_to_other_location_existing():
    """
    Move player character to a different location that exists.

    Check that the player character's location is correctly updated after the move.
    Return an error if the destination location does not exist.
    """
    game_character = seed_character()

    # Seed two locations
    location1 = seed_location()
    location2 = seed_location()

    # Seed a way connecting the two locations
    way = seed_way(from_location_id=location1.id, to_location_id=location2.id)
 

    # Move the player character to the first location
    game_character.character.location_id = location1.id
    db.add(game_character)
    db.commit()
    db.refresh(game_character)

    # Move the player character to the second location
    game_engine.move_character(game_character.character.id, location2.id)

    # Check that the player character's location is correctly updated after the move
    c = game_engine.get_character(id=game_character.character.id)
    assert c is not None
    l = c.character.location
    assert l == location2

    assert game_engine.move_character(game_character.id, 9999) == False


def test_move_to_other_location_non_existent():
    """
    Move player character to a non yet created location.

    location must be automatically generated on entrance, if Way with `to_location` thats equal None is used
    """



def test_basic_action():
    """
    Execute a basic player action: game_engine.act(action_text)
    note that action_text might contain special syntax like:
     - "Move to {Location:43}"
     - "Demolish {Building:21} with {GameItem:23}"
     - "Attack {Character:11}"
     - "Steal {GameItem:32} from {Character:2}"


    Check that the action has the expected outcome.
    Return an error if the action cannot be executed.
    """
    # Create a character and seed a location for them
    game_character = seed_character()
    
    # Seed two locations
    location = seed_location()
    location2 = seed_location()

    # Seed a way connecting the two locations
    way = seed_way(from_location_id=location.id, to_location_id=location2.id)
 

    # Move the player character to the first location
    game_character.character.location_id = location.id
    db.add(game_character)
    db.commit()
    db.refresh(game_character)

    assert game_character.character.location == location
    
    def llm_fake(prompt):
        assert "move" in prompt.lower()
        assert "location" in prompt.lower()
        # assert location.ways_outgoing[0].to_location.name in prompt.lower()
        # assert str(location.ways_outgoing[0].to_location.id) in prompt.lower()
        return GameLLMResponse(sql="UPDATE character SET location_id=%d WHERE id=%d" % (location.ways_outgoing[0].to_location.id, game_character.character.id))


    # Define a lambda function for moving the character to a new location
    game_engine.llm = llm_fake
    
    # Perform a basic action
    action_text = "Move to {Location:%d}" % (location.ways_outgoing[0].to_location.id)
    game_engine.act(game_character.character.id, action_text)
    db.refresh(game_character)

    # Check that the action has the expected outcome
    assert game_character.character.location != location
    assert game_character.character.location.id == location.ways_outgoing[0].to_location.id


def test_demolish_building():
    """
    Execute a player action to demolish a building:
        action_text = "Demolish {Building:21} with {GameItem:23}"
    Check that the building is removed from the location and the character loses the game item.
    Return an error if the action cannot be executed.
    """
    # Create a character and seed a location with a building
    game_character = seed_character()
    location = seed_location()
    building = seed_building(location_id=location.id)
    assert building in location.buildings
    
    def llm_fake(prompt):
        assert "demolish" in prompt.lower()
        assert "building" in prompt.lower()
        assert str(building.id) in prompt.lower()
        assert "gameitem" in prompt.lower()
        assert str(game_character.game_items[0].id) in prompt.lower()
        return GameLLMResponse(sql="DELETE FROM buildings WHERE id=%d;" % building.id + \
                "DELETE FROM character_game_items WHERE character_id=%d AND game_item_id=%d;" % (game_character.character.id, game_character.game_items[0].id))


    game_engine.llm = llm_fake
    
    # Perform the demolish action
    action_text = "Demolish {Building:%d} with {GameItem:%d}" % (building.id, game_character.game_items[0].id)
    game_engine.act(game_character.character_id, action_text)

    # Check that the action has the expected outcome
    assert building not in location.buildings
    assert game_character.game_items[0] not in game_character.character.game_items


def test_get_inventory():
    """
    Retrieve the player character's inventory.

    Check that the inventory object returned is of the expected type and has the expected properties.
    Return an error if there is no active player character or the inventory is empty.
    """

def test_throw_away_item():
    """
    Throw away an item from the player character's inventory.

    Check that the item is correctly removed from the inventory after the action.
    Return an error if the item cannot be thrown away (e.g. it is not in the inventory).
    """
    # Create a character and seed their inventory with an item
    game_character = seed_character()
    game_item = seed_game_item()
    game_character.character.game_items.append(game_item)
    db.commit()
    db.refresh(game_character.character)
    assert game_item in game_character.character.game_items
    
    # Define a lambda function for throwing away an item
    def llm_fake(prompt):
        assert "throw away" in prompt.lower()
        assert "gameitem" in prompt.lower()
        assert str(game_item.id) in prompt.lower()
        return GameLLMResponse(sql="DELETE FROM character_game_items WHERE character_id=%d AND game_item_id=%d;" % (game_character.character.id, game_item.id))
    
    game_engine.llm = llm_fake

    # Perform the throw away action
    action_text = "Throw away {GameItem:%d}" % game_item.id
    game_engine.act(game_character.character_id, action_text)

    # Check that the action has the expected outcome
    assert game_item not in game_character.character.game_items

