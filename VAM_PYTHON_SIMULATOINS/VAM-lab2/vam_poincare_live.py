#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VAM Poincaré Sphere Live Visualizer
-----------------------------------
Compute polarization-like amplitudes (alpha, beta) from a simulated vorticity
field in the Vortex Æther Model (VAM) and animate the point on the Poincaré/
Bloch sphere in real time.

Two modes:
1) DEMO (default): synthetic (alpha, beta) to illustrate superposition & phase.
2) NPZ: load a .npz file containing vorticity fields and grid meta, then compute
   alpha = <omega_L, omega>, beta = <omega_R, omega> using an energy-weighted
   inner product, and animate the resulting Stokes vector on the sphere.

Expected .npz fields (NPZ mode):
- omega:    shape (T, Nx, Ny, Nz, 3)  vorticity field over time (SI units)
- omega_L:  shape (Nx, Ny, Nz, 3)     L-twist mode (basis)
- omega_R:  shape (Nx, Ny, Nz, 3)     R-twist mode (basis)
- rho:      scalar or array           æther density (kg/m^3)
- dx, dy, dz: scalars                 grid spacings (m)

Run:
  $ python vam_poincare_live.py                     # demo
  $ python vam_poincare_live.py --npz data.npz      # from arrays
  $ python vam_poincare_live.py --npz data.npz --save out.mp4 --fps 30

