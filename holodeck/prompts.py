# prompt_image_building, prompt_encounters, prompt_image_location, prompt_location, prompt_image_object
from langchain.prompts import PromptTemplate
import json
import yaml

prompt_image_building = PromptTemplate(
    input_variables=["building", "location"],
    template="""

generate Midjourney prompt, using following formula:

"An image of a [building] [highly detailed imaginative description of the building] during [time of day] with [type of lighting] and shot using [name of lens] - at 16:9. nvinkpunk"

follow formula!

output prompt for the following building: {building}

located in place with following description: "{location}"


""",
)

prompt_encounters_sample_location = json.dumps(yaml.safe_load(
"""
name: Jungle of the Laughing Monkeys
description: >
  A dense jungle.
buildings:
  - name: Stone Altar
    description: A moss-covered stone altar.
    enterable: true
  - name: Monkey Treehouses
    description: A network of small treehouses.
    enterable: true
ways:
  - name: Jungle Path
    description: A narrow path winding through the thick jungle.
  - name: River
    description: A fast-moving river runs along the edge of the jungle.
"""
))

prompt_encounters_sample_encounters= json.dumps(yaml.safe_load(
"""
---
- probability: 0.1
  description: As you enter jungles, you find a wallet lost by traveler
  trigger:
    type: location
  actions:
    - type: item
      description: Wallet full of gold
- probability: 0.3
  description: On altar you find an ancient inscribing
  trigger:
    type: building
    building: Stone Altar
  actions:
    - type: building
      name: Ancient Inscribing
      description: Ancient inscribing in an unfamiliar language
- probability: 0.02
  description: As you read the ancient inscribing, the evil Demon of Monkeylord appears!
  trigger:
    type: building
    building: Ancient Inscribing
  actions:
    - type: character
      name: Demon of Monkeylord
      description: Evil ancient demon with both horns and tail! Only attacks good people.
- probability: 0.1
  description: A group of non-sentient monkeys play on the path
  trigger:
    type: way
    way: Jungle Path
  actions:
    - type: critter
      description: Group of non-sentient monkeys. Not aggressive unless provoked.
"""
))


prompt_encounters = PromptTemplate(
    input_variables=["json", "sample_encounters", "sample_location"],
    template="""
    act as Random Encounter Generator. you will be given a JSON with description of location, for example:

```
{sample_location}
```

you must respond with a JSON containing all possible random encounters, for example:

```
{sample_encounters}
```

first user's input: 

```
{json}
```

do not output any explanations!
output valid JSON of encounters in code block
    """
)

prompt_image_location = PromptTemplate(
    input_variables=["location", "buildings"],
    template="""
act as Midjourney prompt generator. use user's prompt as an inspiration to create the best 
possible prompt to draw a a highly detailed, playable in a game with top down view 
description of one square mile location. make sure that prompt that you create does NOT includes 
adventurers or any other characters not referred directly in user's prompt

to generate that prompt, you MUST follow formula:

"An aerial photograph of a [landscape] with [each building mentioned] during [time of day] with [type of lighting] using [name of lens] — at 16:9. nvinkpunk"

be extremely concise! focus on the extra features, such as buildings.

first user's prompt is:

{location}

following buildings are present on this location:
{buildings}

don't output explanations, prompt only

""")


prompt_location_sample_location = json.dumps(yaml.safe_load(
"""
---
name: Plains north of Castle Little Rock
description: >
  A field of lilies with a castle wall visible. The road splits in
  two: one continues north to the forest, while the other goes east to the sea.
  There is a deep, dried-up well near the fork.
buildings:
  - name: Dried-up well
    description: An ancient well grown over with moss. It dried up centuries ago.
    enterable: true
  - name: Castle wall
    description: The southern wall of Castle Little Rock. Unscalable!
ways:
  - name: Road to North
    description: A road that leads to the forest.
  - name: Road to East
    description: A road that leads to the sea.
"""
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

you must output correct JSON in a code block for easier copying
""")

prompt_image_object = PromptTemplate(
    input_variables=["object", "location"],
    template="""
generate Midjourney prompt, using following formula:
"The entire [object] is visible. [object] with [all specific details] on background of [description of object's background] during [time of day] with [type of lighting]. nvinkpunk"

focus attention on object, not surroundings: only use description of location of the object for hints about small details you could add into the picture. Do not describe location! Describe object. follow formula!

output prompt for the following object: {object}

located in place with following description: "{location}"
""")


