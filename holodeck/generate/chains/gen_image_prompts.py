from langchain.llms import OpenAI
from langchain.chains import LLMChain
from ...helpers.retry import retry

from ...settings import openai_generation_temperature, styles

from langchain.prompts import PromptTemplate
import toml


prompt_encounters_sample_location = toml.dumps(toml.loads(
"""
name = "Jungle of the Laughing Monkeys"
description = "A dense jungle."

[[buildings]]
name = "Stone Altar"
description = "A moss-covered stone altar."
enterable = true

[[buildings]]
name = "Monkey Treehouses"
description = "A network of small treehouses."
enterable = true

[[ways]]
name = "Jungle Path"
description = "A narrow path winding through the thick jungle."

[[ways]]
name = "River"
description = "A fast-moving river runs along the edge of the jungle."
"""
))

prompt_encounters_sample_encounters= toml.dumps(toml.loads(
"""
[[root]]
probability = 0.1
description = "As you enter jungles, you find a wallet lost by traveler"

  [root.trigger]
  type = "location"

  [[root.actions]]
  type = "item"
  description = "Wallet of gold"

[[root]]
probability = 0.3
description = "On altar you find an ancient inscribing"

  [root.trigger]
  type = "building"
  building = "Stone Altar"

  [[root.actions]]
  type = "building"
  name = "Ancient Inscribing"
  description = "Ancient inscribing in an unfamiliar language"

[[root]]
probability = 0.02
description = "As you read the ancient inscribing, the evil Demon of Monkeylord appears!"

  [root.trigger]
  type = "building"
  building = "Ancient Inscribing"

  [[root.actions]]
  type = "character"
  name = "Demon of Monkeylord"
  description = "Evil ancient demon with both horns and tail! Only attacks good people."

[[root]]
probability = 0.1
description = "A group of non-sentient monkeys play on the path"

  [root.trigger]
  type = "way"
  way = "Jungle Path"

  [[root.actions]]
  type = "critter"
  description = "Group of non-sentient monkeys. Not aggressive unless provoked."
"""
))


prompt_encounters = PromptTemplate(
    input_variables=["toml", "sample_encounters", "sample_location"],
    template="""
    act as Random Encounter Generator. you will be given a toml with description of location, for example:

```
{sample_location}
```

you must respond with a toml containing all possible random encounters, for example:

```
{sample_encounters}
```

make sure that every way, critter, character, building and item have unique 'name' AND 'description'! add at least 1 critter and 1 character!

first user's input: 

```
{toml}
```

do not output any explanations!
output valid toml (lowercase keys) of encounters in code block
    """
)



prompt_location_sample_location = toml.dumps(toml.loads(
'''
name = "Plains north of Castle Little Rock"
description = """
A field of lilies with a castle wall visible. The road splits in two: one continues north to the forest, while the other goes east to the sea. There is a deep, dried-up well near the fork.
"""

[[buildings]]
name = "Dried-up well"
description = "An ancient well grown over with moss. It dried up centuries ago."
enterable = true

[[buildings]]
name = "Castle wall"
description = "The southern wall of Castle Little Rock. Unscalable!"

[[ways]]
name = "Road to North"
description = "A road that leads to the forest."

[[ways]]
name = "Road to East"
description = "A road that leads to the sea."

'''
))

prompt_location = PromptTemplate(
    input_variables=["prompt", "sample_location"],
    template="""
act as location generator. use user's prompt as an inspiration to create a playable location in fantasy setting. 

Location must include brief description of the 1 square mile of landscape with all features, enterable or interactable static constructions, and ways to leave, for example:

```
{sample_location}
```

note that only name, description, buildings and ways are correct keys

first user's prompt is: "{prompt}"

you must output correct toml (lowercase keys) in a code block for easier copying
make sure that every building, way and location have unique 'name' and 'description'!
""")



prompt_image_sample = {
    'prompt':"prompt goes here",
    'negative_prompt':"negative_prompt goes ehere"
}

prompt_image_intro = f"""
you must describe the object to a blind artist! describe the object, be extremly concise: omit words not neccessary for visual description. amount of words is limited to amount similiar to the sample. describe only what is visible, style guidance and camera directions, strictly following following samples:
"""

prompt_image_building = PromptTemplate(
    input_variables=["building", "location"],
    template= prompt_image_intro +"""
A futuristic laboratory with glowing screens, robotic arms, and sparking electricity. sci-fi, cyberpunk, (first-person view)
A spooky haunted house with creaky floorboards, dusty cobwebs, and flickering candles. horror, spooky, (first-person view)
    
 <description of location>, <detail1>, <detail2>, <style direction>, (<appropriate camera direction>)


the building is located at {location}. describe the building, not location!


"{building}"

your description in given format:
""",
)


