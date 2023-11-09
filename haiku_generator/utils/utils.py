from openai import OpenAI
import os
from dotenv import load_dotenv
from seeds import get_seed_words
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
    print("Generating haiku...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
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

def generate_haiku_and_image():
    seed_words = get_seed_words()
    haiku = generate_haiku(HAIKU_PROMPT_INSTRUCTIONS, seed_words, TEMPERATURE)
    image_prompt = create_image_prompt(IMAGE_PROMPT_INSTRUCTIONS, haiku)
    image_url = generate_image(image_prompt)
    return haiku, image_prompt, image_url

print(generate_haiku_and_image())