import os
from helpers.gpt_text_decoding import detoml
import yaml

from ..helpers import retry
from ..settings import styles

style = styles[0]

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from .prompts import *

from ..models import *
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.ERROR)



llm = OpenAI(temperature=0.9)


chain_location = LLMChain(llm=llm, prompt=prompt_location)
chain_encounters = LLMChain(llm=llm, prompt=prompt_encounters)
chain_image_building = LLMChain(llm=llm, prompt=prompt_image_building)
chain_image_location = LLMChain(llm=llm, prompt=prompt_image_location)
chain_image_item = LLMChain(llm=llm, prompt=prompt_image_item)
chain_image_critter = LLMChain(llm=llm, prompt=prompt_image_critter)
chain_image_character = LLMChain(llm=llm, prompt=prompt_image_character)




def generate_location_and_encounters(prompt):
    location = detoml(chain_location({
        'prompt':prompt,
        'sample_location':prompt_location_sample_location,
    }))
    encounters = detoml(chain_encounters(
        {
        'toml':toml.dumps(location),
        'sample_location':prompt_encounters_sample_location,
        'sample_encounters':prompt_encounters_sample_encounters,
    }
    ))
    return (location, encounters or [])


from itertools import cycle
style_cycle = cycle(styles)


def image_prompt_process(response):
    return f"{response['text']} {next(style_cycle)}"




@retry(3)
def generate_location_image_prompt(location):
    return image_prompt_process(chain_image_location({
        'location':location.description,
        'buildings':"\n".join([f"{b.name}: {b.description}" for b in location.buildings]),
        'style':style,
    }))

@retry(3)
def generate_building_image_prompt(building, location):
    return image_prompt_process(chain_image_building({
        'location':location.description,
        'building':f"{building.name}: {building.description}",
        'style':style,
    }))

@retry(3)
def generate_item_image_prompt(object, location):
    return image_prompt_process(chain_image_item({
        'location':location.description,
        'item':f"{object.name}: {object.description}",
        'style':style,
    }))

@retry(3)
def generate_character_image_prompt(object, location):
    return image_prompt_process(chain_image_character({
        'location':location.description,
        'character':f"{object.name}: {object.description}",
        'style':style,
    }))


@retry(3)
def generate_critter_image_prompt(object, location):
    return image_prompt_process(chain_image_critter({
        'location':location.description,
        'critter':f"{object.name}: {object.description}",
        'style':style,
    }))

def generate_object_image_prompt(object, location):
    if isinstance(object, Critter):
        return generate_critter_image_prompt(object, location)
 
    if isinstance(object, Character):
        return generate_character_image_prompt(object, location)
    if isinstance(object, Item):
        return generate_item_image_prompt(object, location)


import traceback

if __name__ == "__main__":

    from game_objects import initialize_location
    location_dict, encounters_list = generate_location_and_encounters("futuristic city flying cars crazy steampunk")

    try:
        location = initialize_location(location_dict, encounters_list)
    except KeyError as e:
        print("Error: Key not found -", e)
        traceback.print_exc()
    # location_image_prompt = generate_location_image_prompt(location)

    objects_image_prompts = [(o, generate_object_image_prompt(o, location)) for o in location.objects]
    buildings_image_prompts = [(b, generate_object_image_prompt(b, location)) for b in location.all_buildings]
    
    print(objects_image_prompts)

    print(buildings_image_prompts)
