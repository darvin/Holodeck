from enum import Enum

class TriggerType(Enum):
    WAY = 1
    BUILDING = 2

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.buildings = []
        self.ways = []
        self.encounters = []

    def add_encounter(self, encounter):
        self.encounters.append(encounter)

    def add_building(self, building):
        self.buildings.append(building)

    def add_way(self, way):
        self.ways.append(way)

    def __str__(self):
        buildings_str = "\n  ".join([str(b) for b in self.buildings])
        ways_str = "\n  ".join([str(w) for w in self.ways])
        encounters_str = "\n  ".join([str(e) for e in self.encounters])
        return f"{self.name}\n{self.description}\n\nBuildings:\n  {buildings_str}\n\nWays:\n  {ways_str}\n\nEncounters:\n  {encounters_str}"

    @property
    def objects(self):
        objects = []
        for encounter in self.encounters:
            for action in encounter.actions:
                if isinstance(action, Item) or isinstance(action, Critter) or isinstance(action, Character):
                    objects.append(action)
        return objects

    @property
    def all_buildings(self):
        all_buildings = []
        for building in self.buildings:
            all_buildings.append(building)
        for encounter in self.encounters:
            for action in encounter.actions:
                if isinstance(action, Building):
                    all_buildings.append(action.building)
        return all_buildings
    
class Way:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        
    def __str__(self):
        return f"{self.name}: {self.description}"

class Building:
    def __init__(self, name, description, enterable):
        self.name = name
        self.description = description
        self.enterable = enterable

    def __str__(self):
        enter_str = "Enterable" if self.enterable else "Not enterable"
        return f"{self.name}: {self.description} ({enter_str})"

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __str__(self):
        return f"{self.name}: {self.description}"

class Action:
    def __init__(self, type, description, name=None):
        self.type = type
        self.description = description
        self.name = name

    def __str__(self):
        action_str = f"{self.type_}:\n"
        for key, value in self.__dict__.items():
            if key != "type_":
                action_str += f"{key}: {value}\n"
        return action_str


class Encounter:
    def __init__(self, probability, description, trigger, actions):
        self.probability = probability
        self.description = description
        self.trigger = trigger
        self.actions = actions
    def __str__(self):
        if self.trigger:
            trigger_str = f"{self.trigger.type.name}: {self.trigger.way}" if self.trigger.way else f"{self.trigger.type.name}: {self.trigger.building}"
        else:
            trigger_str = ""
        action_str = "\n".join([f"  {action}" for action in self.actions])
        return f"Encounter ({self.probability * 100}%): {self.description}\nTrigger: {trigger_str}\nActions:\n{action_str}"

class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"

class Critter:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __str__(self):
        return f"{self.name}: {self.description}"
    
class Trigger:
    def __init__(self, type, way=None, building=None):
        self.type = type
        self.way = way
        self.building = building
    
    def __str__(self):
        trigger_str = f"{self.type_.name}: "
        for key, value in self.__dict__.items():
            if key != "type_":
                trigger_str += f"{key}={value}, "
        trigger_str = trigger_str.rstrip(", ")
        return trigger_str


import random
import base64
import uuid
import base64

def generate_short_uuid():
    uuid_bytes = uuid.uuid4().bytes_le
    short_uuid_bytes = base64.urlsafe_b64encode(uuid_bytes)[:6]
    short_uuid = short_uuid_bytes.decode('utf-8')
    return short_uuid

def get_randomized_id():
    return generate_short_uuid()


def initialize_location(location_dict, encounters_list):
    def get_critter_number():
        return get_randomized_id()
    
    def get_item_number():
        return get_randomized_id()


    def get_building_number():
        return get_randomized_id()


    def get_character_number():
        return get_randomized_id()



    location = Location(location_dict['name'], location_dict.get('description', ""))
    for building_dict in location_dict.get('buildings', []) or []:
        building = Building(building_dict.get('name', f"Building {get_building_number()}"), building_dict.get('description', ""), building_dict.get('enterable', False))
        location.add_building(building)
    for way_dict in location_dict.get('ways', []):
        try:
            way = Way(way_dict['name'], way_dict.get('description', ""))
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
        trigger_type = encounter_dict['trigger']['type']
        trigger = None
        if trigger_type.upper() == TriggerType.WAY.name:
            trigger = Trigger(TriggerType.WAY, way=encounter_dict['trigger'].get('way'))
        elif trigger_type.upper() == TriggerType.BUILDING.name:
            trigger = Trigger(TriggerType.BUILDING, building=encounter_dict['trigger'].get('building'))
        actions = []
        for action_dict in encounter_dict.get('actions', []) or []:
            action_type = action_dict['type'].strip()
            if action_type in ['character', 'ship']:
                action = Character(action_dict.get('name', f"Character {get_character_number()}"), action_dict['description'])
            elif action_type == 'item':
                action = Item(action_dict.get('name', f"Item {get_item_number()}"), action_dict['description'])
            elif action_type in ['critter', 'creature']:
                action = Critter(action_dict.get('name', f"Critter {get_critter_number()}"), action_dict['description'])
            elif action_type == 'building':
                action = Building(action_dict.get('name', f"Building {get_building_number()}"), action_dict['description'], True)
            else:
                print(f"unknown type! {action_type}")
            actions.append(action)
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