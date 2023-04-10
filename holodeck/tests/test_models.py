

from sqlmodel import SQLModel, create_engine
from ..generate.initialize_location import initialize_location

from ..models import TriggerType



db_filepath = ".data/test1db.db"
sqlite_url = f"sqlite+pysqlite:///{db_filepath}"

import os
if os.path.exists(db_filepath):
    os.remove(db_filepath)


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



def test_location_initialization():
    location_dict = \
{'name': 'Sky City Clankersburg',
 'description': 'A large floating city comprised of steampunk-style buildings and vehicles. The city is bustling with activity, and people are zipping around on flying cars of all shapes and sizes. In the center of the city is an airship dock, with several airships coming and going. \n',
 'buildings': [{'name': 'Airship Dock',
   'description': 'A large dock with several airships coming and going.',
   'enterable': True},
  {'name': 'Steampunk-style Buildings',
   'description': 'Several buildings made of various materials and with various contraptions and decorations.'}],
 'ways': [{'name': 'Flying Cars',
   'description': 'Zipping around the city, people fly in all shapes and sized cars.'},
  {'name': 'Airships',
   'description': 'Several airships coming and going from the airship dock.'}]}

    encounters_list = \
[{'probability': 0.2,
  'description': 'You spot a group of street urchins stealing items off the flying cars',
  'trigger': {'type': 'way', 'way': 'Flying Cars'},
  'actions': [{'type': 'critter',
    'description': 'Group of street urchins pilfering items off flying cars'}]},
 {'probability': 0.1,
  'description': 'You see a crew of airship brigands attempting to hijack an airship',
  'trigger': {'type': 'way', 'way': 'Airships'},
  'actions': [{'type': 'character',
    'name': 'Airship Brigands',
    'description': 'A rowdy crew of airship hijackers'}]},
 {'probability': 0.2,
  'description': 'Inside one of the steampunk-style buildings, you find a secret laboratory',
  'trigger': {'type': 'building', 'building': 'Steampunk-style Buildings'},
  'actions': [{'type': 'building',
    'name': 'Secret Laboratory',
    'description': 'A hidden laboratory full of strange contraptions and machinery'}]},
 {'probability': 0.1,
  'description': 'A mysterious figure in a hooded cloak is seen entering one of the airships',
  'trigger': {'type': 'way'}}]

    location = initialize_location(location_dict, encounters_list)
    assert location is not None
    # Test that the location has the correct name and description
    assert location.name == "Sky City Clankersburg"
    assert location.description == "A large floating city comprised of steampunk-style buildings and vehicles. The city is bustling with activity, and people are zipping around on flying cars of all shapes and sizes. In the center of the city is an airship dock, with several airships coming and going. \n"

    # Test that the location has the correct number of buildings and ways_outgoing
    assert len(location.buildings) == 2
    assert len(location.ways_outgoing) == 2

    # Test that the location's buildings have the correct attributes
    assert location.buildings[0].name == "Airship Dock"
    assert location.buildings[0].description == "A large dock with several airships coming and going."
    assert location.buildings[0].enterable == True

    assert location.buildings[1].name == "Steampunk-style Buildings"
    assert location.buildings[1].description == "Several buildings made of various materials and with various contraptions and decorations."
    assert location.buildings[1].enterable == False

    # Test that the location's ways_outgoing have the correct attributes
    assert location.ways_outgoing[0].name == "Flying Cars"
    assert location.ways_outgoing[0].description == "Zipping around the city, people fly in all shapes and sized cars."

    assert location.ways_outgoing[1].name == "Airships"
    assert location.ways_outgoing[1].description == "Several airships coming and going from the airship dock."

    # Test that the location's encounters have been created correctly
    assert len(location.encounters) == 4

    assert location.encounters[0].probability == 0.2
    assert location.encounters[0].description == "You spot a group of street urchins stealing items off the flying cars"

    assert location.encounters[1].probability == 0.1
    assert location.encounters[1].description == "You see a crew of airship brigands attempting to hijack an airship"

    assert location.encounters[2].probability == 0.2
    assert location.encounters[2].description == "Inside one of the steampunk-style buildings, you find a secret laboratory"

    assert location.encounters[3].probability == 0.1
    assert location.encounters[3].description == "A mysterious figure in a hooded cloak is seen entering one of the airships"

    # Test that the triggers for each encounter have been created correctly
    assert len(location.encounters[0].triggers) == 1
    assert location.encounters[0].triggers[0].type == TriggerType.WAY
    assert location.encounters[0].triggers[0].way.name == "Flying Cars"

    assert len(location.encounters[1].triggers) == 1
    assert location.encounters[1].triggers[0].type == TriggerType.WAY
    assert location.encounters[1].triggers[0].way.name == "Airships"

    assert len(location.encounters[2].triggers) == 1
    assert location.encounters[2].triggers[0].type == TriggerType.BUILDING
    assert location.encounters[2].triggers[0].building.name == "Steampunk-style Buildings"

    assert len(location.encounters[3].triggers) == 1
    assert location.encounters[3].triggers[0].type == TriggerType.WAY
    assert location.encounters[3].triggers[0].way == None



