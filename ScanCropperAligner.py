from PIL import Image
import numpy as np
import os
from fpdf import FPDF
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def edge_crop(image_path, padding=10):
    img = Image.open(image_path).convert("RGB")
    img_cv = np.array(img)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(img_gray, threshold1=50, threshold2=150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return img

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    x0 = max(x - padding, 0)
    y0 = max(y - padding, 0)
    x1 = min(x + w + padding, img.width)
    y1 = min(y + h + padding, img.height)

    return img.crop((x0, y0, x1, y1))

def smart_crop_gray_background(image_path, brightness_threshold=230, border=10):
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

def export_pdf(image_paths, output_pdf="notebook_cleaned.pdf"):
    """Export list of image paths to a single PDF after smart cropping."""
    pdf = FPDF(unit="pt")
    for i, path in enumerate(image_paths):
        cropped = smart_crop_gray_background(path)
        img_rgb = cropped.convert("RGB")
        temp_path = f"temp_crop_{i}.jpg"
        img_rgb.save(temp_path)
        pdf.add_page(format=[cropped.width, cropped.height])
        pdf.image(temp_path, 0, 0)
        os.remove(temp_path)
    pdf.output(output_pdf)
    print(f"✅ Exported to {output_pdf}")


def final_balanced_crop(image_path, final_width=1700, final_height=2400, v_threshold=240, density_thresh=10):
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

# Display results
fig, axs = plt.subplots(1, len(final_crops), figsize=(16, 6))
for ax, img in zip(axs, final_crops):
    ax.imshow(img)
    ax.axis("off")
plt.tight_layout()
plt.show()

# Example usage:
# image_list = ["Scan_20250611 (4).png", "Scan_20250611 (5).png", "Scan_20250611 (6).png"]
# export_pdf(image_list)
# Apply edge-based cropping to the same test images
edge_crops = [edge_crop(path) for path in retest_images]

# Show results
fig, axs = plt.subplots(1, len(edge_crops), figsize=(16, 6))
for ax, im in zip(axs, edge_crops):
    ax.imshow(im)
    ax.axis('off')
plt.tight_layout()
plt.show()