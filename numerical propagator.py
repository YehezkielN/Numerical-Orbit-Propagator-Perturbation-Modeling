import math
import numpy as np
GRAVITATIONAL_PARAMETER = 3.986004418e14
EARTH_RADIUS = 6378137.0
j2 = 1.08262668e-3
j3 = -2.53215306e-6
Omega_Earth = 7.2921150e-5
dt = 1
BALLISTIC_COEFF = 0.005
RHO_SURFACE = 1.225       
H  = 8500.0      

def compute_derivatives(state):
    px = state[0]
    py = state[1]
    pz = state[2]
    vx = state[3]
    vy = state[4]
    vz = state[5]
    #Calculate scalar distance (r) and scalar velocity (v) from center of the Earth
    sat_distance = (px**2 + py**2 + pz**2) **0.5
    sat_velocity = (vx**2 + vy**2 + vz**2) **0.5
    altitude = sat_distance - EARTH_RADIUS
    print("Altitude:", altitude, "m")
#Calculate primary two-body Keplerian gravitational acceleration
    acc_x = -(GRAVITATIONAL_PARAMETER * px) / sat_distance**3
    acc_y = -(GRAVITATIONAL_PARAMETER * py) / sat_distance**3
    acc_z = -(GRAVITATIONAL_PARAMETER * pz) / sat_distance**3
#Calculate J2 perturbation acceleration (Earth's equatorial bulge effect)
    a_j2x = - (1.5 * j2 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**2) / sat_distance **5) * px * (1-(5*pz**2 /sat_distance**2)))
    a_j2y = - (1.5 * j2 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**2) / sat_distance **5) * py * (1-(5*pz**2 /sat_distance**2)))
    a_j2z = - (1.5 * j2 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**2) / sat_distance **5) * pz * (3-(5*pz**2 /sat_distance**2)))
#Calculate J3 perturbation acceleration (Earth's pear-shaped asymmetric effect)
    a_j3x = - (0.5 * j3 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**3) / sat_distance **7) * px * (5*pz*(7*pz**2 / sat_distance**2 -3)))
    a_j3y = - (0.5 * j3 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**3) / sat_distance **7) * py * (5*pz*(7*pz**2 / sat_distance**2 -3)))
    a_j3z = - (0.5 * j3 * ((GRAVITATIONAL_PARAMETER * EARTH_RADIUS**3) / sat_distance **7) * (35 * pz**4 / sat_distance**2 - 30 * pz**2 + 3 * sat_distance**2))
    RHO_ATMOSPHERE = RHO_SURFACE * math.exp(-altitude/H)
#Calculate Atmospheric Drag
    a_drag_x = -0.5 * RHO_ATMOSPHERE * BALLISTIC_COEFF * sat_velocity * vx
    a_drag_y = -0.5 * RHO_ATMOSPHERE * BALLISTIC_COEFF * sat_velocity * vy
    a_drag_z = -0.5 * RHO_ATMOSPHERE * BALLISTIC_COEFF * sat_velocity * vz
 #Sum all acceleration components (Keplerian + J2 + J3 perturbations)
    a_total_x = acc_x + a_j2x + a_j3x + a_drag_x
    a_total_y = acc_y + a_j2y + a_j3y + a_drag_y
    a_total_z = acc_z + a_j2z + a_j3z + a_drag_z
    return np.array([vx, vy, vz, a_total_x, a_total_y, a_total_z])

satellite_name = input("Satellite Name: ")
position_x = float(input('position_x: '))
position_y = float(input("position_y: "))
position_z = float(input("position_z: "))
vel_x = float(input("vel_x: "))
vel_y = float(input("vel_y: "))
vel_z = float(input("vel_z: "))

history_time = []
history_latitude = []
history_longtitude = []
history_altitude = []

time = 0
print(f"Simulation started at t = {time} second")

