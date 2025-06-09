# import pyautogui
# import io
# import requests
from api_keys import deepseek_api_key as api_key
from save_image import capture_screenshot
from openai import OpenAI

def send_to_deepseek():
    
    capture_screenshot()
    
    image_link = "https://drive.google.com/uc?export=view&id=1BGGlN7T_dcERNjYAPc68-oNGTZSYwlh6"

    message = (f"""analyze the image in the link ({image_link}) and give the correct answer. 
               let's consider the top answer is number 1, I need you to give only the number of the correct answer.""")
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": message},
        ],
        stream=False
    )

    print(response.choices[0].message.content) 

if __name__ == "__main__":
    # print("Press Enter to capture the screenshot and send to DeepSeek. (Press Ctrl+C to exit.)")
    while True:
        print("Press Enter to proceed.")
        input()
        send_to_deepseek()
