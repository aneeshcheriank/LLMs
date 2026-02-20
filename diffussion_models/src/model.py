import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from src import download_image
from diffussion_models.config import 

device = "cuda" if torch.cuda.is_available() else "cpu"

def image_generator(image, prompt):
  model_id = MODEL_NAME
  pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
  pipe.to(device)
  pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
  
  image = download_image(image)
  images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images

  return images[0]