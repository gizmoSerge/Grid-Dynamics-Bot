import cv2
import numpy as np

def detect_circles():
    # Read the input image
    image_path = r"C:\code\grid_bot\screen.png"
    output_path = r"C:\code\grid_bot\detected_circles.png"
    
    img = cv2.imread(image_path)
    # gray_blur = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray_blur = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(gray_blur, 
                              cv2.HOUGH_GRADIENT,
                              dp=1.2,           # Inverse ratio of accumulator resolution
                              minDist=20,     # Minimum distance between circles
                              param1=50,      # Upper threshold for Canny edge detector
                              param2=25,      # Threshold for center detection
                              minRadius=8,    # Minimum circle radius
                              maxRadius=20)    # Maximum circle radius (0 for unlimited)

    centers = []
    
    if circles is not None:
        # Convert coordinates and radius to integers
        circles = np.uint16(np.around(circles))
        
        for circle in circles[0, :]:
            # Get center coordinates (x, y)
            center = (circle[0], circle[1])
            centers.append(center)
            
            # Draw the outer circle
            cv2.circle(img, center, circle[2], (0, 255, 0), 2)
            # Draw the center point
            cv2.circle(img, center, 2, (0, 0, 255), 3)
        
        # Save the output image with detected circles
        cv2.imwrite(output_path, img)

    sorted_circles = []
    for i, (x, y) in enumerate(centers):
        if not sorted_circles:
            sorted_circles.append((x, y))
            for tx, ty in centers[i+1:]:
                if x-5 < tx < x+5:
                    sorted_circles.append((tx, ty))
        if len(sorted_circles) >= 3:
            break
        else:
            sorted_circles.clear()

    # for x, y in sorted_circles:
    #     print(x, y)
    sorted_circles.sort(key=lambda x: x[1])
    # for x, y in sorted_circles:
    #     print(x, y)
    return sorted_circles[::-1]

# Example usage
if __name__ == "__main__":
    
    circle_centers = detect_circles()
    
    print("Detected circle centers:")
    for i, center in enumerate(circle_centers, 1):
        print(f"Circle {i}: X={center[0]}, Y={center[1]}")