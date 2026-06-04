# 🛰️ Numerical Orbit Propagator & Perturbation Modeling

A numerical orbit propagator for Low Earth Orbit (LEO) satellites, implementing full gravitational perturbation modeling and 4th-order Runge-Kutta (RK4) numerical integration — built from scratch in Python.

Developed as **Project #1** of an ongoing astrodynamics research portfolio, with direct application to Indonesia's **NEO-1 satellite constellation** developed by BRIN (National Research and Innovation Agency).

---

## 📋 Features

- ✅ Two-body Keplerian gravitational acceleration
- ✅ J2 perturbation — Earth's equatorial oblateness
- ✅ J3 perturbation — Earth's pear-shaped asymmetry
- ✅ Atmospheric drag with exponential density model
- ✅ 4th-order Runge-Kutta (RK4) numerical integrator
- ✅ ECI → ECEF coordinate transformation
- ✅ Geodetic conversion (Lat/Lon/Altitude)
- ✅ Ground track visualization
- ✅ Altitude variation per orbit plot

---

## 🔭 Validated Satellites

| Satellite | Altitude | Inclination | Orbit Type |
|-----------|----------|-------------|------------|
| GRACE-FO  | 500 km   | 89.0°       | Near-Polar |
| LAPAN-A2  | 630 km   | 97.8°       | Sun-Synchronous (SSO) |
| NEO-1 (BRIN) | 500 km | 97.4°    | Sun-Synchronous (SSO) |

---

## 📊 Sample Results

### GRACE-FO — Near-Polar Orbit (89°)
| Output | Description |
|--------|-------------|
| Altitude Variation | Perigee ~490,000 m / Apogee ~500,000 m |
| Ground Track | Reaches ±87° latitude (near-polar coverage) |

### LAPAN-A2 — Sun-Synchronous Orbit (97.8°)
| Output | Description |
|--------|-------------|
| Altitude Variation | Perigee ~614,000 m / Apogee ~630,000 m |
| Ground Track | Retrograde SSO pattern, ±80° latitude coverage |

### NEO-1 (BRIN) — Sun-Synchronous Orbit (97.4°)
| Output | Description |
|--------|-------------|
| Altitude Variation | Perigee ~492,000 m / Apogee ~500,000 m |
| Ground Track | SSO pattern with J2/J3 secondary perturbation visible |

---

## ⚙️ Physical Model

### Constants
```python
GRAVITATIONAL_PARAMETER = 3.986004418e14  # m³/s²
EARTH_RADIUS            = 6378137.0       # m
J2                      = 1.08262668e-3
J3                      = -2.53215306e-6
OMEGA_EARTH             = 7.2921150e-5    # rad/s
RHO_SURFACE             = 1.225           # kg/m³
H_SCALE                 = 8500.0          # m (scale height)
```

### Equations of Motion
```
Total Acceleration = a_gravity + a_J2 + a_J3 + a_drag

a_gravity = -(GM / r³) × r_vec          (Keplerian)
a_J2      = f(GM, Re, J2, r, z)         (Oblateness)
a_J3      = f(GM, Re, J3, r, z)         (Asymmetry)
a_drag    = -½ × ρ(h) × Cd(A/m) × v²   (Atmospheric drag)
ρ(h)      = ρ₀ × exp(-h / H)           (Exponential atmosphere)
```

### Numerical Integration — RK4
```
k1 = f(state)
k2 = f(state + dt/2 × k1)
k3 = f(state + dt/2 × k2)
k4 = f(state + dt   × k3)

state_new = state + (dt/6) × (k1 + 2k2 + 2k3 + k4)
```

---

## 🚀 Getting Started

### Requirements
```bash
pip install numpy matplotlib
```

### Run
```bash
python orbit_propagator.py
```

### Input Parameters
```
Satellite Name : e.g. NEO-1
position_x     : X coordinate in ECI frame [m]
position_y     : Y coordinate in ECI frame [m]
position_z     : Z coordinate in ECI frame [m]
vel_x          : Velocity X component [m/s]
vel_y          : Velocity Y component [m/s]
vel_z          : Velocity Z component [m/s]
```

### Example Input — NEO-1 (BRIN)
```
Satellite Name : NEO-1
position_x     : 6878137.0
position_y     : 0.0
position_z     : 0.0
vel_x          : 0.0
vel_y          : -980.4
vel_z          : 7549.0
```

---

## 📁 Repository Structure

```
orbit-propagator/
│
├── orbit_propagator.py      ← Main script
├── README.md                ← This file
└── results/
    ├── GRACE-FO_altitude.png
    ├── GRACE-FO_groundtrack.png
    ├── LAPAN-A2_altitude.png
    ├── LAPAN-A2_groundtrack.png
    ├── NEO-1_altitude.png
    └── NEO-1_groundtrack.png
```

---

## 🗺️ Roadmap

This project is **Part 1** of an integrated Precision Orbit Determination (POD) pipeline:

```
✅ Project 1 — Numerical Orbit Propagator & Perturbation Modeling
🔄 Project 2 — High-Precision Orbit Determination via Least Squares
⏳ Project 3 — Constellation Design & Ground Track Coverage
⏳ Project 4 — Satellite Altimetry Waveform Processing
⏳ Project 5 — Global Gravity Field Modeling
```

Projects 1 + 2 together form a complete **POD pipeline** directly applicable to BRIN's NEO-1 satellite constellation development.

---

## 🌏 Application Context

This propagator was developed with direct relevance to **Indonesia's national satellite program**:

- **NEO-1 (Nusantara Earth Observation-1)** — BRIN's upcoming Earth observation satellite, planned for launch in 2027 on a 500 km SSO
- **NEO Constellation** — 8-satellite constellation (2 VHSR + 4 HSR + 2 SAR) under development by BRIN

Accurate orbit propagation and perturbation modeling are essential for mission planning, ground station contact scheduling, and precision orbit determination post-launch.

---

## 📚 References

- Vallado, D.A. (2013). *Fundamentals of Astrodynamics and Applications*, 4th ed.
- Montenbruck, O. & Gill, E. (2000). *Satellite Orbits: Models, Methods and Applications*
- NRLMSISE-00 Atmosphere Model
- NORAD Two-Line Element (TLE) Format Documentation

---

## 👤 Author

**Geomatics Engineering — UPN Veteran Yogyakarta**
Undergraduate Thesis: *Ocean Heat Content Identification via Sea Surface Height Distribution in the Banda Sea Using Sentinel-6 Along Track*

---

## 📄 License

MIT License — free to use with attribution.