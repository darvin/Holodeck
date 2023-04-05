# prompt_image_building, prompt_encounters, prompt_image_location, prompt_location, prompt_image_object
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
  description = "Wallet full of gold"

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

make sure that every way, critter, character, building and item have unique 'name' and 'description'!

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


image_sample1 = {
    'prompt':"(Digital Artwork:1.3) of (Technical illustration:1) nvinkpunk, long shot of a man wearing an astronaut suit standing on the surface of a planet with a red sun in the sky in the middle of a storm, masterpiece, realistic, high resolution, very detailed, greeble, intricate, centered, face focus,(by Artist WLOP:1.3),Highly Detailed,Featured on CGSociety,Trending on ArtStation.",
    'negative_prompt':"Scribbles,Low quality,Low rated,Mediocre,3D rendering,Screenshot,Software,UI,((watermark)),(text),(overlay),getty images,(cropped),low quality,worst quality"
}

image_sample2 = {
    'prompt':"(Digital Artwork:1.3) of (Technical illustration:1) nvinkpunk, upper body portrait of a beautiful green-eyed (brunette:1.4) woman wearing an astronaut suit and cowboy hat looking at the camera, background is the surface of a planet with a red sun in the sky in the middle of a storm, spacecowboy, masterpiece, realistic, high resolution, very detailed, greeble, intricate, centered, face focus, Highly Detailed, Featured on CGSociety, Trending on ArtStation",
    'negative_prompt':"helmet, Scribbles, Low quality, Low rated,Mediocre,3D rendering, Screenshot, Software, UI,((watermark)),(text),(overlay), getty images,(cropped),low quality, worst quality"
}

prompt_image_intro = f"""
Act as Stable Diffusion prompt generator. 

if user says: "astranaut on mars", respond with following correct toml, without any explanations:
{toml.dumps(image_sample1)}


if user says "woman space cowboy", respond with following TOML:
{toml.dumps(image_sample2)}

Try adding celebrity names with low emphasis eg "nvinkpunk beautiful woman, [[taylor swift]].

Maximum allowed length of the prompt is 77 tokens
"""

prompt_image_building = PromptTemplate(
    input_variables=["building", "location"],
    template= prompt_image_intro +"""


output prompt for the following building: {building}

located in place with following description: "{location}"


""",
)


prompt_image_object = PromptTemplate(
    input_variables=["object", "location"],
    template= prompt_image_intro + """
    
focus attention on object, not surroundings: only use description of location of the object for hints about small details you could add into the picture. Do not describe location! Describe object. 

output prompt for the following object: {object}

located in place with following description: "{location}"
""")


prompt_image_location = PromptTemplate(
    input_variables=["location", "buildings"],
    template=prompt_image_intro + """
 must be included in prompt! 

use user's prompt as an inspiration to create the best 
possible prompt to draw a a highly detailed, playable in a game with top down view 
description of one square mile location. make sure that prompt that you create does NOT includes 
adventurers or any other characters not referred directly in user's prompt

be extremely concise! focus on the extra features, such as buildings. maximum allowed length of prompt is 77 tokens.

first user's prompt is:

{location}

following buildings are present on this location:
{buildings}


""")