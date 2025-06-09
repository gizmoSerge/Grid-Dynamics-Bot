# import pyautogui
# import io
# import requests
import api_keys
from save_image import capture_screenshot
from openai import OpenAI
from time import sleep
# import openai

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

# if __name__ == "__main__":
#     # print("Press Enter to capture the screenshot and send to DeepSeek. (Press Ctrl+C to exit.)")
#     while True:
#         print("Press Enter to proceed.")
#         input()
#         send_to_deepseek()


def upload_image(file_path):
    """Upload a file to OpenAI and return its ID"""
    with open(file_path, "rb") as f:
        file = client.files.create(
            file=f,
            purpose="vision"
        )
    return file.id



# Initialize the OpenAI client
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key in environment variables
# openai.api_key = api_keys.openai_api_key

client = OpenAI(api_key=api_keys.openai_api_key)

def chat_with_assistant():

    # capture_screenshot()
    sleep(1)
    file_id = upload_image("screen.png")

    # Create a thread
    thread = client.beta.threads.create()
    
    # User input
    user_message = 'Proceed with the task.'
    
    # Add message to thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        # content=user_message
        content=[{"type": "text", "text": user_message},
            {"type": "image_file", "image_file": {"file_id": file_id}}]
    )
    
    # Create a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=api_keys.openai_assistant_key
        # assistant_id='asst_K6qGg5M7Bj8uaP7Z3ie8fvlk'
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
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                print(f"Assistant: {msg.content[0].text.value}")
    else:
        print("The run failed to complete")

if __name__ == "__main__":
    while True:
        print('Press to proceed')
        input()
        chat_with_assistant()