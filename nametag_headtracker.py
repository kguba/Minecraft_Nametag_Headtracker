import cv2
import mediapipe as mp
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Initialize mediapipe face detection
mp_face_detection = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize time variables for FPS counter
pTime = 0
cTime = 0

# Define the floating label text
floating_text = "Konstantin"

# Load custom Minecraft font
font_path = os.path.join(os.path.dirname(__file__), 'minecraft_font.ttf')
font_size = 48  # Name tag font size
fps_font_size = 42  # Reduced from 64 to 42 for smaller FPS display

# Initialize position smoothing variables
last_y = None
last_x = None
smoothing_factor = 0.5  # Reduced from 0.8 to 0.5 for less delay
height_threshold = 0.1  # 10% threshold for height changes
base_height = None
moving_avg_y = []
max_avg_samples = 3  # Reduced from 10 to 3 for faster response

def get_text_size(text, font):
    # Create a dummy image to calculate text size
    dummy_img = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]  # width, height

def put_text_with_custom_font(img, text, position, font_size, color):
    # Convert the image to PIL format
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # Create a drawing object
    draw = ImageDraw.Draw(img_pil)
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    # Draw the text
    draw.text(position, text, font=font, fill=color)
    # Convert back to OpenCV format
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def smooth_position(current, last, smoothing):
    if last is None:
        return current
    return int(current * (1 - smoothing) + last * smoothing)

def get_adaptive_color(img, x, y, width, height):
    # Extract the region around the text
    roi = img[max(0, y-10):min(img.shape[0], y+height+10), 
              max(0, x-10):min(img.shape[1], x+width+10)]
    if roi.size == 0:
        return (255, 255, 255)  # Default to white if ROI is invalid
    
    # Calculate average brightness
    avg_color = np.mean(roi)
    
    # Return black for bright backgrounds, white for dark backgrounds
    return (0, 0, 0) if avg_color > 127 else (255, 255, 255)

while True:
    success, img = cap.read()
    
    # Convert the image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect faces
    results = face_detection.process(imgRGB)
    
    if results.detections:
        for detection in results.detections:
            # Get bounding box coordinates
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            
            # Calculate center position
            current_x = bbox[0] + bbox[2]//2
            current_y = bbox[1] - 200
            
            # Initialize base height if not set
            if base_height is None:
                base_height = current_y
                moving_avg_y = [current_y] * max_avg_samples
            
            # Update moving average for Y position
            moving_avg_y.pop(0)
            moving_avg_y.append(current_y)
            avg_y = sum(moving_avg_y) / len(moving_avg_y)
            
            # Check if height change is within threshold
            height_change = abs(avg_y - base_height) / base_height
            if height_change <= height_threshold:
                current_y = base_height
            else:
                base_height = avg_y  # Update base height for large changes
            
            # Apply position smoothing
            label_x = smooth_position(current_x, last_x, smoothing_factor)
            label_y = smooth_position(current_y, last_y, smoothing_factor)
            
            # Update last positions
            last_x = label_x
            last_y = label_y
            
            # Get text size using PIL
            font = ImageFont.truetype(font_path, font_size)
            text_width, text_height = get_text_size(floating_text, font)
            text_x = label_x - text_width//2  # Center text horizontally
            
            # Create overlay for semi-transparent background
            overlay = img.copy()
            
            # Draw background rectangle
            cv2.rectangle(overlay, 
                         (text_x - 10, label_y - text_height),
                         (text_x + text_width + 10, label_y + 25),
                         (45, 45, 45), -1)  # Dark gray color
            
            # Apply transparency
            alpha = 0.7  # Transparency factor (0 = fully transparent, 1 = fully opaque)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            
            # Draw floating text with custom font
            img = put_text_with_custom_font(
                img, 
                floating_text,
                (text_x, label_y - text_height),
                font_size,
                (255, 255, 255)  # White color
            )
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    # Prepare FPS text
    fps_text = f'FPS: {int(fps)}'
    fps_font = ImageFont.truetype(font_path, fps_font_size)
    fps_width, fps_height = get_text_size(fps_text, fps_font)
    
    # Get adaptive color for FPS text based on background
    fps_color = get_adaptive_color(img, 10, 10, fps_width, fps_height)
    
    # Draw FPS with Minecraft font and adaptive color
    img = put_text_with_custom_font(
        img,
        fps_text,
        (10, 10),
        fps_font_size,
        fps_color
    )
    
    # Display the image
    cv2.imshow('Face Detection', img)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
