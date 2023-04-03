from diffusers import StableDiffusionPipeline
import torch

model_id = "Envvi/Inkpunk-Diffusion"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.safety_checker = lambda images, **kwargs: (images, [False] * len(images))
pipe = pipe.to("cuda")

style = "vinkpunk"
def generate_image(prompt):
    if style not in prompt.lower():
        prompt += f". n{style}"
    return pipe(prompt).images[0]
 
 
if __name__=="__main__":
    print(generate_image('The entire Cobalt Building of Machines is visible. Machines with intricate cogs and tubes, steampunk pipes, and colorful cobalt energy coursing through them on background of the bustling futuristic city with flying cars during the afternoon with warm lighting. nvinkpunk'))