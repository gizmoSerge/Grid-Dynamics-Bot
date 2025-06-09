import pyautogui
import time

print("Press Ctrl+C to stop the program.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse Position: X={x}, Y={y}")
        # print(end='\r')
        time.sleep(1)  # Update every 0.1 seconds
except KeyboardInterrupt:
    print("\nProgram stopped by user.")