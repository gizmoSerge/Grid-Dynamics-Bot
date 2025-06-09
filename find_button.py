import pyautogui
import cv2
import numpy as np


def find_button_location(confidence=0.8):
    """
    Finds the location of the blue **Next** button in the most recent screenshot.

    *What changed?*  Instead of template‑matching the greyscale screenshot,
    we now detect the **colour** of the button:

    1.  Read the reference ``button.png`` and measure its dominant hue.
    2.  Threshold the screenshot to everything with a similar hue.
    3.  Take the largest blob that survives that threshold and return its
        centre.

    The signature and overall flow stay the same so the rest of your code
    doesn’t have to change.
    """
    try:
        # ------------------------------------------------------------------
        # 1️⃣  Read images (unchanged)
        # ------------------------------------------------------------------
        screen_img = cv2.imread(r"C:\code\grid_bot\screen.png")
        button_img = cv2.imread(r"C:\code\grid_bot\button.png")

        # if screen_img is None or button_img is None:
        #     print("Could not load screen.png or button.png – check paths.")
        #     return None

        # ------------------------------------------------------------------
        # 2️⃣  Work in HSV so we can isolate the button’s blue colour
        # ------------------------------------------------------------------
        screen_hsv = cv2.cvtColor(screen_img, cv2.COLOR_BGR2HSV)
        button_hsv = cv2.cvtColor(button_img, cv2.COLOR_BGR2HSV)

        # Keep only well‑saturated pixels from the reference and grab their hue
        b_mask = button_hsv[..., 1] > 60
        button_hues = button_hsv[..., 0][b_mask]
        if button_hues.size == 0:
            print("Button reference contains no saturated pixels.")
            return None

        dominant_hue = int(np.median(button_hues))

        # ±10° window around the dominant hue → blue range for the threshold
        lower_hue = max(0,   dominant_hue - 10)
        upper_hue = min(179, dominant_hue + 10)
        lower_bound = np.array([lower_hue,  60,  60])
        upper_bound = np.array([upper_hue, 255, 255])

        mask = cv2.inRange(screen_hsv, lower_bound, upper_bound)

        # Small morphology “close” to remove speckles / radio‑button rings
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # ------------------------------------------------------------------
        # 3️⃣  Find the biggest blue blob and return its centre
        # ------------------------------------------------------------------
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print("Button not found in the screenshot.")
            return None

        big_cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(big_cnt) < 9000:
            print("Largest blue area too small – probably not the button.")
            return None

        M = cv2.moments(big_cnt)
        if M["m00"] == 0:
            return None

        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        return (center_x, center_y)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# --------------------------------------------------------------------------
# Example usage (almost identical to your original block)
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Take a screenshot of the quiz area and save it exactly as before
    screen_region = (1020, 160, 830, 940)
    screenshot = pyautogui.screenshot(region=screen_region)
    screenshot.save("screen.png")

    button_center = find_button_location()

    if button_center:
        # Convert region‑relative to absolute screen coordinates for the click
        pyautogui.click(button_center[0] + 1020, button_center[1] + 160)
        print(
            f"Button center found at: X={button_center[0] + 1020}, "
            f"Y={button_center[1] + 160}"
        )
    else:
        print("Button not found.")
