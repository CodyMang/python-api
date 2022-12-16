import os
from dotenv import load_dotenv
import openai
# Load environment variables from the .env file
load_dotenv(".env")

# Get the value of the "SECRET_KEY" variable
openai.api_key = os.getenv("SECRET_KEY")
assert openai.api_key, "SECRET_KEY value should be in .env file"

def get_images_from_desc(sentence, n=1):
    if sentence:
        try:
            response = openai.Image.create(
                prompt=sentence,
                n=n,
                size="1024x1024",
                # size="1024x1024"
                response_format="b64_json"
                )
            return response
        except Exception as e:
            print(e)
            return None
    else:
        print("No input given")

from base64 import b64decode

if __name__ == '__main__':
    test_prompt = 'A penguin snowboarding down a mountain on a sunny snowy day'
    # print(dir(openai.Image))
    result = get_images_from_desc(test_prompt)
    res = result.to_dict()
    i=1
    for idx,file_content in enumerate(res['data'],start=1):
        file_name = f"file{idx}.png"
        with open(file_name, 'wb') as f:
            f.write(b64decode(file_content['b64_json']))
    # file_uuid = res['created']
    # new_file_name = f'{file_uuid}.png'
    # with open(new_file_name,'wb') as f:
    #     f.write(res['created'])
    # # for url in res['data']:
    #     print(url['url'])
    # openai.Image.list()