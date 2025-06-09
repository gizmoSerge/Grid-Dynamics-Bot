import pyautogui
import base64
import api_keys
from time import sleep
from openai import OpenAI


def encode_image():
    with open(r'C:\code\grid_bot\screen.png', "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def take_screenshot():
    screen_region = (970, 75, 930, 1080)  
    screenshot = pyautogui.screenshot(region=screen_region)
    screenshot.save('screen.png')

def ai_chat():
    base64_screenshot = encode_image()
    user_message = """Analyze the image and give me only the correct answer. The answer must be written exactly the same as in the image. No explanation needed, just the correct answer."""

    response = client.responses.create(
    model="gpt-4.1",
    # model = "chatgpt-4o-latest",
    input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": f"{user_message}" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_screenshot}",
                        "detail": "high"
                    },
                ],
            }
        ],
    )
    return response.output_text

def main():
    sleep(5)
    take_screenshot()
    ai_response = ai_chat()
    print(f'-- {ai_response}')

if __name__ == "__main__":
    client = OpenAI(api_key=api_keys.openai_api_key)
    print('Sleep for 3 seconds...')
    sleep(3)
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
