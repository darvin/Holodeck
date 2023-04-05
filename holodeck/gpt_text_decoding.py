import json
import yaml
import toml
from yamlfix import fix_code



def clean_line_by_line(text):
    lines = text.split('\n')
    for i in range(len(lines)):
        line = lines[i].strip(" .(")
        if line.count('"') == 1:
            line += '"'
        lines[i] = line
    return '\n'.join(lines)


def detoml(chain_response):
    text = chain_response['text']
    toml_start = text.find('```')
    toml_end = text.rfind('```')
    if toml_start != -1 and toml_end == toml_end:
        toml_end = len(text)-1
    if toml_start != -1 and toml_end != -1 and toml_start < toml_end:
        text = text[toml_start+3:toml_end].strip()

    # print(f"> STRIPPED: ---\n{text}<<<\n")

    text = clean_line_by_line(text)
    text = text.strip(' `')
    # print(f"> FIXED: ---\n{text}<<<\n")


    while True:
        try:
            obj = toml.loads(text)
            if 'root' in obj:
                obj = obj['root']
            print(f"<\n{obj}\n")
            if obj is dict:
                obj = {key.lower(): value for key, value in obj.items()}
            return obj
        except Exception as e:
            lines = text.split('\n')
            if len(lines) == 1:
                print(f"ERROR DECODING: \n'{chain_response['text']}<<<\n")
                raise e
            text = '\n'.join(lines[:-1])

def deyaml(chain_response):
    text = chain_response['text']
    yaml_start = text.find('```')
    yaml_end = text.rfind('```')
    if yaml_start != -1 and yaml_end == yaml_start:
        yaml_end = len(text)-1
    if yaml_start != -1 and yaml_end != -1 and yaml_start < yaml_end:
        text = text[yaml_start+3:yaml_end].strip()

    # print(f"> STRIPPED: ---\n{text}<<<\n")

    # text = fix_code(text)
    # print(f"> FIXED: ---\n{text}<<<\n")


    while True:
        try:
            obj = yaml.safe_load(text)
            print(f"<\n{obj}\n")
            return obj
        except:
            lines = text.split('\n')
            if len(lines) == 1:
                print(f"UNABLE TO DECODE: \n {chain_response['text']}\n")
                raise e
            text = '\n'.join(lines[:-1])
            if len(lines) <= 2:
                print(f"UNABLE TO DECODE: \n {chain_response['text']}\n")
                break



def dejson(chain_response):
    text = chain_response['text']
    json_start = text.find('```json')
    json_end = text.rfind('```')
    if json_start != -1 and json_end == json_start:
        json_end = len(text) - 1
    if json_start != -1 and json_end != -1 and json_start < json_end:
        text = text[json_start + 7:json_end].strip()

    while True:
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            lines = text.split('\n')
            if len(lines) == 1:
                raise e
            text = '\n'.join(lines[:-1])
            if len(lines) <= 2:
                break


if __name__ == "__main__":

    t = '''

```
name = "Earth-Spacecraft Delta"
description = "The colossal spaceship Delta looms above the Earth's atmosphere, nearly blinding the sun's rays with its reflective metallic hull. The airlock opens to the stars, they glimmer in the starry sky. Inside, the grand ship is lined with steel and has nine decks, each level accommodating a variety of technologies. In the hallways, robots scurry around with supplies and maintenance tasks."

[[buildings]]
name = "Hangar"
description = "A large hangar bay with a single door leading to the airlock and to the outside world. Contains numerous spaceships and equipment that are used for missions and exploration."
enterable = true

[[buildings]]
name = "Robotics Bay"
description = "The robotics bay is where robots are constructed and tested. It's a large hall filled with diagnostic and engineering equipment."
enterable = true

[[buildings]]
name = "Bridge"
description = "The bridge is the command center of the spaceship Delta. It is a dimly lit room, filled with computers and displays. The captain sits in the center, overseeing the ship's movements."
enterable = true
    
    '''
    print (detoml({'text':t}))