import pyautogui
from io import BytesIO
import base64
# import requests
import api_keys
from openai import OpenAI
from time import sleep


client = OpenAI(api_key=api_keys.openai_api_key)

def chat_with_assistant():

    # Take the screenshot for the specified region
    screen_region = (1020, 260, 830, 840)
    screenshot = pyautogui.screenshot(region=screen_region)
    # transform screenshot to base64

    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")
    base64_screenshot = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # base64_screenshot = base64.b64encode(screenshot.tobytes()).decode("utf-8")

    # sleep(1)

    # Create a thread
    # thread = client.beta.threads.create()
    
    # User input
    user_message = 'Proceed with the task.'
    
    # Add message to thread
    # client.beta.threads.messages.create(
    #     thread_id=thread.id,
    #     role="user",
    #     # content=user_message
    #     content=[{"type": "text", "text": user_message},
    #         {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_screenshot}", "detail": "high"}}]
    #         # {"type": "image_file", "image_file": {"file_id": file_id}}]
    # )
    
    thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{user_message}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_screenshot}",
                        "detail": "high",
                    }
                }
                ]
            }
        ]
    )

    # Create a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=api_keys.grid_bot_3
    )
    
    # Wait for completion
    while run.status not in ["completed", "failed"]:
        sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # Get responses
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(f"Assistant: {messages.data[0].content[0].text.value}")
    else:
        print("The run failed to complete")

if __name__ == "__main__":
    while True:
        print('Press Enter to proceed...')
        input()
        chat_with_assistant()
