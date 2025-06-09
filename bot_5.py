import pyautogui
import base64
import api_keys
from openai import OpenAI


client = OpenAI(api_key=api_keys.openai_api_key)

def encode_image():
    with open(r'C:\Amdaris\grid_bot\screen.png', "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat_with_assistant():

    screen_region = (1020, 260, 830, 840)
    screenshot = pyautogui.screenshot(region=screen_region)

    screenshot.save('screen.png')

    base64_screenshot = encode_image()

    user_message = "Analyze the image and give the correct answer. I need you only to say what is the correct answer, don't explain anything."
    
    response = client.responses.create(
    model="gpt-4.1",
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

    print(response.output_text)


if __name__ == "__main__":
    try:
        while True:
            print('Press Enter to proceed...')
            input()
            chat_with_assistant()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