Notes:
- We deliberately avoid picking specific colors to keep styling neutral.
- For large grids, consider chunking or downsampling before computing.
"""

import argparse
import numpy as np
import sys
import os
from typing import Tuple, Optional, Union

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)


# -------------------------------
# Utilities
# -------------------------------

def ensure_array(x: Union[float, np.ndarray], shape_like: np.ndarray) -> np.ndarray:
    """Broadcast scalar to the shape of 'shape_like' if needed."""
    x_arr = np.asarray(x)
    if x_arr.ndim == 0:
        return np.full(shape_like.shape[:-1], float(x_arr))  # drop last dim (vector components)
    return x_arr


def inner_product(omega_a: np.ndarray,
                  omega_b: np.ndarray,
                  rho: Union[float, np.ndarray],
                  dV: float) -> float:
    """
    Energy-weighted inner product:
        <a,b> = (rho/2) ∫ omega_a · omega_b dV
    Assumes omega_* shape (..., 3) and rho scalar or broadcastable to grid.
    """
    # omega_a, omega_b: (..., 3)
    # rho_grid: (..., )
    rho_grid = ensure_array(rho, omega_a)
    dot_ab = np.sum(omega_a * omega_b, axis=-1)  # (...,)
    val = 0.5 * np.sum(rho_grid * dot_ab) * dV
    return float(val)


def norm_mode(omega_k: np.ndarray,
              rho: Union[float, np.ndarray],
              dV: float) -> float:
    """Mode norm induced by energy metric: ||k|| = sqrt(<k,k>)"""
    return np.sqrt(max(inner_product(omega_k, omega_k, rho, dV), 0.0))


def compute_alpha_beta(omega: np.ndarray,
                       omega_L: np.ndarray,
                       omega_R: np.ndarray,
                       rho: Union[float, np.ndarray],
                       dV: float,
                       normalize_modes: bool = True) -> Tuple[complex, complex]:
    """
    Project the field onto L/R twist modes:
        alpha = <omega_L, omega> / ||omega_L||^2 (if normalize_modes=True)
        beta  = <omega_R, omega> / ||omega_R||^2
    If modes are already normalized to unit energy, set normalize_modes=True (default).
    """
    if normalize_modes:
        nL2 = max(norm_mode(omega_L, rho, dV)**2, 1e-300)
        nR2 = max(norm_mode(omega_R, rho, dV)**2, 1e-300)
    else:
        # Use raw projections if the caller guarantees unit-norm modes.
        nL2 = 1.0
        nR2 = 1.0

    # Real-valued inner products (fields are real); keep complex type for consistency
    a = inner_product(omega_L, omega, rho, dV) / nL2
    b = inner_product(omega_R, omega, rho, dV) / nR2
    return complex(a), complex(b)


def stokes_from_ab(alpha: complex, beta: complex) -> Tuple[float, float, float, float]:
    """
    Compute Stokes parameters:
      S0 = |a|^2 + |b|^2
      S1 = 2 Re(a b*)
      S2 = 2 Im(a b*)
      S3 = |a|^2 - |b|^2
    Returns (S0, S1, S2, S3).
    """
    a, b = alpha, beta
    ab_conj = a * np.conj(b)
    S0 = float(abs(a)**2 + abs(b)**2)
    S1 = float(2.0 * np.real(ab_conj))
    S2 = float(2.0 * np.imag(ab_conj))
    S3 = float(abs(a)**2 - abs(b)**2)
    return S0, S1, S2, S3


def unit_vector(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def equal_aspect_3d(ax):
    """Set equal aspect ratio for 3D axes."""
    extents = np.array([getattr(ax, f'get_{dim}lim')() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, f'set_{dim}lim')(ctr - r, ctr + r)


# -------------------------------
# Demo generator
# -------------------------------

def demo_generator(num_frames: int = 360,
                   theta: float = np.pi/2,
                   phi_rate: float = np.pi/90) -> Tuple[np.ndarray, np.ndarray]:
    """
    Produce a sequence of (alpha, beta) for a pure state that sits at polar angle 'theta'
    and precesses in phase: |psi> = cos(theta/2)|L> + e^{i phi(t)} sin(theta/2)|R|.
    Returns (alphas, betas) arrays of shape (T,).
    """
    ts = np.arange(num_frames)
    phi = phi_rate * ts
    a = np.cos(theta/2.0) * np.ones_like(phi, dtype=np.complex128)
    b = np.exp(1j * phi) * np.sin(theta/2.0)
    return a, b


# -------------------------------
# NPZ loader
# -------------------------------

def load_npz_and_project(path: str,
                         normalize_modes: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load vorticity arrays from .npz and compute (alpha_t, beta_t) over time.
    Returns two complex arrays of shape (T,).
    """
    data = np.load(path, allow_pickle=False)
    required = ['omega', 'omega_L', 'omega_R', 'dx', 'dy', 'dz', 'rho']
    for key in required:
        if key not in data:
            raise KeyError(f"Missing '{key}' in npz file. Found keys: {list(data.keys())}")

    omega = data['omega']        # (T, Nx, Ny, Nz, 3)
    omega_L = data['omega_L']    # (Nx, Ny, Nz, 3)
    omega_R = data['omega_R']    # (Nx, Ny, Nz, 3)
    dx = float(np.asarray(data['dx']).squeeze())
    dy = float(np.asarray(data['dy']).squeeze())
    dz = float(np.asarray(data['dz']).squeeze())
    rho = data['rho']            # scalar or array (Nx, Ny, Nz)

    if omega.ndim != 5 or omega.shape[-1] != 3:
        raise ValueError("omega must have shape (T, Nx, Ny, Nz, 3)")
    if omega_L.shape != omega.shape[1:]:
        raise ValueError("omega_L must have shape (Nx, Ny, Nz, 3) matching omega's spatial shape")
    if omega_R.shape != omega.shape[1:]:
        raise ValueError("omega_R must have shape (Nx, Ny, Nz, 3) matching omega's spatial shape")

    dV = dx * dy * dz
    T = omega.shape[0]
    alphas = np.zeros(T, dtype=np.complex128)
    betas  = np.zeros(T, dtype=np.complex128)

    # Precompute mode norms if requested
    if normalize_modes:
        nL = norm_mode(omega_L, rho, dV)
        nR = norm_mode(omega_R, rho, dV)
        nL2 = max(nL**2, 1e-300)
        nR2 = max(nR**2, 1e-300)
    else:
        nL2 = 1.0
        nR2 = 1.0

    for t in range(T):
        w = omega[t]  # (Nx, Ny, Nz, 3)
        a = inner_product(omega_L, w, rho, dV) / nL2
        b = inner_product(omega_R, w, rho, dV) / nR2
        alphas[t] = a
        betas[t] = b

    return alphas, betas