while time < 5677:
#Calculate scalar distance (r) and scalar velocity (v) from center of the Earth
    sat_distance = (position_x**2 + position_y**2 + position_z**2) **0.5
    sat_velocity = (vel_x**2 + vel_y**2 + vel_z**2) **0.5
    altitude = sat_distance - EARTH_RADIUS
    print("Altitude:", altitude, "m")
    state = np.array([position_x, position_y, position_z, vel_x, vel_y, vel_z])
    k1 = compute_derivatives(state)
    k2 = compute_derivatives(state + (dt/2)*k1)
    k3 = compute_derivatives(state + (dt/2)*k2)
    k4 = compute_derivatives(state + (dt*k3))
    state_baru = state + (dt/6) *(k1 + 2*k2 + 2*k3 + k4)
    position_x = state_baru[0]
    position_y = state_baru[1]
    position_z = state_baru[2]
    vel_x = state_baru[3]
    vel_y = state_baru[4]
    vel_z = state_baru[5]
    # Print state baru (untuk debugging)
    print(f"\n Updated Velocity and Position State at Second-{time}: ")
    print(vel_x, "updated velocity x m/s")
    print(vel_y, "updated velocity y m/s")
    print(vel_z, "updated velocity z m/s")
    print(position_x, "updated position x m")
    print(position_y, "updated position y m")
    print(position_z, "updated position z m")
#Coordinate Transformation - Convert ECI (Inertial) to ECEF (Earth-Fixed) Frame
    print(f"\n Keterangan Posisi Terbaru detik ke-{time}: ")
    theta = Omega_Earth * time 
    Xecef = position_x * math.cos(theta) + position_y * math.sin(theta)
    Yecef = -position_x * math.sin(theta) + position_y * math.cos(theta)
    Zecef = position_z
    print(Xecef, "Earth-Centered, Earth-Fixed X-Coordinate", "m")
    print(Yecef, "Earth-Centered, Earth-Fixed Y-Coordinate", "m")
    print(Zecef, "Earth-Centered, Earth-Fixed Z-Coordinate", "m")
 # Geodetic Conversion - Calculate final Longitude and Latitude (Ground Track)
    Longtitude = math.atan2(Yecef, Xecef)
    longtitude_deg = math.degrees(Longtitude)
    P = (Xecef**2 + Yecef**2) **0.5
    latitude = math.atan2(Zecef, P)
    latitude_deg = math.degrees(latitude)
    print(f"\n Ground Track satellite detik ke-{time}: ")
    print(longtitude_deg, "Longitude", "°")
    print(latitude_deg, "Latitude", "°")

    history_time.append(time)
    history_latitude.append(latitude_deg)
    history_longtitude.append(longtitude_deg)
    history_altitude.append(altitude)
    time += 1

print("End of program.")

import matplotlib.pyplot as plt 
print("\n=== POST SIMULATION VISUALITATION ===")

# --- FIGURE 1: ORBIT DECAY ANALYSIS ---
plt.figure(figsize=(10, 5))
plt.plot(history_time, history_altitude, color='red', linewidth=2)
plt.title(f"Altitude Variation per Orbit - {satellite_name}")
plt.xlabel("Time (second)")
plt.ylabel("Altitude (meter)")
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.grid(True)

# --- FIGURE 2: GROUND TRACK CLEANED (Anti-Garis Siluman) ---
# Membuat list baru untuk memutus garis saat terjadi lompatan bujur ekstrem
clean_longtitude = []
clean_latitude = []

for i in range(len(history_longtitude)):
    if i > 0:
        # Jika bujur melompat ekstrem (misal lebih dari 100 derajat dalam 1 detik)
        if abs(history_longtitude[i] - history_longtitude[i-1]) > 100:
            # Sisipkan None untuk memutus garis penghubung matplotlib
            clean_longtitude.append(None)
            clean_latitude.append(None)
            
    clean_longtitude.append(history_longtitude[i])
    clean_latitude.append(history_latitude[i])

plt.figure(figsize=(10, 6))
# Plot menggunakan data yang sudah dibersihkan
plt.plot(clean_longtitude, clean_latitude, color='blue', marker='o', linestyle='-', linewidth=1.5, markersize=3)
plt.title(f"Ground Track Satellite (Cleaned) - {satellite_name}")
plt.xlabel("Longitude (degree)")
plt.ylabel("Latitude (degree)")

# Mengunci batas proyeksi peta silinder normal (-180 sampai 180, -90 sampai 90)
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.grid(True)

plt.show()
