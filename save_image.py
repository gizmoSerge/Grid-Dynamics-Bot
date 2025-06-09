import pyautogui

def capture_screenshot(left = 1020, top = 100, width = 830, height = 1000):

    # Fixed region variables: (left, top, width, height)
    # screen_region = (642, 445, 635, 340)  # Update these values as needed
    screen_region = (left,top, width, height)

    # Take the screenshot for the specified region
    screenshot = pyautogui.screenshot(region=screen_region)

    # Save the screenshot to a file
    screenshot.save(r'C:\Amdaris\grid_bot\screen\screen.png')
    print("Screenshot saved as screen.png")
    # return screenshot


if __name__ == "__main__":
    capture_screenshot()