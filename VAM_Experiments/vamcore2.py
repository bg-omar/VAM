# VAMcore refactor stubs for Rodin coil + fields
# Uses existing VAMbindings where available; isolates heavy kernels as C++/PyBind11 class candidates.
# Existing bindings referenced:
#   - vambindings.biot_savart_velocity
#   - vambindings.compute_kinetic_energy
#   - vambindings.VortexKnotSystem
#
# New C++ classes to add (proposed → file layout):
#   1) BiotSavartGridEvaluator         → ./src/biot_savart_grid.cpp|.h, ./src_bindings/py_biot_savart_grid.cpp
#   2) SegmentTangentBuilder           → ./src/segment_builder.cpp|.h,   ./src_bindings/py_segment_builder.cpp
#   3) ThreePhaseCoilAssembler         → ./src/three_phase_coil.cpp|.h,  ./src_bindings/py_three_phase_coil.cpp
#   4) StreamlineIntegrator3D          → ./src/streamline.cpp|.h,        ./src_bindings/py_streamline.cpp
#   5) VorticityCurvatureTensor        → ./src/swirl_curvature.cpp|.h,   ./src_bindings/py_swirl_curvature.cpp
#   6) SwirlGravityField               → ./src/swirl_gravity.cpp|.h,     ./src_bindings/py_swirl_gravity.cpp
from __future__ import annotations

import numpy as np
from typing import Tuple, List

from typing import Tuple, List
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Minimal import block; extend if more bindings exist in vambindings.cp311-*.pyd
from vambindings import (
    biot_savart_velocity,   # scalar point evaluation along poly-segment filament(s)
    compute_kinetic_energy, # KE(V, rho)
    VortexKnotSystem        # existing example object
)
# vam_rodin_core.py
# VAMcore-ready Python layer for Rodin-coil/field workflows.
# References existing VAMbindings and defines class APIs to be backed by C++/PyBind11.
# Proposed C++/binding files:
#   ./src/segment_builder.cpp|.h            ./src_bindings/py_segment_builder.cpp
#   ./src/biot_savart_grid.cpp|.h           ./src_bindings/py_biot_savart_grid.cpp
#   ./src/three_phase_coil.cpp|.h           ./src_bindings/py_three_phase_coil.cpp
#   ./src/streamline.cpp|.h                 ./src_bindings/py_streamline.cpp
#   ./src/swirl_curvature.cpp|.h            ./src_bindings/py_swirl_curvature.cpp
#   ./src/swirl_gravity.cpp|.h              ./src_bindings/py_swirl_gravity.cpp

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401



# -----------------------
# Geometry (kept in Python)
# -----------------------

def generate_alternating_skip_sequence(
        corners: int,
        step_even: int,
        step_odd: int,
        radius: float = 1.0,
        z_layer: float = 0.0,
        angle_offset: float = 0.0
) -> Tuple[List[int], np.ndarray]:
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    positions = np.array([
        (radius*np.cos(angles[i % corners] + angle_offset),
         radius*np.sin(angles[i % corners] + angle_offset),
         z_layer)
        for i in sequence
    ], dtype=float)
    return sequence, positions


