from langchain.llms import OpenAI
from langchain.chains import LLMChain
from helpers.gpt_text_decoding import detoml
from ...helpers.retry import retry


from ...settings import openai_generation_temperature

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
  description = "    of gold"

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




def gen_location_and_encounters(prompt, llm=OpenAI(temperature=openai_generation_temperature)):
    chain_location = LLMChain(llm=llm, prompt=prompt_location)
    chain_encounters = LLMChain(llm=llm, prompt=prompt_encounters)

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
