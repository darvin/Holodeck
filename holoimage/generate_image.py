from transformers import pipeline
from PIL import Image
import torch
import numpy as np
from io import BytesIO
from diffusers import StableDiffusionPipeline
import torch
from verify_image import verify_image

async def generate_image_raw(prompt):
    return pipe(prompt).images[0]


 

def convert_image_to_png_bytes(image):
    output_image = Image.fromarray(np.uint8(image)).convert('RGB')

    byte_io = BytesIO()
    output_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    image_bytes = byte_io.getvalue()
    byte_io.close()
    output_image.close()
    return image_bytes


async def generate_image_verified(prompt, max_attempts):
    last_image = None
    for attempt in range(max_attempts):
        image = await generate_image_raw(prompt)
        is_good = await verify_image(image, prompt)
        if is_good:
            return convert_image_to_png_bytes(image)
        last_image = image
    if last_image:
        return convert_image_to_png_bytes(last_image)
    raise ValueError("Failed to generate a good image after all attempts")

async def generate_image(prompt):
    output = await generate_image_raw(prompt)
    return convert_image_to_png_bytes(output)

def init_generate_image():
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.safety_checker = lambda images, **kwargs: (images, [False] * len(images))
    pipe = pipe.to("cuda")
    return pipe


# model_id = "prompthero/openjourney-v4"
model_id = "Envvi/Inkpunk-Diffusion"
# model_id = "runwayml/stable-diffusion-v1-5"
pipe = init_generate_image()