def get_wire_arrows(positions: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Return (M,3) segment starts and (M,3) tangents."""
    p0 = positions[:-1].astype(float)
    p1 = positions[1:].astype(float)
    tangents = p1 - p0
    return p0, tangents


# -----------------------------------------
# Candidate 1: SegmentTangentBuilder (C++)
# -----------------------------------------

class SegmentTangentBuilder:
    """
    Python fallback. Promote to C++ for large coils/layers.
    Target: build layered multi-phase segment starts/tangents.
    """
    def build_layered(self, seq: List[int], corners: int, angles: np.ndarray,
                      layers: int, layer_spacing: float, angle_offset: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        pts: List[List[float]] = []
        for L in range(layers):
            z_off = L * layer_spacing
            for i in range(len(seq)):
                a = angles[(seq[i]-1) % corners] + angle_offset
                x, y = np.cos(a), np.sin(a)
                z = z_off + i * (layer_spacing / max(1, (len(seq)-1)))
                pts.append([x, y, z])
        positions = np.asarray(pts, dtype=float)
        return get_wire_arrows(positions)

    def build_phase(self, corners: int, step_even: int, step_odd: int,
                    layers: int, layer_spacing: float, angle_offset: float,
                    angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        seq, _ = generate_alternating_skip_sequence(corners, step_even, step_odd, angle_offset=angle_offset)
        return self.build_layered(seq, corners, angles, layers, layer_spacing, angle_offset)


# ------------------------------------------------
# Candidate 2: BiotSavartGridEvaluator (C++ core)
# ------------------------------------------------

class BiotSavartGridEvaluator:
    """
    Python wrapper that calls existing scalar vambindings.biot_savart_velocity
    per grid point. Replace with a batch C++ kernel that accepts:
        evaluate(grid: (N,3), seg_p0: (M,3), seg_t: (M,3), gamma: float) -> (N,3)
    """
    def evaluate(self, grid_points: np.ndarray, seg_p0: np.ndarray, seg_t: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        gp = np.asarray(grid_points, dtype=float)
        p0 = np.asarray(seg_p0, dtype=float).tolist()
        tt = np.asarray(seg_t, dtype=float).tolist()
        out = np.empty_like(gp)
        for i, r in enumerate(gp.tolist()):
            out[i] = biot_savart_velocity(r, p0, tt, gamma)
        return out


# ----------------------------------------------------
# Candidate 3: ThreePhaseCoilAssembler (C++ utility)
# ----------------------------------------------------

class ThreePhaseCoilAssembler:
    """
    Assembles 3 phases with 120° offsets and returns concatenated segments.
    Intended for C++ once stable.
    """
    def __init__(self, corners: int, step_even: int, step_odd: int, layers: int, layer_spacing: float):
        self.corners = corners
        self.step_even = step_even
        self.step_odd = step_odd
        self.layers = layers
        self.layer_spacing = layer_spacing

    def assemble(self, angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        builder = SegmentTangentBuilder()
        p_all, t_all = [], []
        for ang_off in (0.0, 2*np.pi/3, 4*np.pi/3):
            p0, t = builder.build_phase(self.corners, self.step_even, self.step_odd,
                                        self.layers, self.layer_spacing, ang_off, angles)
            p_all.append(p0); t_all.append(t)
        return np.vstack(p_all), np.vstack(t_all)


# ------------------------------------------------
# Candidate 4: StreamlineIntegrator3D (C++ solver)
# ------------------------------------------------

class StreamlineIntegrator3D:
    """
    Field-line integrator over a discrete 3D vector field on a rectilinear grid.
    Python fallback uses nearest-index sampling. Promote to C++ ODE or RK4.
    """
    def __init__(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, Fx: np.ndarray, Fy: np.ndarray, Fz: np.ndarray):
        self.X, self.Y, self.Z = X, Y, Z
        self.Fx, self.Fy, self.Fz = Fx, Fy, Fz

    def _sample(self, r: np.ndarray) -> np.ndarray:
        xi = np.argmin(np.abs(self.X[:,0,0] - r[0]))
        yi = np.argmin(np.abs(self.Y[0,:,0] - r[1]))
        zi = np.argmin(np.abs(self.Z[0,0,:] - r[2]))
        if 0 <= xi < self.Fx.shape[0] and 0 <= yi < self.Fy.shape[1] and 0 <= zi < self.Fz.shape[2]:
            v = np.array([self.Fx[xi, yi, zi], self.Fy[xi, yi, zi], self.Fz[xi, yi, zi]], dtype=float)
            n = np.linalg.norm(v)
            return v / (n + 1e-12)
        return np.zeros(3, dtype=float)

    def integrate(self, seed: np.ndarray, ds: float = 0.03, length: float = 3.5) -> np.ndarray:
        steps = int(max(1, length / max(ds, 1e-6)))
        traj = [np.asarray(seed, dtype=float)]
        for _ in range(steps):
            d = self._sample(traj[-1])
            if not np.any(d):
                break
            traj.append(traj[-1] + ds * d)
        return np.vstack(traj)


# -----------------------------------------------------------
# Candidate 5–6: VorticityCurvatureTensor & SwirlGravityField
# -----------------------------------------------------------

class VorticityCurvatureTensor:
    """
    Python reference for ω = ∇×v and R_ij = 0.5*(∂i ω_j + ∂j ω_i).
    Promote to C++ for performance and memory locality.
    """
    def curl(self, vx: np.ndarray, vy: np.ndarray, vz: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        dvz_dy, dvz_dx, dvz_dz = np.gradient(vz, axis=(1, 0, 2))
        dvy_dz, dvy_dx, dvy_dy = np.gradient(vy, axis=(2, 0, 1))
        dvx_dz, dvx_dx, dvx_dy = np.gradient(vx, axis=(2, 0, 1))
        omega_x = dvy_dz - dvz_dy
        omega_y = dvz_dx - dvx_dz
        omega_z = dvx_dy - dvy_dx
        return omega_x, omega_y, omega_z

    def curvature(self, omega_x: np.ndarray, omega_y: np.ndarray, omega_z: np.ndarray) -> np.ndarray:
        R = np.empty((3, 3, *omega_x.shape), dtype=omega_x.dtype)
        gox = np.gradient(omega_x)
        goy = np.gradient(omega_y)
        goz = np.gradient(omega_z)
        G = [gox, goy, goz]
        for i in range(3):
            for j in range(3):
                R[i, j] = 0.5 * (G[j][i] + G[i][j])
        return R


class SwirlGravityField:
    """
    Python reference for g_i = - ω_j R_ij.
    Promote to C++ for fused loops and cache-friendly ops.
    """
    def compute(self, omega: Tuple[np.ndarray, np.ndarray, np.ndarray], R: np.ndarray) -> np.ndarray:
        ox, oy, oz = omega
        omega_vec = np.stack([ox, oy, oz], axis=0)  # (3, Nx, Ny, Nz)
        g = np.zeros_like(omega_vec)
        for i in range(3):
            acc = np.zeros_like(ox)
            for j in range(3):
                acc -= omega_vec[j] * R[i, j]
            g[i] = acc
        return g


# -----------------------
# Convenience orchestrators
# -----------------------

def field_on_grid_from_segments(
        X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
        seg_p0: np.ndarray, seg_t: np.ndarray, gamma: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute (Fx,Fy,Fz) on rectilinear grid via VAM (scalar loop) → replace with BiotSavartGridEvaluator C++."""
    gp = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    V = BiotSavartGridEvaluator().evaluate(gp, seg_p0, seg_t, gamma)
    V = V.reshape(*X.shape, 3)
    return V[...,0], V[...,1], V[...,2]


def kinetic_energy_from_field(V: np.ndarray, rho: float) -> float:
    """V is (N,3) flattened; delegates to vambindings.compute_kinetic_energy."""
    return compute_kinetic_energy(V.tolist(), rho)


# -----------------------
# Example usage snippets
# -----------------------

def example_trefoil_field(nvec: int = 9, L: float = 5.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    knot = VortexKnotSystem()
    knot.initialize_trefoil_knot()
    pos = np.asarray(knot.get_positions(), dtype=float)
    tan = np.asarray(knot.get_tangents(), dtype=float)
    x = np.linspace(-L, L, nvec); y = np.linspace(-L, L, nvec); z = np.linspace(-L, L, nvec)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    Fx, Fy, Fz = field_on_grid_from_segments(X, Y, Z, pos[:-1], np.diff(pos, axis=0))
    return X, Y, Z, np.stack([Fx, Fy, Fz], axis=0)


def example_three_phase_segments(corners=32, s_even=11, s_odd=-9, layers=10, dz=0.05) -> Tuple[np.ndarray, np.ndarray]:
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    assembler = ThreePhaseCoilAssembler(corners, s_even, s_odd, layers, dz)
    return assembler.assemble(angles)




# ---------- Geometry helpers (Python) ----------

def generate_alternating_skip_sequence(
        corners: int,
        step_even: int,
        step_odd: int,
        radius: float = 1.0,
        z_layer: float = 0.0,
        angle_offset: float = 0.0
) -> Tuple[List[int], np.ndarray]:
    """Return (sequence, positions[corners+1,3]) for star skip pattern on a circle."""
    sequence: List[int] = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    pos = np.empty((len(sequence), 3), dtype=float)
    for k, idx in enumerate(sequence):
        a = angles[(idx - 1) % corners] + angle_offset
        pos[k] = (radius*np.cos(a), radius*np.sin(a), z_layer)
    return sequence, pos


def arrows_from_positions(positions: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Convert a polyline positions[N,3] to segment starts P0[M,3] and tangents T[M,3], M=N-1."""
    P0 = np.ascontiguousarray(positions[:-1], dtype=float)
    T  = np.ascontiguousarray(np.diff(positions, axis=0), dtype=float)
    return P0, T


# ---------- CANDIDATE CLASS 1: SegmentTangentBuilder (C++) ----------

class SegmentTangentBuilder:
    """
    Build layered coil segments and tangents.
    C++ target: class SegmentTangentBuilder with methods:
      - build_layered(seq, angles, layers, dz, offset) -> (P0, T)
      - build_phase(corners, s_even, s_odd, layers, dz, offset, angles) -> (P0, T)
    """

    def build_layered(
            self,
            seq: List[int],
            corners: int,
            angles: np.ndarray,
            layers: int,
            layer_spacing: float,
            angle_offset: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        pts: List[List[float]] = []
        Lseq = max(1, len(seq) - 1)
        for L in range(layers):
            z0 = L * layer_spacing
            for i in range(len(seq)):
                a = angles[(seq[i]-1) % corners] + angle_offset
                x, y = np.cos(a), np.sin(a)
                z = z0 + (i * (layer_spacing / Lseq))
                pts.append([x, y, z])
        P = np.asarray(pts, dtype=float)
        return arrows_from_positions(P)

    def build_phase(
            self,
            corners: int,
            step_even: int,
            step_odd: int,
            layers: int,
            layer_spacing: float,
            angle_offset: float,
            angles: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        seq, _ = generate_alternating_skip_sequence(
            corners, step_even, step_odd, angle_offset=angle_offset
        )
        return self.build_layered(seq, corners, angles, layers, layer_spacing, angle_offset)


# ---------- CANDIDATE CLASS 2: BiotSavartGridEvaluator (C++) ----------

class BiotSavartGridEvaluator:
    """
    Evaluate induced velocity at many points from filament segments.
    Python fallback loops over grid points calling vambindings.biot_savart_velocity.

    C++ target signature:
      evaluate(grid[N,3], seg_p0[M,3], seg_t[M,3], gamma: float=1.0) -> vel[N,3]
    """

    def evaluate(
            self,
            grid_points: np.ndarray,
            seg_p0: np.ndarray,
            seg_t: np.ndarray,
            gamma: float = 1.0
    ) -> np.ndarray:
        gp = np.ascontiguousarray(grid_points, dtype=float)
        p0 = np.ascontiguousarray(seg_p0, dtype=float).tolist()
        tt = np.ascontiguousarray(seg_t, dtype=float).tolist()
        V = np.empty_like(gp)
        # scalar loop → to be replaced by batch C++ kernel
        for i, r in enumerate(gp.tolist()):
            V[i] = biot_savart_velocity(r, p0, tt, gamma)
        return V


# ---------- CANDIDATE CLASS 3: ThreePhaseCoilAssembler (C++) ----------

class ThreePhaseCoilAssembler:
    """
    Assemble three phases with 120° offsets into concatenated segment arrays.

    C++ target: class ThreePhaseCoilAssembler with:
      assemble(angles, corners, s_even, s_odd, layers, dz) -> (P0, T)
    """

    def __init__(self, corners: int, s_even: int, s_odd: int, layers: int, dz: float):
        self.corners = corners
        self.s_even = s_even
        self.s_odd  = s_odd
        self.layers = layers
        self.dz     = dz

    def assemble(self, angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        builder = SegmentTangentBuilder()
        P0s, Ts = [], []
        for off in (0.0, 2*np.pi/3, 4*np.pi/3):
            P0, T = builder.build_phase(
                self.corners, self.s_even, self.s_odd, self.layers, self.dz, off, angles
            )
            P0s.append(P0); Ts.append(T)
        return np.vstack(P0s), np.vstack(Ts)


# ---------- CANDIDATE CLASS 4: StreamlineIntegrator3D (C++) ----------

class StreamlineIntegrator3D:
    """
    Integrate field lines on a rectilinear grid using nearest-cell sampling (reference).
    C++ target: RK4 integrator with trilinear interpolation and bounds checks.
    """

    def __init__(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
                 Fx: np.ndarray, Fy: np.ndarray, Fz: np.ndarray):
        self.X, self.Y, self.Z = X, Y, Z
        self.Fx, self.Fy, self.Fz = Fx, Fy, Fz

    def _sample_dir(self, r: np.ndarray) -> np.ndarray:
        xi = np.argmin(np.abs(self.X[:,0,0] - r[0]))
        yi = np.argmin(np.abs(self.Y[0:,0,0] - self.Y[0,0,0]))  # guard for shape
        yi = np.argmin(np.abs(self.Y[0,:,0] - r[1]))
        zi = np.argmin(np.abs(self.Z[0,0,:] - r[2]))
        if 0 <= xi < self.Fx.shape[0] and 0 <= yi < self.Fy.shape[1] and 0 <= zi < self.Fz.shape[2]:
            v = np.array([self.Fx[xi, yi, zi], self.Fy[xi, yi, zi], self.Fz[xi, yi, zi]], dtype=float)
            n = np.linalg.norm(v)
            if n == 0.0:
                return np.zeros(3)
            return v / n
        return np.zeros(3)

    def integrate(self, seed: np.ndarray, ds: float = 0.03, length: float = 3.5) -> np.ndarray:
        steps = int(max(1, length / max(ds, 1e-9)))
        traj = [np.asarray(seed, dtype=float)]
        for _ in range(steps):
            d = self._sample_dir(traj[-1])
            if not np.any(d):
                break
            traj.append(traj[-1] + ds * d)
        return np.vstack(traj)


# ---------- CANDIDATE CLASS 5: VorticityCurvatureTensor (C++) ----------

class VorticityCurvatureTensor:
    """
    Compute ω = ∇×v and the symmetric swirl curvature tensor R_ij = 0.5(∂i ω_j + ∂j ω_i).
    Grid spacing can be provided for correct physical gradients.
    """

    def curl(self, vx, vy, vz, spacing=1.0):
        if np.isscalar(spacing):
            dx = dy = dz = float(spacing)
        else:
            dx, dy, dz = map(float, spacing)

        dvx_dx, dvx_dy, dvx_dz = np.gradient(vx, dx, dy, dz, edge_order=2)
        dvy_dx, dvy_dy, dvy_dz = np.gradient(vy, dx, dy, dz, edge_order=2)
        dvz_dx, dvz_dy, dvz_dz = np.gradient(vz, dx, dy, dz, edge_order=2)

        omega_x = dvy_dz - dvz_dy
        omega_y = dvz_dx - dvx_dz
        omega_z = dvx_dy - dvy_dx
        return omega_x, omega_y, omega_z

    def curvature(self, omega_x, omega_y, omega_z, spacing=1.0):
        # spacing: scalar or (dx, dy, dz)
        if np.isscalar(spacing):
            dx = dy = dz = float(spacing)
        else:
            dx, dy, dz = map(float, spacing)

        # Gradients of each vorticity component
        gox_dx, gox_dy, gox_dz = np.gradient(omega_x, dx, dy, dz, edge_order=2)
        goy_dx, goy_dy, goy_dz = np.gradient(omega_y, dx, dy, dz, edge_order=2)
        goz_dx, goz_dy, goz_dz = np.gradient(omega_z, dx, dy, dz, edge_order=2)

        grads = [
            (gox_dx, gox_dy, gox_dz),
            (goy_dx, goy_dy, goy_dz),
            (goz_dx, goz_dy, goz_dz),
        ]

        # R_ij = 0.5 * (∂i ω_j + ∂j ω_i)
        R = np.empty((3, 3) + omega_x.shape, dtype=omega_x.dtype)
        for i in range(3):
            for j in range(3):
                R[i, j] = 0.5 * (grads[j][i] + grads[i][j])
        return R



# ---------- CANDIDATE CLASS 6: SwirlGravityField (C++) ----------

class SwirlGravityField:
    """
    Compute g_i = - ω_j R_ij (Einstein summation form) from vorticity and curvature tensor.
    """

    def compute(
            self,
            omega: Tuple[np.ndarray, np.ndarray, np.ndarray],
            R: np.ndarray
    ) -> np.ndarray:
        ox, oy, oz = omega
        omega_vec = np.stack([ox, oy, oz], axis=0)  # (3, Nx,Ny,Nz)
        g = np.zeros_like(omega_vec)
        for i in range(3):
            acc = np.zeros_like(ox)
            for j in range(3):
                acc -= omega_vec[j] * R[i, j]
            g[i] = acc
        return g


# ---------- Orchestrators (Python API; C++ backends can drop-in) ----------

def field_on_grid_from_segments(
        X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
        seg_p0: np.ndarray, seg_t: np.ndarray, gamma: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute (Fx,Fy,Fz) on a rectilinear grid."""
    gp = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    V = BiotSavartGridEvaluator().evaluate(gp, seg_p0, seg_t, gamma)
    V = V.reshape(*X.shape, 3)
    return V[...,0], V[...,1], V[...,2]


def kinetic_energy_from_field(V: np.ndarray, rho: float) -> float:
    """Flattened V[N,3] → KE via VAMbinding."""
    return compute_kinetic_energy(np.ascontiguousarray(V, float).tolist(), float(rho))


# ---------- Example adapters (kept minimal) ----------

def example_three_phase_segments(
        corners=32, s_even=11, s_odd=-9, layers=10, dz=0.05
) -> Tuple[np.ndarray, np.ndarray]:
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    assembler = ThreePhaseCoilAssembler(corners, s_even, s_odd, layers, dz)
    return assembler.assemble(angles)


def example_trefoil_field(nvec: int = 9, L: float = 5.0, gamma: float = 1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    knot = VortexKnotSystem()
    knot.initialize_trefoil_knot()
    pos = np.asarray(knot.get_positions(), dtype=float)
    seg_p0, seg_t = arrows_from_positions(pos)
    x = np.linspace(-L, L, nvec); y = np.linspace(-L, L, nvec); z = np.linspace(-L, L, nvec)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    Fx, Fy, Fz = field_on_grid_from_segments(X, Y, Z, seg_p0, seg_t, gamma)
    return X, Y, Z, np.stack([Fx, Fy, Fz], axis=0)



# run_rodin_vam.py
# Reproduce your original pipeline using the VAMcore-friendly wrappers.
# Heavy math goes through vambindings now (C++); plotting/IO stays Python.



# ---------------------------
# 1) Geometric construction
# ---------------------------
coil_corners = 32
skip_forward = 11
skip_backward = -9
num_layers = 10
layer_spacing = 0.05

angles = np.linspace(0, 2*np.pi, coil_corners, endpoint=False) - np.pi/2

# Visualize 1‑phase path (matches your “Connected Coil Path”)
seq, _ = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward)
xs, ys, zs = [], [], []
for i in range(len(seq)):
    a = angles[(seq[i]-1) % coil_corners]
    xs.append(np.cos(a))
    ys.append(np.sin(a))
    zs.append(i * (3/(len(seq)-1)) - 1.5)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs, ys, zs, color='purple', lw=2, label="Connected Coil Path")
ax.set_title(f"1 layer of 1 phase\nDouble Starship coil\nN={coil_corners}, Skip=({skip_forward},{skip_backward})")
ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.5); ax.set_zlim(-1.5,1.5)
ax.legend()
plt.tight_layout()
plt.savefig("exports/coil_one_phase_path.png", dpi=150)

# 3‑phase geometry (like your second figure)
phase_offsets = (0.0, 2*np.pi/3, 4*np.pi/3)
cols = ['purple','blue','green']
fig = plt.figure(figsize=(10, 8)); ax = fig.add_subplot(111, projection='3d')
for c, off in zip(cols, phase_offsets):
    seq_o, _ = generate_alternating_skip_sequence(coil_corners, skip_forward, skip_backward, angle_offset=off)
    Xs, Ys, Zs = [], [], []
    for i in range(len(seq_o)):
        a = angles[(seq_o[i]-1) % coil_corners] + off
        Xs.append(np.cos(a)); Ys.append(np.sin(a))
        Zs.append(i * (3/(len(seq_o)-1)) - 1.5)
    ax.plot(Xs, Ys, Zs, color=c, lw=2)
ax.set_title(f"3‑Phase Double Star Coil\nN={coil_corners}, Skip=({skip_forward},{skip_backward})")
ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.5); ax.set_zlim(-1.5,1.5)
plt.tight_layout()
plt.savefig("exports/coil_three_phase_paths.png", dpi=150)

