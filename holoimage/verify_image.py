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




async def verify_image(image, prompt):
    image_description = pipe_description(image)[0]['generated_text']
    print(image_description)
    is_good_txt = chain_image_verify({'image_description':image_description, 'prompt': prompt})['text'].lower()
    print(is_good_txt)
    is_good = "yes" in is_good_txt or "good" in is_good_txt
    return is_good

def initialize_verify_image():
    llm = OpenAI(temperature=0.9)
    chain_image_verify = LLMChain(llm=llm, prompt=prompt_image_verify)
    pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    return (chain_image_verify, pipe)


chain_image_verify, pipe_description = initialize_verify_image()