# -------------------------------
# Visualization
# -------------------------------

def make_sphere(ax, r: float = 1.0, n: int = 50):
    """Draw a wireframe sphere of radius r with n x n grid."""
    u = np.linspace(0, 2*np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, linewidth=0.5, alpha=0.3)


def animate_stokes(alphas: np.ndarray,
                   betas: np.ndarray,
                   save: Optional[str] = None,
                   fps: int = 30):
    """Animate point (S1,S2,S3)/S0 on the sphere."""
    # Precompute normalized Stokes vectors
    S = []
    for a, b in zip(alphas, betas):
        S0, S1, S2, S3 = stokes_from_ab(a, b)
        if S0 <= 0:
            s = np.array([0.0, 0.0, 0.0])
        else:
            s = np.array([S1/S0, S2/S0, S3/S0])
        s = np.clip(s, -1.0, 1.0)
        S.append(s)
    S = np.array(S)  # (T, 3)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    make_sphere(ax, 1.0, 40)

    # Axes
    ax.set_xlabel('S1')
    ax.set_ylabel('S2')
    ax.set_zlabel('S3')
    ax.set_title('VAM Polarization on Poincaré/Bloch Sphere')

    # Unit axes lines
    ax.plot([-1, 1], [0, 0], [0, 0], linewidth=1.0)
    ax.plot([0, 0], [-1, 1], [0, 0], linewidth=1.0)
    ax.plot([0, 0], [0, 0], [-1, 1], linewidth=1.0)

    point, = ax.plot([S[0,0]], [S[0,1]], [S[0,2]], marker='o', markersize=6)
    trace, = ax.plot([S[0,0]], [S[0,1]], [S[0,2]], linewidth=1.0)

    equal_aspect_3d(ax)

    def update(i):
        # update point and short trailing trace
        start = max(0, i - 200)
        xs, ys, zs = S[start:i+1, 0], S[start:i+1, 1], S[start:i+1, 2]
        point.set_data([S[i,0]], [S[i,1]])
        point.set_3d_properties([S[i,2]])
        trace.set_data(xs, ys)
        trace.set_3d_properties(zs)
        return point, trace

    ani = FuncAnimation(fig, update, frames=len(S), interval=1000/max(fps,1), blit=False)

    if save:
        try:
            # Try to save using default writer; user can install ffmpeg if needed.
            ani.save(save, fps=fps)
            print(f"[INFO] Saved animation to: {save}")
        except Exception as e:
            print(f"[WARN] Could not save animation ({e}). Falling back to interactive show.")
            plt.show()
    else:
        plt.show()


# -------------------------------
# Main
# -------------------------------

def main():
    parser = argparse.ArgumentParser(description="VAM Poincaré Sphere Live Visualizer")
    parser.add_argument("--npz", type=str, default=None, help="Path to .npz with omega fields & meta")
    parser.add_argument("--fps", type=int, default=30, help="Animation frames per second")
    parser.add_argument("--save", type=str, default=None, help="Output video file (e.g., out.mp4). If omitted, shows interactively.")
    parser.add_argument("--theta", type=float, default=np.pi/2, help="DEMO: polar angle for the state (0=pure L, pi=pure R)")
    parser.add_argument("--phi-rate", type=float, default=np.pi/90, help="DEMO: phase advance per frame (rad/frame)")
    args = parser.parse_args()

    if args.npz is None:
        # DEMO mode
        alphas, betas = demo_generator(num_frames=360, theta=args.theta, phi_rate=args.phi_rate)
        animate_stokes(alphas, betas, save=args.save, fps=args.fps)
    else:
        if not os.path.exists(args.npz):
            print(f"[ERROR] NPZ file not found: {args.npz}", file=sys.stderr)
            sys.exit(1)
        alphas, betas = load_npz_and_project(args.npz, normalize_modes=True)
        animate_stokes(alphas, betas, save=args.save, fps=args.fps)


if __name__ == "__main__":
    main()
