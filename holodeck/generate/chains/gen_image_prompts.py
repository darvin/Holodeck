from langchain.llms import OpenAI
from langchain.chains import LLMChain
from helpers.gpt_text_decoding import detoml
from ...helpers.retry import retry

from ...settings import openai_generation_temperature, styles

from langchain.prompts import PromptTemplate
import toml




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


