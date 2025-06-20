from PIL import Image
import numpy as np
import cv2
import json

INPUT_FILE = "pi.jpeg"
OUTPUT_FILE = "pi_path_points.json"

# load image and convert to grayscale
image_path = f"images/{INPUT_FILE}"

image = Image.open(image_path).convert("L")

# convert to numpy, remove ligt parts (should be a line image)
image_np = np.array(image)
_, binary_image = cv2.threshold(image_np, 200, 255, cv2.THRESH_BINARY_INV)

# find contours
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# draw the contours for visual inspection
canvas = np.ones_like(image_np) * 255
cv2.drawContours(canvas, contours, -1, (0), 1)

# Display image with contours using PIL
contour_image = Image.fromarray(canvas)
contour_image.show()

# keep only largest contour
largest_contour = max(contours, key=cv2.contourArea)
path_points = [(int(point[0][0]), int(point[0][1])) for point in largest_contour]

output_path = f"paths/{OUTPUT_FILE}"

# Save the path points as JSON
with open(output_path, "w") as f:
    json.dump({"path_points": path_points}, f, indent=2)
