from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from io import BytesIO
from fastapi import FastAPI, HTTPException, Response
from PIL import Image
import torch
from transformers import pipeline
import numpy as np

import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from diffusers import StableDiffusionPipeline
import torch

app = FastAPI()





def generate_image(prompt):
    return pipe(prompt).images[0]

@app.get("/")
async def root():
    return {"message": "this is image generation api. use get on /image to generate images"}



@app.get("/image")
async def generate_image(prompt:str, api_token:str):
    if api_token != SECRET_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    if len(prompt) < 5:
        raise HTTPException(status_code=402, detail="Promt must be longer!")

    # Generate an image using the model
    # output = image_generator("A colorful bird", return_tensors="pt")
    
    output = pipe(prompt).images[0]
    # Convert the output tensor to a PIL image
    output_image = Image.fromarray(np.uint8(output)).convert('RGB')

    # Convert the PIL image to a byte stream
    byte_io = BytesIO()
    output_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    
    # Return the image as a response
    return Response(content=byte_io.getvalue(), media_type="image/png")



def init_pipe():
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.safety_checker = lambda images, **kwargs: (images, [False] * len(images))
    pipe = pipe.to("cuda")
    return pipe


 


# model_id = "prompthero/openjourney-v4"
model_id = "Envvi/Inkpunk-Diffusion"
# model_id = "runwayml/stable-diffusion-v1-5"
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)
SECRET_API_TOKEN = os.environ.get('HOLOIMAGE_API_TOKEN')
pipe = init_pipe()