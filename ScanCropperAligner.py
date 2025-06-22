from PIL import Image, ImageOps
import os
from fpdf import FPDF
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

retest_images = [
    "C:\\Users\\mr\\Pictures\\Scans\\2012-NoteBook\\Scan_20250611 (1).png",
    "C:\\Users\\mr\\Pictures\\Scans\\2012-NoteBook\\Scan_20250611 (2).png",
    "C:\\Users\\mr\\Pictures\\Scans\\2012-NoteBook\\Scan_20250611 (3).png"
]

# Function to crop the image by detecting content
def crop_to_content(image_path, border=10):
    image = Image.open(image_path).convert("L")
    image_inverted = ImageOps.invert(image)
    bbox = image_inverted.getbbox()
    if bbox:
        cropped_image = image.crop((
            max(bbox[0] - border, 0),
            max(bbox[1] - border, 0),
            min(bbox[2] + border, image.width),
            min(bbox[3] + border, image.height)
        ))
        return cropped_image
    return image

# Process and save cropped images
cropped_images = []
for path in retest_images:
    cropped = crop_to_content(path)
    cropped_images.append(cropped)

# # Display cropped images for verification ---------------------------------grey
# fig, axs = plt.subplots(1, len(cropped_images), figsize=(16, 8))
# for ax, img in zip(axs, cropped_images):
#     ax.imshow(img, cmap='gray')
#     ax.axis('off')
# plt.tight_layout()

from PIL import Image



# Function to crop based on tight content but centered horizontally
def center_crop(image_path, border=10):
    color_img = Image.open(image_path)
    gray_img = color_img.convert("L")
    inverted = ImageOps.invert(gray_img)
    bbox = inverted.getbbox()

    if bbox:
        # Crop tightly vertically, but keep horizontal center
        content_width = bbox[2] - bbox[0]
        full_width = color_img.width
        center_x = full_width // 2
        half_crop_width = max(content_width // 2 + border, 1)

        left = max(center_x - half_crop_width, 0)
        right = min(center_x + half_crop_width, full_width)
        top = max(bbox[1] - border, 0)
        bottom = min(bbox[3] + border, color_img.height)

        centered_crop = color_img.crop((left, top, right, bottom))
        return centered_crop

    return color_img

# Apply centered cropping
centered_crops = [center_crop(path) for path in retest_images[-2:]]

# Display for verification
fig, axs = plt.subplots(1, len(centered_crops), figsize=(12, 6))
for ax, img in zip(axs, centered_crops):
    ax.imshow(img)
    ax.axis('off')
plt.tight_layout()


centered_crop_batch = [center_crop(path) for path in retest_images]

# Display results to verify correct alignment
fig, axs = plt.subplots(1, len(centered_crop_batch), figsize=(16, 6))
for ax, img in zip(axs, centered_crop_batch):
    ax.imshow(img)
    ax.axis('off')
plt.tight_layout()


def smart_crop_gray_background(image_path, brightness_threshold=25, border=50):
    """Crop image by removing light-gray/gradient background, keeping main notebook content."""
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    gray = np.mean(img_np, axis=2)

    # Create mask for pixels below brightness threshold
    content_mask = gray < brightness_threshold

    # Find bounding box of content
    coords = np.argwhere(content_mask)
    if coords.size == 0:
        return img  # fallback to original if no content found

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    # Apply padding
    x0 = max(x0 - border, 0)
    y0 = max(y0 - border, 0)
    x1 = min(x1 + border, img.width)
    y1 = min(y1 + border, img.height)

    return img.crop((x0, y0, x1, y1))


def final_balanced_crop(image_path, final_width=1800, final_height=1400, v_threshold=100, density_thresh=10):
    """
    Refined notebook crop:
    - Crops to fixed width & height
    - Horizontally centers on the spine
    - Vertically centers around detected content
    """
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    gray = np.mean(img_np, axis=2)

    # Mask content
    content_mask = gray < v_threshold

    # Horizontal (spine) center
    col_sum = content_mask.sum(axis=0)
    col_indices = np.where(col_sum > density_thresh)[0]
    if col_indices.size == 0:
        col_center = img.width // 2
    else:
        col_center = (col_indices[0] + col_indices[-1]) // 2

    # Vertical center from content
    row_sum = content_mask.sum(axis=1)
    row_indices = np.where(row_sum > density_thresh)[0]
    if row_indices.size == 0:
        row_center = img.height // 2
    else:
        row_center = (row_indices[0] + row_indices[-1]) // 2

    # Final crop box (fixed size, centered)
    x0 = max(col_center - final_width // 2, 0)
    y0 = max(row_center - final_height // 2, 0)
    x1 = min(col_center + final_width // 2, img.width)
    y1 = min(row_center + final_height // 2, img.height)

    return img.crop((x0, y0, x1, y1))

# Apply final balanced crop
final_crops = [final_balanced_crop(path) for path in retest_images]
# Apply crop again
retested_crops = [smart_crop_gray_background(path) for path in retest_images]

fig, axs = plt.subplots(1, len(final_crops), figsize=(16, 6))
for ax, img in zip(axs, final_crops):
    ax.imshow(img)
    ax.axis("off")
plt.tight_layout()

def fixed_width_center_crop(image_path, target_width=1600, vertical_border=10):
    """
    Centered crop with fixed width around the detected page center.
    Crops vertically to content and horizontally to a fixed width around the center.
    """
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    gray = np.mean(img_np, axis=2)

    # Threshold to find dark (content) regions
    content_mask = gray < 240
    row_density = content_mask.sum(axis=1) / content_mask.shape[1]
    valid_rows = np.where(row_density > 0.01)[0]

    if valid_rows.size == 0:
        return img  # fallback if no content

    y0, y1 = valid_rows[0], valid_rows[-1] + 1
    y0 = max(y0 - vertical_border, 0)
    y1 = min(y1 + vertical_border, img_np.shape[0])

    # Center X
    col_density = content_mask.sum(axis=0)
    col_center = int(np.mean(np.where(col_density > 10)))  # rough content center

    # Fixed width around center
    half_width = target_width // 2
    x0 = max(col_center - half_width, 0)
    x1 = min(col_center + half_width, img.width)

    return img.crop((x0, y0, x1, y1))


# Show actual output crops
fig, axs = plt.subplots(1, len(retested_crops), figsize=(16, 6))
for ax, img in zip(axs, retested_crops):
    ax.imshow(img)
    ax.axis("off")
plt.tight_layout()


# Test with fixed-width center crop
center_fixed_crops = [fixed_width_center_crop(path) for path in retest_images]

# Display results
fig, axs = plt.subplots(1, len(center_fixed_crops), figsize=(16, 6))
for ax, img in zip(axs, center_fixed_crops):
    ax.imshow(img)
    ax.axis('off')
plt.tight_layout()

plt.show()
