import os, cv2, numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog

class SpineAlignedCropper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notebook Cropper (Spine-Aligned)")
        self.geometry("900x720")

        self.paths = []
        self.ref_box = None
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self.start_box)
        self.canvas.bind("<B1-Motion>", self.update_box)
        self.canvas.bind("<ButtonRelease-1>", self.finish_box)

        btnf = tk.Frame(self); btnf.pack()
        ttk.Button(btnf, text="Load Folder", command=self.load_folder).pack(side="left", padx=5)
        ttk.Button(btnf, text="Test One", command=self.test_one).pack(side="left", padx=5)
        ttk.Button(btnf, text="Crop All", command=self.crop_all).pack(side="left", padx=5)
        self.status = tk.Label(self, text="Draw crop box on first image")
        self.status.pack()

        self._box_start = None

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder: return
        exts = ('.png','.jpg','.jpeg','.tif','.tiff','.bmp')
        self.paths = sorted([os.path.join(folder,f) for f in os.listdir(folder) if f.lower().endswith(exts)])
        if not self.paths:
            self.status.config(text="No images found")
            return
        self.show_image(self.paths[0])
        self.status.config(text="Draw crop box and test/crop")

    def show_image(self, path):
        self.img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        self.h, self.w = self.img.shape[:2]
        self.tkimg = ImageTk.PhotoImage(Image.fromarray(self.img).resize((800,600)))
        self.canvas.delete("all")
        self.canvas.create_image(0,0,anchor="nw",image=self.tkimg)

    def start_box(self, e):
        self._box_start = (e.x, e.y)
        self.canvas.delete("box")

    def update_box(self, e):
        x0, y0 = self._box_start
        self.canvas.delete("box")
        self.canvas.create_rectangle(x0,y0,e.x,e.y, outline="red",width=2, tag="box")

    def finish_box(self, e):
        x0, y0 = self._box_start
        x1, y1 = e.x, e.y
        fx, fy = self.w/800, self.h/600
        self.ref_box = (int(x0*fx), int(y0*fy), int(x1*fx), int(y1*fy))
        self.status.config(text=f"Crop box: {self.ref_box}")

    def deskew_and_crop(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=100, maxLineGap=20)

        h, w = gray.shape
        center_x = w // 2
        vs = []

        if lines is not None:
            for line in lines:
                try:
                    x1, y1, x2, y2 = line[0] if isinstance(line[0], (list, tuple, np.ndarray)) else line
                    if abs(x1 - x2) < 20:  # almost vertical
                        line_x = (x1 + x2) // 2
                        if abs(line_x - center_x) < w * 0.2:  # near center
                            length = np.hypot(x2 - x1, y2 - y1)
                            if length > h * 0.6:  # long line
                                vs.append((x1, y1, x2, y2))
                except:
                    continue

        if not vs:
            print("No spine lines found. Skipping rotation.")
            return img

        angles = [np.degrees(np.arctan2(y2 - y1, x2 - x1)) for x1, y1, x2, y2 in vs]
        angle = np.median(angles)
        print(f"Estimated deskew angle: {angle:.2f}°")

        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
        return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR)

    def test_one(self):
        if not self.ref_box or not self.paths:
            self.status.config(text="Draw crop box first!")
            return
        img = cv2.imread(self.paths[0])
        desk = self.deskew_and_crop(img)
        x0, y0, x1, y1 = self.ref_box
        crop = desk[y0:y1, x0:x1]
        Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)).show()
        self.status.config(text="Previewed first crop ✅")

    def crop_all(self):
        if not self.ref_box or not self.paths:
            self.status.config(text="Draw crop box first!")
            return
        x0, y0, x1, y1 = self.ref_box
        outdir = os.path.join(os.path.dirname(self.paths[0]), "cropped_spine")
        os.makedirs(outdir, exist_ok=True)

        for path in self.paths:
            img = cv2.imread(path)
            desk = self.deskew_and_crop(img)
            crop = desk[y0:y1, x0:x1]
            out_path = os.path.join(outdir, os.path.basename(path))
            cv2.imwrite(out_path, crop)

        self.status.config(text=f"Cropped {len(self.paths)} images to {outdir} ✅")

SpineAlignedCropper().mainloop()
