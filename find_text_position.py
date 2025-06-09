# Import required packages
import cv2
import pytesseract
from Levenshtein import ratio as string_similarity
import re


# Example string to match against 
example_to_match = "to decide"  # User-provided example string
score_list = []

def find_closest_match(target, entries):
    # """Find the entry with highest similarity to target string"""
    best_match = None
    highest_score = 0
    
    for entry in entries:
        # score = string_similarity(target, entry['text'].replace('©', '').strip())
        score = string_similarity(target, re.sub(r'^[co©]+', '', entry['text'], flags=re.IGNORECASE).strip())
        # print(entry['text'].replace('©', '').strip())
        score_list.append((entry['text'], score))
        if score > highest_score:
            highest_score = score
            best_match = entry
    
    return best_match, highest_score

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\smaye\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # In case using colab after installing above modules

# Read image from which text needs to be extracted
img = cv2.imread("screen.png")

# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size. 
# Kernel size increases or decreases the area 
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect 
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_NONE)

# Initialize list to store text entries
text_entries = []

# Creating a copy of image
im2 = img.copy()

# A text file is created and flushed
# file = open("recognized.txt", "w+")
# file.write("")
# file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
    
    # Open the file in append mode
    # file = open("recognized.txt", "a")

    
    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
    
    cleaned_text = text.strip()
    # print(f"Text: {cleaned_text} | Position: (x={x}, y={y}, w={w}, h={h})")
    text_entries.append({
        'text': cleaned_text,
        'x': x,
        'y': y,
        'w': w,
        'h': h
    })

# Display matching results
if text_entries:
    best_match, score = find_closest_match(example_to_match, text_entries)
    if best_match:
        # for i in score_list:
        #     print(i)
        print(f"\nBest match to '{example_to_match}' ({score*100:.1f}% similar):")
        print(f"Text: {best_match['text']}")
        print(f"Position: (x={best_match['x']}, y={best_match['y']})")
        print(f"Dimensions: {best_match['w']}w x {best_match['h']}h")
    else:
        print("\nNo close matches found")
else:
    print("\nNo text blocks detected")

# This code is modified by Susobhan Akhuli
