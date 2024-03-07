from openai import OpenAI
from django.core.files.base import ContentFile
import os
from dotenv import load_dotenv
from haiku_generator.seeds import get_seed_words
from .models import Haiku
import requests

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)


# TEMPERATURE is a measure of how random the output is.
# The higher the temperature, the more random the output.
TEMPERATURE = 0.7 
HAIKU_PROMPT_INSTRUCTIONS = "Write a haiku but do not always use strict 5 - 7 - 5 sylable structure. Poem should incorporate these items: "
IMAGE_PROMPT_INSTRUCTIONS = "Please create a prompt for DALL·E that is no longer than 800 characters. Extract visual imagery from this text: " 

def generate_haiku(instructions, seed_words, temperature=0.7):
    prompt = instructions + seed_words
    print("..generating haiku...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    print(response)
    haiku = response.choices[0].message.content.strip()
    return haiku

def create_image_prompt(instructions, haiku):
    print("...generating image prompt...")
    prompt = instructions + haiku
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # make sure to use the correct model name
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    image_prompt = response.choices[0].message.content.strip()
    return image_prompt

def generate_image(prompt):
    print("...generating image...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,  
        size="1024x1024"  
    )
    image_url = response.data[0].url
    return image_url

def extract_image_name(url):
    parts = url.split('/')
    
    # Iterate over each part to find the one with '.png'
    for part in parts:
        if '.png' in part:
            # Return the part of the string before '.png'
            return part.split('?')[0]
    return None  # Return None if '.png' is not found

def save_image_from_url(model_instance, image_url):
    print("...saving image...")
    response = requests.get(image_url)
    print(image_url)
    if response.status_code == 200:
        image_content = ContentFile(response.content)
        image_name = extract_image_name(image_url)
        print(image_name)
        model_instance.image.save(image_name, image_content)
      

def save_haiku_and_image(haiku, image_prompt, seed_words='', image_path=''):
    new_haiku = Haiku(
        text=haiku,
        alt_text=image_prompt,
        seed_words=seed_words,
    )
    save_image_from_url(new_haiku, image_path)
    return new_haiku

def generate_haiku_and_image():
    print('...kicking off process...')
    seed_words = get_seed_words()
    print("seed words: ", seed_words)
    haiku = generate_haiku(HAIKU_PROMPT_INSTRUCTIONS, seed_words, TEMPERATURE)
    print(haiku)
    image_prompt = create_image_prompt(IMAGE_PROMPT_INSTRUCTIONS, haiku)
    print("Image prompt: ", image_prompt)
    image_url = generate_image(image_prompt)
    print("Image url: ", image_url)
    saved_haiku = save_haiku_and_image(haiku, image_prompt, seed_words, image_url)

    return saved_haiku