# -----------------------------------------------------
# 2) Build segments/tangents (ready for C++ replacement)
# -----------------------------------------------------
builder = SegmentTangentBuilder()
assembler = ThreePhaseCoilAssembler(coil_corners, skip_forward, skip_backward, num_layers, layer_spacing)
seg_p0_3p, seg_t_3p = assembler.assemble(angles)   # all three phases concatenated

# You can also build 1‑phase only if you want forward/backward coloring later:
seg_p0_1p, seg_t_1p = builder.build_phase(
    coil_corners, skip_forward, skip_backward, num_layers, layer_spacing, angle_offset=0.0, angles=angles
)

# -----------------------------------
# 3) Field on rectilinear 3D grid
# -----------------------------------
grid_dims = (21,21,21)
x = np.linspace(-1.0, 1.0, grid_dims[0])
y = np.linspace(-1.0, 1.0, grid_dims[1])
z = np.linspace(-1.0, 1.0, grid_dims[2])
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Biot–Savart field via evaluator (loops to C++ scalar for now; later → batch C++)
evaluator = BiotSavartGridEvaluator()
Fx, Fy, Fz = None, None, None
V = evaluator.evaluate(np.stack([X,Y,Z], axis=-1).reshape(-1,3), seg_p0_3p, seg_t_3p, gamma=1.0)
V = V.reshape(*X.shape, 3)
Fx, Fy, Fz = V[...,0], V[...,1], V[...,2]
Vmag = np.linalg.norm(V, axis=-1)

