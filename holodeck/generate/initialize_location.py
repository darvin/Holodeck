
import random
import base64
import uuid
import base64
from ..models import Location, \
                        Building, \
                        Way, \
                        Character, \
                        Item, \
                        Trigger, TriggerType, \
                        Encounter, \
                        Action




def initialize_location(location_dict, encounters_list):

    def generate_short_uuid():
        uuid_bytes = uuid.uuid4().bytes_le
        short_uuid_bytes = base64.urlsafe_b64encode(uuid_bytes)[:6]
        short_uuid = short_uuid_bytes.decode('utf-8')
        return short_uuid

    def get_randomized_id():
        return generate_short_uuid()
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


    location = Location(name=location_dict.get('name', f"Location {get_location_number()}"), 
                        description=location_dict.get('description', ""))
    for building_dict in location_dict.get('buildings', []) or []:
        building = Building(name=building_dict.get('name', f"Building {get_building_number()}"), 
                            description=building_dict.get('description', ""),
                            enterable=building_dict.get('enterable', False))
        location.add_building(building)
    for way_dict in location_dict.get('ways', []):
        try:
            way = Way(name=way_dict.get('name', f"Way {get_way_number()}"), 
                      description=way_dict.get('description', ""))
            location.add_way(way)
        except TypeError:
            pass # fixme. happens when GPT returns 'way: Name of Way' - one liner :(

    def get_or_create_way_by_name(way_name):
        if not way_name:
            return None
        for way in location.ways_outgoing:
            if way.name and  way.name.lower() == way_name.lower():
                return way
        # new way, not found in location!
        way = Way(way_name, f"<a description of way {way_name}>")
        location.add_way(way)
        return way

    def get_or_create_building_by_name(building_name):
        if not building_name:
            return None
        for building in location.all_buildings:
            if building.name and building.name.lower() == building_name.lower():
                #no need to add building cause it may be built on the location per trigger
                return building
        return Building(name=building_name, 
                        description=f"<a description of building {building_name}>",
                        enterable=False)

    for encounter_dict in encounters_list:
        if not encounter_dict.get('trigger') or \
            not encounter_dict.get('probability') or \
            not encounter_dict.get('description'):
            continue
        probability = encounter_dict['probability']
        description = encounter_dict['description']

        triggers_dicts = []
        if isinstance(encounter_dict['trigger'] , list):
            triggers_dicts = encounter_dict['trigger']
        else:
            triggers_dicts = [encounter_dict['trigger']]
        triggers = []
        for trigger_dict in triggers_dicts:
            trigger_type = trigger_dict['type']
            trigger = None
            if trigger_type.upper() == TriggerType.WAY.name and trigger_dict.get('way'):
                trigger = Trigger(type=TriggerType.WAY, 
                                  way=get_or_create_way_by_name(trigger_dict.get('way')))
            elif trigger_type.upper() == TriggerType.WAY.name and trigger_dict.get('way') is None: # any way triggers
                trigger = Trigger(type=TriggerType.WAY)
            elif trigger_type.upper() == TriggerType.BUILDING.name and trigger_dict.get('building'):
                trigger = Trigger(type=TriggerType.BUILDING, 
                                  building=get_or_create_building_by_name(trigger_dict.get('building')))
            if trigger:
                triggers.append(trigger)
        actions = []
        for action_dict in encounter_dict.get('actions', []) or []:
            action_type = action_dict['type'].strip()
            if action_type in ['character', 'ship', 'vessel', 'characters', 'robot']:
                action_obj = Character(name=action_dict.get('name', f"Character {get_character_number()}"),
                                       description=action_dict['description'],
                                       character_type="critter", 
                                       character_subtype=action_type)
            elif action_type == 'item':
                action_obj = Item(name=action_dict.get('name', f"Item {get_item_number()}"),
                                  description=action_dict['description'])
            elif action_type in ['critter', 'creature', 'computer']:
                action_obj = Character(name=action_dict.get('name', f"Critter {get_critter_number()}"), 
                                       description=action_dict['description'],
                                       character_type="critter", 
                                       character_subtype=action_type)
            elif action_type == 'building':
                action_obj = Building(name=action_dict.get('name', f"Building {get_building_number()}"),
                                      description=action_dict['description'],
                                      enterable=True)
            else:
                print(f"unknown type! {action_type}")
            actions.append(Action(action_type, action_obj))
        encounter = Encounter(probability=probability, 
                              description=description, 
                              triggers=triggers, 
                              actions=actions)
        location.add_encounter(encounter)
    return location