prompt_image_character = PromptTemplate(
    input_variables=["character", "location"],
    template= prompt_image_intro + """
portrait of fierce dark-skinned male pirate, black bandana, bushy beard, brown eyes, sword-wielding, adventure, (tropical island with a shipwreck in the background:1.9)

portrait of quirky light-skinned female scientist, thick-rimmed glasses, frizzy hair, excited brown eyes, conducting experiments, science, futuristic laboratory with advanced equipment in the background

portrait of <description of character>, <what's on the head>, <face features>, <eyes>, <words that associated with character appearance, comma separated>, <environment> on background, 


    
location of character is {location}

"{character}"

your description in given format:
""")


prompt_image_item = PromptTemplate(
    input_variables=["item", "location"],
    template= prompt_image_intro + """
close-up of a worn leather bag, with a gleaming revolver and a jangling stack of gold coins spilling out, dangerous and alluring, (dingy saloon with shadowy figures in the background:1.9)

image of a polished silver pocket watch, with intricate clockwork and a gleaming chain, (Victorian-era mansion with flickering candlelight and antique furniture:1.9)

<camera direction> of <description of item>, <detail1>, <detail2>, <style direction> (<environment>:1.9)

    
location where item is found - {location}. use it only for styling hints! don't mention it and choose any appropiate background for item


"{item}"

your description in given format:
""")

prompt_image_critter = PromptTemplate(
    input_variables=["critter", "location"],
    template= prompt_image_intro + """
tracking shot of the monstrous Kraken, with massive tentacles emerging from the depths of the ocean, terrorizing a ship, mythological, (stormy ocean with a lighthouse in the background:1.9)

aerial shot of the majestic white unicorn, with shimmering horn and rainbow mane, galloping through a meadow, magical, (enchanted forest with fairy lights in the background:1.9)

overhead shot of the mystical phoenix, with fiery wings spreading wide, feathers glowing in the sunlight, reborn from its ashes, legendary, (ancient temple ruins in the background:1.9)

<appropriate camera direction> of <description of creature>, <detail1>, <detail2>, (<environment>:1.9)


    
location where creature is found - {location}. use it only for styling hints! don't mention it and choose any appropiate background for item


"{critter}"

your description in given format:
""")


prompt_image_location = PromptTemplate(
    input_variables=["location", "buildings"],
    template=prompt_image_intro + """
A steampunk airship with propellers, smokestacks, and gleaming brass. victorian, brass, (aerial view)
A sprawling cyberpunk city with neon signs, holographic billboards, and towering skyscrapers. futuristic, sci-fi, (panoramic view)

 <description of location>, <detail1>, <detail2>, <style direction>, (<appropriate camera direction>)



"a location one square mile, described as following:
{location}
following is present on this location:
{buildings}"
you need to describe whole location, do not focus on buildings!

your description in given format:
""")




from itertools import cycle
style_cycle = cycle(styles)


def image_prompt_process(response):
    return f"{response['text']} {next(style_cycle)}"


@retry(3)
def gen_location_image_prompt(location, llm=OpenAI(temperature=openai_generation_temperature)):
    chain_image_location = LLMChain(llm=llm, prompt=prompt_image_location)

    return image_prompt_process(chain_image_location({
        'location':location.description,
        'buildings':"\n".join([f"{b.name}: {b.description}" for b in location.buildings]),
        'style':style,
    }))

@retry(3)
def gen_building_image_prompt(building, location, llm=OpenAI(temperature=openai_generation_temperature)):
    chain_image_building = LLMChain(llm=llm, prompt=prompt_image_building)

    return image_prompt_process(chain_image_building({
        'location':location.description,
        'building':f"{building.name}: {building.description}",
        'style':style,
    }))

@retry(3)
def gen_item_image_prompt(object, location, llm=OpenAI(temperature=openai_generation_temperature)):
    chain_image_item = LLMChain(llm=llm, prompt=prompt_image_item)
    return image_prompt_process(chain_image_item({
        'location':location.description,
        'item':f"{object.name}: {object.description}",
        'style':style,
    }))

@retry(3)
def gen_character_image_prompt(object, location, llm=OpenAI(temperature=openai_generation_temperature)):
    chain_image_character = LLMChain(llm=llm, prompt=prompt_image_character)
    return image_prompt_process(chain_image_character({
        'location':location.description,
        'character':f"{object.name}: {object.description}",
        'style':style,
    }))


