import torch
from torch import autocast
from diffusers.models import AutoencoderKL
from diffusers import StableDiffusionPipeline
from IPython.display import Image
from numpy import UFUNC_BUFSIZE_DEFAULT
import uuid
import runpod

default_prompt = "A pitbull drinking a red slushy while wearing shades"

def disableSafetyChecker(images, **kwargs): 
	return images, False

def imageGenerator(job):   

    job_input = job["input"]
    the_number = job_input["number"]

    # if not isinstance(the_number, int):
    #     return {"error": "Silly human, you need to pass an integer."}

    # if the_number % 2 == 0:
    #     return True
    
    run()
    
    return "A image was generated"

def setUUID(unique_id):
  uniq = unique_id

def getSeed(seed):
  return this.seed

def setSeed(prompt, seed):
  if seed != None:
    return f"{prompt} --seed {seed}"
  else:
    print("No seed detected: defaulting to prompt")
    return prompt

def setPrompt(prompt = None, seed=None):
  if prompt == None:
    demo_prompt = default_prompt
    promptWithMidjourneyStyle = f"{demo_prompt}"
    return promptWithMidjourneyStyle
  
  promptWithMidjourneyStyle = f"{prompt}"
  return promptWithMidjourneyStyle

def writeImagePromptFile(prompt, unique_id):
  imagePromptFile = open(f"{unique_id}-imagePromptFile.txt", "a")
  imagePromptFile.write(f"{prompt}")
  imagePromptFile.close()

def saveImage(imageGenerated, uuid):
  # Uploading image to Google Drive using uuid
  imageGenerated.save(f"{uuid}.png")

def printImage():
  print(f"The image was generated using unique_id: {uniq} and placed in '.' ")
  Image(filename=f'{uniq}.png')

def printImage(unique_id):
    print(f"The image was generated using unique_id: {unique_id} and placed in '.' ")
    Image(filename=f'{unique_id}.png')

def runStableDiffusionPipeline(prompt=default_prompt, unique_id = uniq, num_inference_steps = 30, width = 512, height = 512 , guidance_scale = 7 , negative_prompt=None, seed=None):
  print("Starting Stable Diffusion Pipeline...")
  print(f"Generated UUID for image generation {unique_id}")
  with autocast("cuda"):
    # Height and Width must be divisible by 8
    # Generates one image
    print(f"Prompt is: {prompt}, num_inference_steps: {num_inference_steps}")
    image = pipe(prompt=prompt, num_inference_steps=num_inference_steps, width=width, height=height, guidance_scale=guidance_scale, negative_prompt=negative_prompt).images[0]
  print("Saving image to current directory")
  saveImage(image, unique_id)
  print(f"Saving complete!...image uuid is: {unique_id}")
  print(f"Writing image prompt file to current directory")
  writeImagePromptFile(prompt, unique_id)
  print(f"Writing image prompt file to Google Drive completed!..")

def runTxt2ImageStableDiffusionPL(prompt = None, num_inference_steps = None, width = None, height = None, guidance_scale = None, negative_prompt = None, seed = None):

  # generate uuid
  uniq = uuid.uuid1()
  print(f"UUID is: {uniq}")

  # Setting UUID
  setUUID(uniq)

  # Determine if prompt is provided, if not then default prompt will be used
  if prompt == None:
    print(f"Please provide a prompt, default prompt will be: '{default_prompt}'")

  # Check to see if seed if provided
  if seed != None:
    print(f"Applying seed to end of prompt: {seed}")
    prompt = setPrompt(prompt, seed)
    print(f"full prompt is: {prompt}")
  else:
    prompt = setPrompt(prompt)
    print(f"No seed found: prompt will be: {prompt}")

  runStableDiffusionPipeline(prompt=prompt, unique_id = uniq, num_inference_steps=num_inference_steps, width=width, height=height, negative_prompt=negative_prompt, seed=seed)

def run():
    runTxt2ImageStableDiffusionPL(
        #Prompting
        prompt="an abandoned wasteland, dark, grim, full of greys and blacks, the depths of a portal to the underworld through the cracks in the found. skulls and bones across a valley of ancient relics of the past voodoo zombie land of misery. voodoo coloring and symbols",
        #Height
        height=512,
        #Negative Prompt
        negative_prompt="(deformed, distorted, disfigured:1.3), poorly drawn, watermark, watermarked, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands:1.4), (mutated fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, \
              mancanvas frame, cartoon, uneven skeleton, big skeleton, 3d, ((disfigured)), ((bad art)), ((deformed)),((extra limbs)),((close up)),((b&w)), blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, video game, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render, (knees), (full body), (((nsfw)))",
        #Guidance Scale
        guidance_scale=7.5,
        # Num Inference Steps
        num_inference_steps=50
    )

pipe = StableDiffusionPipeline.from_pretrained("stablediffusionapi/deliberate-v2")
pipe = pipe.to("cuda")
pipe.safety_checker = disableSafetyChecker


runpod.serverless.start({"handler": imageGenerator})