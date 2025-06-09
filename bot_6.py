import pyautogui
import base64
import os
import cv2
import pytesseract
from time import sleep
from openai import OpenAI
from find_button import find_button_location
from Levenshtein import ratio as string_similarity
import re


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

##############################################################################

def find_closest_match(target, entries): # function not used
    best_match = None
    highest_score = 0
    
    for entry in entries:
        score = string_similarity(target, re.sub(r'^[co©]+', '', entry['text'], flags=re.IGNORECASE).strip())
        if score > highest_score:
            highest_score = score
            best_match = entry
    return best_match, highest_score

def find_top_two_matches(target, entries):
    top_match = None
    top_match_score = 0
    second_match = None
    second_match_score = 0
    for entry in entries:
        processed_text = re.sub(r'^[co©]+', '', entry['text'], flags=re.IGNORECASE).strip()
        score = string_similarity(target, processed_text)
        if score > top_match_score:
            top_match, second_match = entry, top_match
            top_match_score, second_match_score = score, top_match_score
        elif score > second_match_score:
            second_match = entry
            second_match_score = score
    # print(f'Top: {top_match['text']} - {top_match_score}')
    # print(f'Second: {second_match['text']} - {second_match_score}')
    return ((top_match, top_match_score), (second_match, second_match_score))

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    return cv2.dilate(thresh, kernel, iterations=1)

def find_text_contours(dilated_image):
    return cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

def extract_text_entries(contours, base_image):
    text_entries = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = base_image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cropped).strip()
        text_entries.append({'text': text, 'x': x, 'y': y})
    return text_entries

def get_text_coordinates(text):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\smaye\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    dilated = preprocess_image("screen.png")
    contours = find_text_contours(dilated)
    text_entries = extract_text_entries(contours, cv2.imread("screen.png"))
    
    if text_entries:
        top_match, second_match = find_top_two_matches(text, text_entries)
        if top_match[1] - second_match[1] > 0.1 and top_match[1] > 0.7:
            # best_match = top_matches[0]
            # # print(f"({best_match['x']}, {best_match['y']})")
            # return (best_match['x'], best_match['y'])
            return (top_match[0]['x'], top_match[0]['y'])
        else:
            return '------------------ Choose the correct answer manually... Waiting for 5 seconds. ------------------'
        
##############################################################################

def main():
    sleep(2)
    take_screenshot()
    ai_response = ai_chat()
    print(f'-- {ai_response}')
    response_coordinates = get_text_coordinates(ai_response)
    # print(response_coordinates)
    try:
        if isinstance(response_coordinates, str):
            print(response_coordinates)
            sleep(5)
        else:
            x = response_coordinates[0] + 970 + 20
            y = response_coordinates[1] + 75 + 10
            pyautogui.click(x, y)
            sleep(1)

        button_center = find_button_location()
        pyautogui.click(button_center[0] + 970, button_center[1] + 75)
    except Exception as e:
        print('Exception! Trying again.')

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    print('Sleep for 3 seconds...')
    sleep(3)
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
