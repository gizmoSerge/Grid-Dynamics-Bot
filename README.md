# Grid Dynamics Test Bot

This repository contains scripts designed to automate solving the entry test used by Grid Dynamics. The main goal of the app is to capture the on-screen question, send it to an AI model for analysis, and automatically select the correct answer. The process involves taking a screenshot of the test interface, using OCR to detect text, and clicking on the detected answer.

The automation relies on several Python libraries:

- **pyautogui** for interacting with the screen and simulating mouse clicks.
- **pytesseract** and **OpenCV** for image processing and text recognition.
- **OpenAI** for leveraging a language model to interpret screenshots and produce the correct answer.

Running the scripts continuously monitors the test interface and clicks the detected correct answer, helping to pass the entry test.
