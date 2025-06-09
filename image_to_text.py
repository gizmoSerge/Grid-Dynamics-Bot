from PIL import Image
import pytesseract

# Point to the Tesseract executable (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\smaye\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Windows example

# Open the image file
image_path = r"C:\code\grid_bot\screen.png"  # Replace with your image path
img = Image.open(image_path)

# Extract text using OCR
text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')

# Print the extracted text
print(text)

# print("Extracted Text:")
print(text)