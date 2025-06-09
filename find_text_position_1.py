import cv2
import pytesseract
from Levenshtein import ratio as string_similarity
import re

def find_closest_match(target, entries):
    best_match = None
    highest_score = 0
    
    for entry in entries:
        score = string_similarity(target, re.sub(r'^[co©]+', '', entry['text'], flags=re.IGNORECASE).strip())
        if score > highest_score:
            highest_score = score
            best_match = entry
    return best_match, highest_score

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

def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\smaye\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    dilated = preprocess_image("screen.png")
    contours = find_text_contours(dilated)
    text_entries = extract_text_entries(contours, cv2.imread("screen.png"))
    
    if text_entries:
        best_match, score = find_closest_match("to decide", text_entries)
        if best_match:
            # print(f"({best_match['x']}, {best_match['y']})")
            return (best_match['x'], best_match['y'])


if __name__ == "__main__":
    main()
