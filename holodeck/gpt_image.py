
from .holoimage_client import AsyncApis, ApiClient
# from .holoimage_client import ApiException
from pprint import pprint
import os
from .settings import *




async def generate_image(prompt, negative_prompt):
    # Create an instance of the API class
    api_instance = AsyncApis(ApiClient(os.environ.get('HOLOIMAGE_API_URL'))).default_api
    api_token = os.environ.get('HOLOIMAGE_API_TOKEN')

    try:
        # Route Generate Image
        api_response = await api_instance.route_generate_image_verified_image_verified_get(prompt, negative_prompt, api_token, max_attempts=1)
        return api_response
    except Exception as e:
        print("Exception when calling DefaultApi->route_generate_image_image_get: %s\n" % e)

 
 
if __name__=="__main__":
    print(generate_image('The entire Cobalt Building of Machines is visible. Machines with intricate cogs and tubes, steampunk pipes, and colorful cobalt energy coursing through them on background of the bustling futuristic city with flying cars during the afternoon with warm lighting. nvinkpunk'))