import os
import sys
from rembg import remove
from PIL import Image
import cv2
import numpy as np

# Resolve path relative to script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    input_path = os.path.join(current_dir, "photo.jpg")

output_path = os.path.join(current_dir, "source-prepped.png")
temp_path = os.path.join(current_dir, "temp.png")

print(f"Opening photo: {input_path}")
if not os.path.exists(input_path):
    print(f"Error: photo not found at {input_path}")
    sys.exit(1)

with open(input_path, "rb") as i:
    input_data = i.read()

print("Removing background with rembg...")
output_data = remove(input_data)

with open(temp_path, "wb") as o:
    o.write(output_data)

# Open RGBA Image
img = Image.open(temp_path).convert("RGBA")

# Composite onto pure white background
background = Image.new("RGBA", img.size, (255, 255, 255, 255))
background.paste(img, mask=img)

rgb = np.array(background.convert("RGB"))

# Convert to grayscale
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# Standardize contrast: stretch to [0, 255]
min_val = np.min(gray)
max_val = np.max(gray)
if max_val > min_val:
    gray = ((gray - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Gamma correction to adjust middle gray contrast
# gamma < 1.0 makes shadows darker, gamma > 1.0 makes highlights brighter
gamma = 0.95
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
gray = cv2.LUT(gray, lookUpTable)

# Light smoothing to reduce ASCII noise
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# Save prepped image
cv2.imwrite(output_path, gray)
print(f"Prepped photo saved to: {output_path}")

# Clean up temp file
if os.path.exists(temp_path):
    os.remove(temp_path)