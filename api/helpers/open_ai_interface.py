import os
from dotenv import load_dotenv
import openai
# Load environment variables from the .env file
load_dotenv(".env")

# Get the value of the "SECRET_KEY" variable
openai.api_key = os.getenv("SECRET_KEY")


def get_images_from_desc(sentence, n=4):
    if sentence:
        try:
            response = openai.Image.create(
                prompt=sentence,
                n=n,
                size="1024x1024"
                )
            return response
        except Exception as e:
            print(e)
            return None
    else:
        print("No input given")

if __name__ == '__main__':
    test_prompt = 'A dog sleeping next to a christmas tree'
    # print(dir(openai.Image))
    result = get_images_from_desc(test_prompt)
    res = result.to_dict()
    for url in res['data']:
        print(url['url'])
    # openai.Image.list()