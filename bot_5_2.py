import pyautogui
import base64
import api_keys
from time import sleep
from openai import OpenAI
from circle_detect import detect_circles
from find_button import find_button_location


client = OpenAI(api_key=api_keys.openai_api_key)

def encode_image():
    with open(r'C:\code\grid_bot\screen.png', "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat_with_assistant():
    sleep(2)
    screen_region = (970, 75, 930, 1080)
    screenshot = pyautogui.screenshot(region=screen_region)
    sleep(1)
    screenshot.save('screen.png')
    sleep(1)
    base64_screenshot = encode_image()
    sleep(1)
    circle_centers = detect_circles()
    
    # user_message = "Analyze the image and give the correct answer. Let's count the correct answers from bottom to top, from 1 to how many there are. Each possible answear has is in a gray box and has a circle on the left. I need you only to say the number of the correct answer, don't explain anything."
    user_message = """Analyze the image and give me the correct answer. Each possible answer is in a gray box and has a circle on the left. Give every possible correct answer a number, from the lowest on the image answer as number 1, the one above him number 2 and so on. 
I need you to give me the correct answer in the next format: {number of the answer}; {the text of the answer}
Respond only in this format, don't explain anything."""


    response = client.responses.create(
    # model="gpt-4.1",
    model = "chatgpt-4o-latest",
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
    # print(circle_centers)
    # print(circle_centers[int(response.output_text)-1])
    # print(f'X: {circle_centers[int(response.output_text)-1][0]}, Y: {circle_centers[int(response.output_text)-1][1]}')
    # if len(response.output_text) > 5:
    number = response.output_text.split(';')[0]
    try:
        x = circle_centers[int(number)-1][0] + 970
        y = circle_centers[int(number)-1][1] + 75
        pyautogui.click(x, y)
        sleep(1)

        button_center = find_button_location()
        # print(button_center)
        pyautogui.click(button_center[0] + 970, button_center[1] + 75)
        sleep(1)
    except Exception as e:
        print('Exception! Trying again.')
        # print(response.output_text)
        


if __name__ == "__main__":
    print('Sleep for 3 seconds...')
    sleep(3)
    try:
        while True:
            # print('Press Enter to proceed...')
            # input()
            chat_with_assistant()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