# Quiver slice (XY midplane) ~ your midplane plots
mid = grid_dims[2]//2
plt.figure(figsize=(8,6))
plt.quiver(X[:,:,mid], Y[:,:,mid], Fx[:,:,mid], Fy[:,:,mid], Vmag[:,:,mid], cmap='viridis')
plt.axis('equal'); plt.title("Biot–Savart Field (XY midplane, 3‑phase)")
plt.tight_layout(); plt.savefig("exports/field_xy_midplane_3phase.png", dpi=150)

# 3D quiver (subsample like your script)
density = 2
mask = np.zeros(X.shape, dtype=bool); mask[::density,::density,::density] = True
Xf, Yf, Zf = X[mask], Y[mask], Z[mask]
Vf = V[mask]; Vmagf = np.linalg.norm(Vf, axis=1)
cols = plt.cm.plasma((Vmagf - Vmagf.min())/(np.ptp(Vmagf)+1e-12))

fig = plt.figure(figsize=(10,8)); ax = fig.add_subplot(111, projection='3d')
ax.quiver(Xf, Yf, Zf, Vf[:,0], Vf[:,1], Vf[:,2], length=0.08, color=cols, normalize=True, linewidth=0.5, arrow_length_ratio=0.3)
ax.set_title("3D Biot–Savart Field (3‑phase, subsampled)"); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)
plt.tight_layout(); plt.savefig("exports/field_quiver3d_3phase.png", dpi=150)

