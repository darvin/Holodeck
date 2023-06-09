
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)



openai_generation_temperature = 0.9

# style = "nvinkpunk"
#img_gen_model = "Envvi/Inkpunk-Diffusion"


styles = [   #"hand drawn watercolor"
# "detailed unreal engine pixel art.",
# "renaissance aesthetic, pastel colors aesthetic, intricate fashion clothing, highly detailed, surrealistic, digital painting, concept art, sharp focus, illustration",
# " highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha",
#"nvinkpunk minimalism, by adrian ghenie, esao andrews, jenny saville, edward hopper, surrealism, dark art by james jean, takato yamamoto",
# "intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by otomo katsuhiro and hyung-tae kim and oshii mamoru",
#  "tristan eaton, victo ngai, artgerm, rhads, ross draws, sharpness, symmetrical",
#  "hd, vibrant color, high contrast, digital illustration",
#  "hyperdetailed, cinematic lighting",
]
# img_gen_model = "runwayml/stable-diffusion-v1-5"
#img_gen_model = "stabilityai/stable-diffusion-2-1"
# img_gen_model = "prompthero/openjourney"




# # very fast
styles = ["intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by otomo katsuhiro and hyung-tae kim and oshii mamoru",]
img_gen_model = "runwayml/stable-diffusion-v1-5"

location_prompts = [
    # "steampunk city with skyscrapers",
    # "cyberpunk village in Japanese rustic style",
    "fantasy dungsseons and dragons",
    "noir city from 1930s",
    # "StarTrek inspired spaceship",
    # "undeground mine of goblins",
    # "SuperMario style magic land plain",
    # "SuperMario style magic land beach",
]
