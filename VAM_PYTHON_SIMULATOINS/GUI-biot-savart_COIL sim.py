import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from scipy.signal import sawtooth

mu0 = 4 * np.pi * 1e-7  # Vacuum permeability

class AnimatedCoilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EM Field Simulator with E/B Scaling")

        self.R = tk.DoubleVar(value=0.5)
        self.N_turns = tk.IntVar(value=10)
        self.I0 = tk.DoubleVar(value=1.0)
        self.grid_size = tk.IntVar(value=10)
        self.grid_range = tk.DoubleVar(value=1.0)
        self.field_boost = tk.DoubleVar(value=1.0)
        self.e_amp = tk.DoubleVar(value=1e13)
        self.omega = tk.DoubleVar(value=2.0)
        self.waveform = tk.StringVar(value='sin')
        self.show_B = tk.BooleanVar(value=True)
        self.show_E = tk.BooleanVar(value=True)

        self.t = 0.0
        self.is_running = False

        self._create_controls()
        self._create_plot_canvas()
        self.update_plot()

    def _create_controls(self):
        frm = ttk.Frame(self.root)
        frm.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        sliders = [
            ("Radius", self.R, 0.1, 2.0),
            ("Turns", self.N_turns, 1, 50),
            ("Current (I₀)", self.I0, 0.1, 5.0),
            ("Grid Size", self.grid_size, 5, 25),
            ("Grid Range", self.grid_range, 1.0, 5.0),
            ("Field Boost", self.field_boost, 0.1, 10.0),
            ("E-Field Scale", self.e_amp, 1e12, 1e14),
            ("Frequency ω", self.omega, 0.1, 10.0),
        ]
        for i, (label, var, mn, mx) in enumerate(sliders):
            ttk.Label(frm, text=label).grid(row=i, column=0, sticky="w")
            ttk.Scale(frm, variable=var, from_=mn, to=mx,
                      orient="horizontal", length=150).grid(row=i, column=1, sticky="we", pady=5)

        ttk.Label(frm, text="Waveform").grid(row=8, column=0, sticky="w")
        for i, mode in enumerate(['sin', 'square', 'saw']):
            ttk.Radiobutton(frm, text=mode.capitalize(), variable=self.waveform, value=mode).grid(row=8+i, column=1, sticky="w")

        ttk.Checkbutton(frm, text="Show B‑field", variable=self.show_B).grid(row=11, column=0, columnspan=2, sticky="w")
        ttk.Checkbutton(frm, text="Show E‑field", variable=self.show_E).grid(row=12, column=0, columnspan=2, sticky="w")

        ttk.Button(frm, text="Play/Pause", command=self.toggle_animation).grid(row=13, column=0, columnspan=2, pady=5)
        ttk.Button(frm, text="Update Now", command=self.update_plot).grid(row=14, column=0, columnspan=2, pady=5)

    def _create_plot_canvas(self):
        self.fig = plt.Figure(figsize=(7,7))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def toggle_animation(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.animate()

    def animate(self):
        if self.is_running:
            self.t += 0.005
            self.update_plot()
            self.root.after(50, self.animate)

    def waveform_value(self, t, omega, kind='sin'):
        wt = omega * t
        if kind == 'square':
            N = 10
            val = sum(np.sin((2*n - 1)*wt)/(2*n - 1) for n in range(1, N+1))
            dval = sum(np.cos((2*n - 1)*wt)*(2*n - 1) for n in range(1, N+1))
            return (4/np.pi)*val, (4/np.pi)*omega*dval
        elif kind == 'saw':
            val = sawtooth(wt, width=0.5)
            dval = omega
            return val, dval
        return np.sin(wt), omega * np.cos(wt)


    def update_plot(self):
        R, N, I0 = self.R.get(), self.N_turns.get(), self.I0.get()
        gs, r_range = self.grid_size.get(), self.grid_range.get()
        boostB, boostE = self.field_boost.get(), self.e_amp.get()
        omega, wave = self.omega.get(), self.waveform.get()
        show_B, show_E = self.show_B.get(), self.show_E.get()

        I_val, dI_val = self.waveform_value(self.t, omega, wave)
        I_t, dI_dt = I0 * I_val, I0 * dI_val

        theta = np.linspace(0, 2*np.pi*N, 800)
        z = np.linspace(-1, 1, 800)
        coil = np.stack([R*np.cos(theta), R*np.sin(theta), z], axis=1)

        X, Y, Z = np.meshgrid(
            np.linspace(-r_range, r_range, gs),
            np.linspace(-r_range, r_range, gs),
            np.linspace(-r_range, r_range, gs), indexing='ij'
        )

        Bx = np.zeros_like(X); By = np.zeros_like(Y); Bz = np.zeros_like(Z)
        Ex = np.zeros_like(X); Ey = np.zeros_like(Y); Ez = np.zeros_like(Z)

        if show_B or show_E:
            for i in range(len(coil)-1):
                dl = coil[i+1] - coil[i]
                rx, ry, rz = X - coil[i,0], Y - coil[i,1], Z - coil[i,2]
                r = np.sqrt(rx**2 + ry**2 + rz**2) + 1e-9

                cx, cy, cz = dl[1]*rz - dl[2]*ry, dl[2]*rx - dl[0]*rz, dl[0]*ry - dl[1]*rx
                factor = mu0 * I_t / (4*np.pi) / (r**3)

                Bx += factor * cx; By += factor * cy; Bz += factor * cz

        if show_E and show_B:
            scaleE = mu0 * dI_dt / (4*np.pi)
            Ex = -scaleE * (By*Z - Bz*Y)
            Ey = -scaleE * (Bz*X - Bx*Z)
            Ez = -scaleE * (Bx*Y - By*X)

        self.ax.clear()
        self.ax.set_title(f"t={self.t:.2f}s I={I_t:.2f}A Wave={wave}")
        self.ax.set_xlim(-r_range, r_range)
        self.ax.set_ylim(-r_range, r_range)
        self.ax.set_zlim(-r_range, r_range)
        self.ax.plot(coil[:,0], coil[:,1], coil[:,2], 'k', linewidth=1)

        def draw_field(U, V, W, color):
            mag = np.sqrt(U**2 + V**2 + W**2)
            mask = mag.flatten()>1e-15
            U, V, W, mag = U.flatten()[mask], V.flatten()[mask], W.flatten()[mask], mag.flatten()[mask]
            Un, Vn, Wn = np.nan_to_num(U/mag), np.nan_to_num(V/mag), np.nan_to_num(W/mag)
            if mag.size == 0 or np.all(mag == 0):
                return  # Skip drawing
            max_mag = np.max(mag)
            alpha = np.clip(mag / max_mag, 0.1, 1.0)

            cols = np.zeros((len(mag),4))
            cols[:, {'blue':2,'red':0}[color]] = 1.0
            cols[:,3] = alpha
            scale = (boostE if color=='red' else boostB) * (1e-13 if color=='red' else 1.0)
            self.ax.quiver(X.flatten()[mask], Y.flatten()[mask], Z.flatten()[mask],
                           Un*scale, Vn*scale, Wn*scale, normalize=False, color=cols)

        if show_B:
            draw_field(Bx, By, Bz, 'blue')
        if show_E:
            draw_field(Ex, Ey, Ez, 'red')

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimatedCoilApp(root)
    root.mainloop()