# -----------------------------------------------------
# 4) Trefoil example (same outputs; already C++ inside)
# -----------------------------------------------------
plotGridsize = 5; n_vectors = 9
knot = VortexKnotSystem(); knot.initialize_trefoil_knot()
kpos = np.asarray(knot.get_positions(), float)
kseg_p0 = kpos[:-1]; kseg_t = np.diff(kpos, axis=0)
xv = np.linspace(-plotGridsize, plotGridsize, n_vectors)
yv = np.linspace(-plotGridsize, plotGridsize, n_vectors)
zv = np.linspace(-plotGridsize, plotGridsize, n_vectors)
Xg, Yg, Zg = np.meshgrid(xv, yv, zv, indexing='ij')
Vt = evaluator.evaluate(np.stack([Xg,Yg,Zg], axis=-1).reshape(-1,3), kseg_p0, kseg_t, gamma=1.0)
Vt = Vt.reshape(*Xg.shape, 3)
Vtmag = np.linalg.norm(Vt, axis=-1)

fig = plt.figure(figsize=(10,8)); ax = fig.add_subplot(111, projection='3d')
Xf2 = Xg[::2,::2,::2].ravel(); Yf2 = Yg[::2,::2,::2].ravel(); Zf2 = Zg[::2,::2,::2].ravel()
Vf2 = Vt[::2,::2,::2].reshape(-1,3); C2 = plt.cm.plasma(((np.linalg.norm(Vf2,axis=1))-Vf2[:,0].min())/(np.ptp(Vf2[:,0])+1e-9))
ax.quiver(Xf2, Yf2, Zf2, Vf2[:,0], Vf2[:,1], Vf2[:,2], length=0.4, normalize=True, color=C2, alpha=0.7)
ax.plot(kpos[:,0], kpos[:,1], kpos[:,2], color='red', lw=2)
ax.set_title("Trefoil Knot — Induced Velocity (VAM)"); ax.set_xlim(-plotGridsize,plotGridsize)
ax.set_ylim(-plotGridsize,plotGridsize); ax.set_zlim(-plotGridsize,plotGridsize)
plt.tight_layout(); plt.savefig("exports/trefoil_velocity.png", dpi=150)

