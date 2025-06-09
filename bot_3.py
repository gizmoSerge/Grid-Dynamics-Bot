import pyautogui
import io
# import requests
import api_keys
# from save_image import capture_screenshot
from openai import OpenAI
from time import sleep


def upload_image(screenshot):
    img_buffer = io.BytesIO()
    screenshot.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    file = AI_instance.files.create(
        file=("screenshot.png", img_buffer, "image/png"),
        purpose="vision"
    )
    return file.id

AI_instance = OpenAI(api_key=api_keys.openai_api_key)

def chat_with_assistant():

    # Take the screenshot for the specified region
    screen_region = (1020, 260, 830, 840)
    screenshot = pyautogui.screenshot(region=screen_region)
    file_id = upload_image(screenshot)

    sleep(1)

    # Create a thread
    thread = AI_instance.beta.threads.create()
    
    # User input
    user_message = 'Proceed with the task.'
    
    # Add message to thread
    AI_instance.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        # content=user_message
        content=[{"type": "text", "text": user_message},
            {"type": "image_file", "image_file": {"file_id": file_id}}]
    )
    
    # Create a run
    run = AI_instance.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=api_keys.grid_bot_3
    )
    
    # Wait for completion
    while run.status not in ["completed", "failed"]:
        sleep(1)
        run = AI_instance.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # Get responses
    if run.status == "completed":
        messages = AI_instance.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                print(f"Assistant: {msg.content[0].text.value}")
    else:
        print("The run failed to complete")

if __name__ == "__main__":
    while True:
        print('Press Enter to proceed...')
        input()
        chat_with_assistant()
