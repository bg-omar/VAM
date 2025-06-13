from PIL import Image
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
    "Scan_20250611 (4).png",
    "Scan_20250611 (5).png",
    "Scan_20250611 (6).png"
]

def smart_crop_gray_background(image_path, brightness_threshold=42, border=5):
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

# Display results
# fig, axs = plt.subplots(1, len(final_crops), figsize=(16, 6))
# for ax, img in zip(axs, final_crops):
#     ax.imshow(img)
#     ax.axis("off")
# plt.tight_layout()



# Show actual output crops
fig, axs = plt.subplots(1, len(retested_crops), figsize=(16, 6))
for ax, img in zip(axs, retested_crops):
    ax.imshow(img)
    ax.axis("off")
plt.tight_layout()
plt.show()