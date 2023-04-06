
from .holoimage_client import AsyncApis, ApiClient
# from .holoimage_client import ApiException
from pprint import pprint
import os
from .settings import *
import requests
import io


async def generate_image_holoimage(prompt, negative_prompt):
    # Create an instance of the API class
    api_instance = AsyncApis(ApiClient(os.environ.get('HOLOIMAGE_API_URL'))).default_api
    api_token = os.environ.get('HOLOIMAGE_API_TOKEN')

    try:
        # Route Generate Image
        api_response = await api_instance.route_generate_image_verified_image_verified_get(prompt, negative_prompt, api_token, max_attempts=1)
        return api_response
    except Exception as e:
        print("Exception when calling DefaultApi->route_generate_image_image_get: %s\n" % e)

async def generate_image_huggingface(prompt):
    API_URL = "https://api-inference.huggingface.co/models/Envvi/Inkpunk-Diffusion"
    api_token = os.environ.get('HUGGINGFACE_API_KEY')

    headers = {"Authorization": f"Bearer {api_token}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    image_bytes = query({
        "inputs": prompt,
    })
    return io.BytesIO(image_bytes)

async def generate_image(prompt, negative_prompt):
    # return await generate_image_holoimage(prompt, negative_prompt)
    return await generate_image_huggingface(prompt)

if __name__=="__main__":
    print(generate_image('The entire Cobalt Building of Machines is visible. Machines with intricate cogs and tubes, steampunk pipes, and colorful cobalt energy coursing through them on background of the bustling futuristic city with flying cars during the afternoon with warm lighting. nvinkpunk'))