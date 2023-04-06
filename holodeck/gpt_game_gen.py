
import random
import base64
import uuid
import base64
from .game_objects import Location, \
                        Building, \
                        Way, \
                        Character, \
                        Item, Critter, \
                        Trigger, TriggerType, \
                        Encounter, \
                        Action

def generate_short_uuid():
    uuid_bytes = uuid.uuid4().bytes_le
    short_uuid_bytes = base64.urlsafe_b64encode(uuid_bytes)[:6]
    short_uuid = short_uuid_bytes.decode('utf-8')
    return short_uuid

def get_randomized_id():
    return generate_short_uuid()


def initialize_location(location_dict, encounters_list):
    def get_location_number():
        return get_randomized_id()

    def get_critter_number():
        return get_randomized_id()
    
    def get_item_number():
        return get_randomized_id()


    def get_building_number():
        return get_randomized_id()


    def get_character_number():
        return get_randomized_id()
    
    def get_way_number():
        return get_randomized_id()


    location = Location(location_dict.get('name', f"Location {get_location_number()}"), location_dict.get('description', ""))
    for building_dict in location_dict.get('buildings', []) or []:
        building = Building(building_dict.get('name', f"Building {get_building_number()}"), building_dict.get('description', ""), building_dict.get('enterable', False))
        location.add_building(building)
    for way_dict in location_dict.get('ways', []):
        try:
            way = Way(way_dict.get('name', f"Way {get_way_number()}"), way_dict.get('description', ""))
            location.add_way(way)
        except TypeError:
            pass # fixme. happens when GPT returns 'way: Name of Way' - one liner :(

    for encounter_dict in encounters_list:
        if not encounter_dict.get('trigger') or \
            not encounter_dict.get('probability') or \
            not encounter_dict.get('description'):
            continue
        probability = encounter_dict['probability']
        description = encounter_dict['description']

        trigger_dict = {}
        if isinstance(encounter_dict['trigger'] , list):
            trigger_dict = encounter_dict['trigger'][0]
        else:
            trigger_dict = encounter_dict['trigger']

        trigger_type = trigger_dict['type']
        trigger = None
        if trigger_type.upper() == TriggerType.WAY.name:
            trigger = Trigger(TriggerType.WAY, way=trigger_dict.get('way'))
        elif trigger_type.upper() == TriggerType.BUILDING.name:
            trigger = Trigger(TriggerType.BUILDING, building=trigger_dict.get('building'))
        actions = []
        for action_dict in encounter_dict.get('actions', []) or []:
            action_type = action_dict['type'].strip()
            if action_type in ['character', 'ship', 'vessel', 'characters']:
                action_obj = Character(action_dict.get('name', f"Character {get_character_number()}"), action_dict['description'])
            elif action_type == 'item':
                action_obj = Item(action_dict.get('name', f"Item {get_item_number()}"), action_dict['description'])
            elif action_type in ['critter', 'creature', 'computer']:
                action_obj = Critter(action_dict.get('name', f"Critter {get_critter_number()}"), action_dict['description'])
            elif action_type == 'building':
                action_obj = Building(action_dict.get('name', f"Building {get_building_number()}"), action_dict['description'], True)
            else:
                print(f"unknown type! {action_type}")
            actions.append(Action(action_type, action_obj))
        encounter = Encounter(probability, description, trigger, actions)
        location.add_encounter(encounter)
    return location


if __name__ == "__main__":
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

    print(initialize_location(location_dict, encounters_list))