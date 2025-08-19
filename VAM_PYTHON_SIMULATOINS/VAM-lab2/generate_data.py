# Generate two example NPZ datasets matching the requested structure
import numpy as np

def make_grid(Nx=48, Ny=48, Nz=24, dx=1e-3, dy=1e-3, dz=1e-3):
    x = (np.arange(Nx) - (Nx-1)/2.0) * dx
    y = (np.arange(Ny) - (Ny-1)/2.0) * dy
    z = (np.arange(Nz) - (Nz-1)/2.0) * dz
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    return X.astype(np.float32), Y.astype(np.float32), Z.astype(np.float32), dx, dy, dz

def vortex_column_omega(X, Y, Z, x0, y0, core=0.004, amp=120.0):
    # 2D Gaussian column oriented along +z (left-handed if amp>0, right-handed if amp<0)
    r2 = (X - x0)**2 + (Y - y0)**2
    omega_z = amp * np.exp(-r2 / (core**2))
    # Broadcast across z (column)
    omega = np.zeros(X.shape + (3,), dtype=np.float32)
    omega[..., 2] = omega_z.astype(np.float32)
    return omega

def save_vortex_dipole_dataset(fname="example_vortex_dipole_march.npz",
                               Nx=48, Ny=48, Nz=24, T=8,
                               dx=1e-3, dy=1e-3, dz=1e-3,
                               rho_scalar=6.97e-7):
    X, Y, Z, dx, dy, dz = make_grid(Nx, Ny, Nz, dx, dy, dz)

    # Static left/right components (columns along z)
    x0 = 0.010  # 1 cm offset left/right
    core = 0.004
    amp = 140.0  # s^-1
    omega_L = vortex_column_omega(X, Y, Z, -x0, 0.0, core=core, amp=+amp)  # left-handed (+z vorticity)
    omega_R = vortex_column_omega(X, Y, Z, +x0, 0.0, core=core, amp=-amp)  # right-handed (-z vorticity)

    # Time-resolved field: advect both columns in +y direction with a small drift per frame
    vt = 0.002  # m per timestep
    omega_t = np.zeros((T, Nx, Ny, Nz, 3), dtype=np.float32)
    for t in range(T):
        yshift = vt * t
        omega_L_t = vortex_column_omega(X, Y - yshift, Z, -x0, 0.0, core=core, amp=+amp)
        omega_R_t = vortex_column_omega(X, Y - yshift, Z, +x0, 0.0, core=core, amp=-amp)
        omega_t[t] = omega_L_t + omega_R_t

    np.savez_compressed(
        f"{fname}",
        omega=omega_t,
        omega_L=omega_L,
        omega_R=omega_R,
        rho=np.array(rho_scalar, dtype=np.float32),
        dx=np.array(dx, dtype=np.float32),
        dy=np.array(dy, dtype=np.float32),
        dz=np.array(dz, dtype=np.float32),
    )
    return f"{fname}", omega_t.shape, omega_L.shape

def abc_vector_field(X, Y, Z, A=1.0, B=1.0, C=1.0, k=2*np.pi/0.048):
    # ABC "Beltrami" field (normally used as velocity; here used as omega exemplar)
    # Components
    vx = A*np.sin(k*Z) + C*np.cos(k*Y)
    vy = B*np.sin(k*X) + A*np.cos(k*Z)
    vz = C*np.sin(k*Y) + B*np.cos(k*X)
    vec = np.stack([vx, vy, vz], axis=-1).astype(np.float32)
    return vec

def save_helical_abc_dataset(fname="example_helical_abc.npz",
                             Nx=48, Ny=48, Nz=24, T=8,
                             dx=1e-3, dy=1e-3, dz=1e-3,
                             rho_scalar=6.97e-7):
    X, Y, Z, dx, dy, dz = make_grid(Nx, Ny, Nz, dx, dy, dz)
    Lx = Nx*dx
    # Wave number k chosen to fit ~1 wavelength across domain in x (~0.048 m here for Nx*dx)
    k = 2*np.pi / max(Lx, 1e-6)

    # Left/Right components as ±ABC snapshots
    base = abc_vector_field(X, Y, Z, A=1.0, B=1.0, C=1.0, k=k)
    omega_L = (+1.0 * base).astype(np.float32)
    omega_R = (-1.0 * base).astype(np.float32)

    # Time series by phase-shifting Z (a traveling helical mode)
    omega_t = np.zeros((T, Nx, Ny, Nz, 3), dtype=np.float32)
    for t in range(T):
        phase = 2*np.pi * t / T
        shifted = abc_vector_field(X, Y, Z + phase/k, A=1.0, B=1.0, C=1.0, k=k)
        omega_t[t] = shifted

    np.savez_compressed(
        f"{fname}",
        omega=omega_t,
        omega_L=omega_L,
        omega_R=omega_R,
        rho=np.array(rho_scalar, dtype=np.float32),
        dx=np.array(dx, dtype=np.float32),
        dy=np.array(dy, dtype=np.float32),
        dz=np.array(dz, dtype=np.float32),
    )
    return f"{fname}", omega_t.shape, omega_L.shape

paths = [save_vortex_dipole_dataset(), save_helical_abc_dataset()]

print(paths)
