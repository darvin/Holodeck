from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Response

import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from .generate_image import generate_image, \
                init_generate_image, \
                generate_image_verified



app = FastAPI()



@app.get("/")
async def route_root():
    return {"message": "this is image generation api. use get on /image to generate images"}



@app.get("/image",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
async def route_generate_image(prompt:str, negative_prompt:str, api_token:str):
    if api_token != SECRET_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    if len(prompt) < 5:
        raise HTTPException(status_code=402, detail="Promt must be longer!")
    image_bytes = await generate_image(prompt, negative_prompt)
    # Return the image as a response
    return Response(content=image_bytes, media_type="image/png")


@app.get("/image_verified",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
async def route_generate_image_verified(prompt:str, negative_prompt:str, api_token:str, max_attempts:int = 3):
    if api_token != SECRET_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    if len(prompt) < 5:
        raise HTTPException(status_code=402, detail="Promt must be longer!")
    image_bytes = await generate_image_verified(prompt, negative_prompt, max_attempts)
    # Return the image as a response
    return Response(content=image_bytes, media_type="image/png")





 


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)
SECRET_API_TOKEN = os.environ.get('HOLOIMAGE_API_TOKEN')
