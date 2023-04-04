from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

from pathlib import Path
from dotenv import find_dotenv, load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)




prompt_image_verify = PromptTemplate(
    input_variables=["image_description", "prompt"],
    template="""
image is described as following: {image_description} 
    
desired image is such: "{prompt}"

verify that this is good image for whats requested

be extra critical! 

respond with "YES" or "NO"
""")

prompt_image_rephrase = PromptTemplate(
    input_variables=["prompt"],
    template="""
list what should definitely be described on the image if prompt for Midjourney to draw it goes like that: {prompt}
output objects and characters only, not the way the image should be created, its style, in comma separated list, without any details, or description of the lighting conditions.
""")


async def verify_image(image, prompt):
    image_description = pipe_description(image)[0]['generated_text']


    prompt_rephrase = chain_image_rephrase({'prompt': prompt})['text']

    is_good_txt = chain_image_verify({'image_description':image_description, 'prompt': prompt_rephrase})['text'].lower()
    
    print(f"ORIGINAL PROMPT: {prompt}\n")
    print(f"PROMPT REPHRASE: {prompt_rephrase}\n")
    print(f"IMAGE DESCRIPTION: {image_description}\n")
    print(f"VERIFIER RESPONCE: {is_good_txt}\n\n\nc")
    is_good = "yes" in is_good_txt or "good" in is_good_txt
    return is_good

def initialize_verify_image(model_id):
    llm = OpenAI(temperature=0.9)
    chain_image_verify = LLMChain(llm=llm, prompt=prompt_image_verify)
    chain_image_rephrase = LLMChain(llm=llm, prompt=prompt_image_rephrase)
    pipe = pipeline("image-to-text", model=model_id)
    return (chain_image_rephrase, chain_image_verify, pipe)

model_id = "microsoft/git-large-textcaps"
# model_id = "Salesforce/blip-image-captioning-large"
# model_id = "Salesforce/blip2-opt-6.7b"
chain_image_rephrase, chain_image_verify, pipe_description = initialize_verify_image(model_id)
