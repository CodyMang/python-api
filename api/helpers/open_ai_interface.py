import requests
import os
from dotenv import load_dotenv
import openai
# Load environment variables from the .env file
load_dotenv(".env")

# Get the value of the "SECRET_KEY" variable
openai.api_key = os.getenv("SECRET_KEY")

# OPEN_AI_API = 'https://api.openai.com/v1/images/generations'

def ensure_valid_input(input_desc):
    if not input_desc:
        return False
    if len(input_desc.split(' ')) < 5:
        return False

def get_images_from_desc(sentence, n=4):
    if sentence:
        response = openai.Image.create(
            prompt="A cute baby sea otter",
            n=2,
            size="1024x1024"
            )
        
        images = openai.Image.to_dict()

            # Print the image URLs
        for image in images.items():
            print(image)


if __name__ == '__main__':
    test_prompt = 'A sea otter that has found a shiny new rock'
    # print(dir(openai.Image))
    get_images_from_desc(test_prompt)
    # openai.Image.list()