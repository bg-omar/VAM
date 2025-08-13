import importlib.util, inspect, os, sys, threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import json
import traceback

import matplotlib
# Use TkAgg so the FigureCanvasTkAgg works with Tkinter
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from test_base import BaseTest

APP_TITLE = "VAM Lab — Electron–Swirl Experiments"
PLUGIN_PREFIX = "vamtest_"
PLUGIN_SUFFIX = "_vamtest.py"  # optional alternate suffix

def splash(root, delay_ms=1200):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    w, h = 420, 220
    x = (root.winfo_screenwidth()-w)//2
    y = (root.winfo_screenheight()-h)//2
    splash.geometry(f"{w}x{h}+{x}+{y}")
    frame = ttk.Frame(splash, padding=20)
    frame.pack(expand=True, fill="both")
    ttk.Label(frame, text="VAM Lab", font=("Segoe UI", 20, "bold")).pack(pady=(8,4))
    ttk.Label(frame, text="Electron–Swirl Transport & QC Playground", font=("Segoe UI", 11)).pack(pady=(0,8))
    ttk.Label(frame, text="Loading tests…", font=("Segoe UI", 10)).pack(pady=(8,0))
    root.after(delay_ms, splash.destroy)

def discover_tests(folder: Path):
    tests = []
    for p in folder.iterdir():
        if p.is_file() and ((p.name.startswith(PLUGIN_PREFIX) and p.suffix==".py") or p.name.endswith(PLUGIN_SUFFIX)):
            spec = importlib.util.spec_from_file_location(p.stem, str(p))
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)  # type: ignore
            except Exception as e:
                print(f"[WARN] Failed to import {p}: {e}")
                traceback.print_exc()
                continue
            test_cls = getattr(mod, "TEST_CLASS", None)
            if test_cls is None:
                for _, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, BaseTest) and obj is not BaseTest:
                        test_cls = obj; break
            if test_cls is None:
                continue
            try:
                tests.append(test_cls())
            except Exception as e:
                print(f"[WARN] Failed to instantiate {p}: {e}")
                traceback.print_exc()
    tests.sort(key=lambda t: t.name.lower())
    return tests

class ParamsEditor(ttk.Frame):
    def __init__(self, master, params: dict):
        super().__init__(master)
        self.vars = {}
        row=0
        for k,v in params.items():
            ttk.Label(self, text=str(k)).grid(row=row, column=0, sticky="w", padx=4, pady=2)
            var = tk.StringVar(value=str(v))
            ent = ttk.Entry(self, textvariable=var, width=18)
            ent.grid(row=row, column=1, sticky="ew", padx=4, pady=2)
            self.vars[k]=var
            row+=1
        self.columnconfigure(1, weight=1)

    def get_params(self):
        out = {}
        for k,var in self.vars.items():
            txt = var.get()
            try:
                out[k]=json.loads(txt)
            except Exception:
                try:
                    out[k]=float(txt)
                except Exception:
                    out[k]=txt
        return out

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x700")
        style = ttk.Style(self);
        try:
            style.theme_use("clam")
        except Exception:
            pass

        splash(self)

        self.tests = discover_tests(Path(__file__).parent)
        self.selected = None
        self.figure = Figure(figsize=(6,4), dpi=120)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()

        # Layout
        left = ttk.Frame(self); left.pack(side="left", fill="y", padx=8, pady=8)
        mid = ttk.Frame(self); mid.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        right = ttk.Frame(self); right.pack(side="right", fill="y", padx=8, pady=8)

        ttk.Label(left, text="Available Tests", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.listbox = tk.Listbox(left, height=20)
        self.listbox.pack(fill="y", expand=False)
        for t in self.tests:
            self.listbox.insert("end", t.name)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.desc = tk.Text(left, width=36, height=12, wrap="word")
        self.desc.pack(pady=(8,0))
        self.desc.configure(state="disabled")

        ttk.Label(right, text="Parameters", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.param_frame = ttk.Frame(right); self.param_frame.pack(fill="y", expand=True)
        self.params_editor = None

        btns = ttk.Frame(right); btns.pack(fill="x", pady=6)
        self.run_btn = ttk.Button(btns, text="Run ▶", command=self.run_selected)
        self.run_btn.pack(side="left", padx=4)
        self.save_btn = ttk.Button(btns, text="Save Results JSON", command=self.save_results, state="disabled")
        self.save_btn.pack(side="left", padx=4)

        self.canvas_widget.pack(in_=mid, fill="both", expand=True)

        if self.tests:
            self.listbox.selection_set(0)
            self.on_select()

        footer = ttk.Label(self, text="Drop new tests into this folder named 'vamtest_*.py' or '*_vamtest.py' and restart.", anchor="center")
        footer.pack(side="bottom", fill="x")

        self.results_cache = None

    def on_select(self, *_):
        idx = self.listbox.curselection()
        if not idx: return
        test = self.tests[idx[0]]
        self.selected = test
        self.desc.configure(state="normal"); self.desc.delete("1.0","end")
        self.desc.insert("end", test.description); self.desc.configure(state="disabled")
        for w in self.param_frame.winfo_children(): w.destroy()
        self.params_editor = ParamsEditor(self.param_frame, test.default_params())
        # Clear figure on selection
        self.figure.clf(); self.canvas.draw()

    def run_selected(self):
        if not self.selected:
            messagebox.showwarning("No test", "Please select a test.")
            return
        params = self.params_editor.get_params() if self.params_editor else self.selected.default_params()
        self.run_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")

        def worker():
            try:
                res = self.selected.run(params, self.figure)
            except Exception as e:
                tb = traceback.format_exc()
                # Show error back on main thread
                self.after(0, lambda: messagebox.showerror("Run error", f"{e}\n\n{tb}"))
                self.after(0, lambda: self.run_btn.configure(state="normal"))
                return
            # Update GUI on main thread
            def finish():
                self.results_cache = res
                self.canvas.draw()
                self.run_btn.configure(state="normal")
                self.save_btn.configure(state="normal")
            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    def save_results(self):
        if self.results_cache is None:
            messagebox.showinfo("No results", "Run a test first.")
            return
        base = Path(__file__).parent / "results"
        base.mkdir(exist_ok=True)
        i=1
        while True:
            path = base / f"result_{i:03d}.json"
            if not path.exists(): break
            i+=1
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.results_cache, f, indent=2)
        messagebox.showinfo("Saved", f"Saved: {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
