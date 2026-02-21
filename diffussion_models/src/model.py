import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from src.image_process import download_image
from config import MODEL_NAME

def device():
  if torch.cuda.is_available():
    return torch.device("cuda")
  elif torch.backends.mps.is_available():
    return torch.device("mps")
  else:
    return torch.device("cpu")

def image_generator(image, prompt):
  model_id = MODEL_NAME
  pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
  pipe.to(device())
  pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
  
  image = download_image(image)
  images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images

  return images[0]