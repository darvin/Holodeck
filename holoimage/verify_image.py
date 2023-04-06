from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import toml
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from helpers.gpt_text_decoding import detoml

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)



image_verify_sample_good = {
    'correct': True,
    'expected': ["dog", "cat", "human"],
    'actual':["wolf", "cat", "woman", "tree", "sun"],
}
image_verify_sample_desription_good = "human, cat and dog in sun-lit forest"


image_verify_sample_prompt = "human is walking with cat and dog"
image_verify_sample_desription_bad = "cat and human in sun-lit forest"

image_verify_sample_bad = {
    'correct': False,
    'expected':["dog", "cat", "human"],
    'actual': ["cat", "human", "tree", "sun"],
    'improved_prompt': "human is walking with cat and (dog:1.1)"
}


prompt_image_verify_intro = f"""

act as image generation verifier. you will be given IMAGE_PROMPT and ACTUAL_IMAGE_DESCRIPTION. you will create EXPECTED_IMAGE_DESCRIPTION like so: list what should definitely on the image, output objects and characters only, not the way the image should be created, its style, without any details, or description of the lighting conditions. Don't be too specific or abstract! Then, compare EXPECTED_IMAGE_DESCRIPTION and all the objects that are present in ACTUAL_IMAGE_DESCRIPTION. If not all are present, create improved prompt by emphasising missing from ACTUAL_IMAGE_DESCRIPTION objects like that: (object that is missing but should be present:1.1). use range of weights from 1.1 to 1.5 for emphasis. be lenient in comparison of the objects!

here is the sample:

<user>: 
IMAGE_PROMPT: "{image_verify_sample_prompt}"
ACTUAL_IMAGE_DESCRIPTION: "{image_verify_sample_desription_bad}"

<assistant>:
```
{toml.dumps(image_verify_sample_bad)}
```

<user>: 
IMAGE_PROMPT: "{image_verify_sample_prompt}"
ACTUAL_IMAGE_DESCRIPTION: "{image_verify_sample_desription_good}"

<assistant>:
```
{toml.dumps(image_verify_sample_good)}
```


"""

prompt_image_verify = PromptTemplate(
    input_variables=["image_description", "prompt"],
    template= prompt_image_verify_intro + """

output TOML with result of generation verification of following:

IMAGE_PROMPT: "{prompt}"
ACTUAL_IMAGE_DESCRIPTION: "{image_description}" 
""")

prompt_image_rephrase = PromptTemplate(
    input_variables=["prompt"],
    template="""
list what should definitely be described on the image if prompt for Midjourney to draw it goes like that: {prompt}
output objects and characters only, not the way the image should be created, its style, in comma separated list, without any details, or description of the lighting conditions.
""") # not used


async def verify_image(image, prompt):
    print(f"ORIGINAL PROMPT: {prompt}\n")

    image_description1 = pipe_description(image)[0]['generated_text']
    print(f"IMG_DESCR1: {image_description1}\n")
    # image_description2 = pipe_description(image)[0]['generated_text']
    # print(f"IMG_DESCR2: {image_description2}\n")
    # image_description3 = pipe_description(image)[0]['generated_text']
    # print(f"IMG_DESCR3: {image_description3}\n")


    # prompt_rephrase = chain_image_rephrase({'prompt': prompt})['text']

    is_good_resp = chain_image_verify({
        'image_description':image_description1, #+ image_description2 + image_description3, 
        'prompt': prompt})
    
    # print(f"PROMPT REPHRASE: {prompt_rephrase}\n")
    # print(f"IMAGE DESCRIPTION: {image_description}\n")
    
    print(f"VERIFIER RESPONCE: {is_good_resp['text']}\n")

    is_good_obj = detoml(is_good_resp)

    print(f"VERIFIER RESPONCE DETOMLED: {is_good_obj}\n\n\n")

    return is_good_obj['correct']

def initialize_verify_image(model_id):
    llm = OpenAI(temperature=0.9)
    chain_image_verify = LLMChain(llm=llm, prompt=prompt_image_verify)
    chain_image_rephrase = LLMChain(llm=llm, prompt=prompt_image_rephrase)
    pipe = pipeline("image-to-text", model=model_id)
    return (chain_image_rephrase, chain_image_verify, pipe)

# model_id = "microsoft/git-large-textcaps" # error input ids
model_id = "Salesforce/blip-image-captioning-large" # works but blah
# model_id = "Salesforce/blip2-opt-6.7b"   ## very good in text outside of app, app freezes if enabled!
chain_image_rephrase, chain_image_verify, pipe_description = initialize_verify_image(model_id)