# Kinetic energy (delegates to C++)
KE = compute_kinetic_energy(Vt.reshape(-1,3).tolist(), 7.0e-7)
print(f"Kinetic Energy (Trefoil): {KE:.3e} J")

# -----------------------------------------------------
# 5) Streamlines (field lines) with our integrator
# -----------------------------------------------------
integ = StreamlineIntegrator3D(X, Y, Z, Fx, Fy, Fz)
seed_points = [[sx, sy, 0.0] for sx in np.linspace(-0.8,0.8,5) for sy in np.linspace(-0.8,0.8,5)]

fig = plt.figure(figsize=(10,8)); ax = fig.add_subplot(111, projection='3d')
for s in seed_points:
    path = integ.integrate(np.array(s), ds=0.03, length=3.5)
    ax.plot(path[:,0], path[:,1], path[:,2], lw=1.5)
ax.set_title("Magnetic-like Field Lines (Streamlines)"); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)
plt.tight_layout(); plt.savefig("exports/streamlines.png", dpi=150)

# -----------------------------------------------------
# 6) Swirl tensor + “gravity” proxy (your ω and R_ij parts)
# -----------------------------------------------------
swirl = VorticityCurvatureTensor()
dx = float(x[1] - x[0])
dy = float(y[1] - y[0])
dz = float(z[1] - z[0])
omega_x, omega_y, omega_z = swirl.curl(Fx, Fy, Fz, spacing=(dx, dy, dz))
R = swirl.curvature(omega_x, omega_y, omega_z, spacing=(dx, dy, dz))
g_field = SwirlGravityField().compute((omega_x,omega_y,omega_z), R)  # shape (3,Nx,Ny,Nz)

# Quick look at g‑quiver, subsampled
gx, gy, gz = g_field
Gf = np.stack([gx,gy,gz], axis=-1)[mask]
Gmagf = np.linalg.norm(Gf, axis=1)
fig = plt.figure(figsize=(10,8)); ax = fig.add_subplot(111, projection='3d')
ax.quiver(Xf, Yf, Zf, Gf[:,0], Gf[:,1], Gf[:,2], length=0.07, normalize=True,
          color=plt.cm.coolwarm((Gmagf - Gmagf.min())/(np.ptp(Gmagf)+1e-12)), linewidth=0.5, arrow_length_ratio=0.3)
ax.set_title("Swirl‑Induced g proxy (ω & curvature)"); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)
plt.tight_layout(); plt.savefig("exports/swirl_gravity_proxy.png", dpi=150)

print("Done. Images in ./exports")
