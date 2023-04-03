import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)


from langchain.llms import OpenAI
from langchain.chains import LLMChain
import yaml
from prompts import *

llm = OpenAI(temperature=0.9)


chain_location = LLMChain(llm=llm, prompt=prompt_location)
chain_encounters = LLMChain(llm=llm, prompt=prompt_encounters)
chain_image_building = LLMChain(llm=llm, prompt=prompt_image_building)
chain_image_location = LLMChain(llm=llm, prompt=prompt_image_location)
chain_image_object = LLMChain(llm=llm, prompt=prompt_image_object)


import yaml

def deyaml(chain_response):
    text = chain_response['text']
    yaml_start = text.find('```')
    yaml_end = text.rfind('```')
    if yaml_start != -1 and yaml_end == -1:
        yaml_end = len(text)-1
    if yaml_start != -1 and yaml_end != -1 and yaml_start < yaml_end:
        text = text[yaml_start+3:yaml_end].strip()

    while True:
        try:
            return yaml.safe_load(text)
        except yaml.scanner.ScannerError as e:
            lines = text.split('\n')
            if len(lines) == 1:
                raise e
            text = '\n'.join(lines[:-1])
            if len(lines) <= 2:
                break



def generate_location_and_encounters(prompt):
    location = deyaml(chain_location("futuristic city flying cars crazy steampunk"))
    encounters = deyaml(chain_encounters(yaml.dump(location)))
    return (location, encounters or [])


def generate_location_image_prompt(location):
    return chain_image_location({
        'location':location.description,
        'buildings':"\n".join([f"{b.name}: {b.description}" for b in location.buildings])
    })['text']

def generate_building_image_prompt(building, location):
    return chain_image_building({
        'location':location.description,
        'building':f"{building.name}: {building.description}",
    })['text']


def generate_object_image_prompt(object, location):
    return chain_image_object({
        'location':location.description,
        'object':f"{object.name}: {object.description}",
    })['text']

if __name__ == "__main__":

    from game_objects import initialize_location
    location_dict, encounters_list = generate_location_and_encounters("futuristic city flying cars crazy steampunk")
    location = initialize_location(location_dict, encounters_list)
    # location_image_prompt = generate_location_image_prompt(location)

    objects_image_prompts = [(o, generate_object_image_prompt(o, location)) for o in location.objects]
    buildings_image_prompts = [(b, generate_object_image_prompt(b, location)) for b in location.all_buildings]
    
    print(objects_image_prompts)

    print(buildings_image_prompts)
