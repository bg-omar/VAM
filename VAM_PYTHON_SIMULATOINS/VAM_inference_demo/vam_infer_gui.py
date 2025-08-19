# -*- coding: utf-8 -*-
from __future__ import annotations
import os, sys, json, threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

APP_OUT_DEMO = "out_plots"
APP_OUT_CSV  = "out_plots_csv"

class VAMGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VAM Inference GUI")
        self.geometry("820x560")
        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True)

        # --- Tab 1: synthetic demo ---
        self.tab_demo = ttk.Frame(nb); nb.add(self.tab_demo, text="Synthetic demo")
        self._build_demo(self.tab_demo)

        # --- Tab 2: fit from CSV ---
        self.tab_csv = ttk.Frame(nb); nb.add(self.tab_csv, text="Fit from CSV")
        self._build_csv(self.tab_csv)

    # ------------ DEMO TAB ------------
    def _build_demo(self, parent):
        top = ttk.Frame(parent, padding=10); top.pack(fill="x")
        ttk.Label(top, text="Run synthetic τ(r) and g(r) demo; outputs to 'out_plots/'.").pack(anchor="w")
        ttk.Button(top, text="Run synthetic demo", command=self.run_demo_threaded, width=28).pack(pady=6, anchor="w")
        self.status_demo = tk.StringVar(value="Ready.")
        ttk.Label(parent, textvariable=self.status_demo).pack(anchor="w", padx=10)
        self.log_demo = tk.Text(parent, height=18, wrap="word"); self.log_demo.pack(fill="both", expand=True, padx=10, pady=6)

    def run_demo_threaded(self):
        threading.Thread(target=self._run_demo, daemon=True).start()

    def _run_demo(self):
        try:
            self.status_demo.set("Running...")
            here = os.path.dirname(os.path.abspath(__file__))
            out = subprocess.run([sys.executable, "demo_vam_inference.py"], cwd=here, capture_output=True, text=True)
            self.log_demo.insert("end", out.stdout + "\n" + out.stderr + "\n"); self.log_demo.see("end")
            if out.returncode == 0:
                self.status_demo.set(f"Done. See '{APP_OUT_DEMO}'.")
            else:
                self.status_demo.set("Failed. See log.")
        except Exception as e:
            self.status_demo.set("Error."); messagebox.showerror("Error", str(e))

    # ------------ CSV TAB ------------
    def _build_csv(self, parent):
        frm = ttk.Frame(parent, padding=10); frm.pack(fill="x")

        # tau(r)
        row1 = ttk.Frame(frm); row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="τ(r) CSV:").pack(side="left")
        self.tau_path = tk.StringVar(value="")
        ttk.Entry(row1, textvariable=self.tau_path, width=70).pack(side="left", padx=6)
        ttk.Button(row1, text="Browse", command=lambda: self._browse(self.tau_path)).pack(side="left")

        # g(r)
        row2 = ttk.Frame(frm); row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="g(r) CSV:").pack(side="left")
        self.g_path = tk.StringVar(value="")
        ttk.Entry(row2, textvariable=self.g_path, width=70).pack(side="left", padx=6)
        ttk.Button(row2, text="Browse", command=lambda: self._browse(self.g_path)).pack(side="left")

        # units / columns
        row3 = ttk.Frame(frm); row3.pack(fill="x", pady=4)
        ttk.Label(row3, text="r-units:").pack(side="left")
        self.r_units = tk.StringVar(value="m")
        ttk.Combobox(row3, textvariable=self.r_units, values=["m","mm","um","nm"], width=6).pack(side="left", padx=6)

        ttk.Button(frm, text="Run fit", command=self.run_csv_threaded, width=20).pack(anchor="w", pady=8)

        self.status_csv = tk.StringVar(value="Ready.")
        ttk.Label(parent, textvariable=self.status_csv).pack(anchor="w", padx=10)
        self.log_csv = tk.Text(parent, height=18, wrap="word"); self.log_csv.pack(fill="both", expand=True, padx=10, pady=6)
        ttk.Label(parent, text=f"Outputs: '{APP_OUT_CSV}'").pack(anchor="w", padx=10, pady=4)

    def _browse(self, var: tk.StringVar):
        p = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV/TSV","*.csv;*.tsv;*.txt"), ("All files","*.*")])
        if p: var.set(p)

    def run_csv_threaded(self):
        threading.Thread(target=self._run_csv, daemon=True).start()

    def _run_csv(self):
        try:
            self.status_csv.set("Running...")
            here = os.path.dirname(os.path.abspath(__file__))
            args = [sys.executable, "fit_from_csv.py", "--outdir", APP_OUT_CSV, "--r-units", self.r_units.get()]
            if self.tau_path.get(): args += ["--tau", self.tau_path.get()]
            if self.g_path.get():   args += ["--g", self.g_path.get()]
            if not self.tau_path.get() and not self.g_path.get():
                messagebox.showwarning("Missing input", "Select at least one CSV (τ or g)."); self.status_csv.set("Ready."); return
            out = subprocess.run(args, cwd=here, capture_output=True, text=True)
            self.log_csv.insert("end", " ".join(args) + "\n" + out.stdout + "\n" + out.stderr + "\n"); self.log_csv.see("end")
            if out.returncode == 0:
                self.status_csv.set(f"Done. See '{APP_OUT_CSV}'.")
            else:
                self.status_csv.set("Failed. See log.")
        except Exception as e:
            self.status_csv.set("Error."); messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = VAMGui()
    app.mainloop()
