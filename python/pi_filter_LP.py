import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

#=================================================================================================
# Prototype filter coefficients and Butterworth filter design approach based on:
# Steer, Michael. *Microwave and RF Design IV: Modules*, Section 2.7: "Butterworth and Chebyshev Filters".
# Retrieved from https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Electronics/Microwave_and_RF_Design_IV%3A_Modules_(Steer)/02%3A_Filters/2.07%3A_Butterworth_and_Chebyshev_Filters
# LibreTexts Engineering Library, accessed [2025-07-18].
#=================================================================================================

def butterworth_pi_components(fc, Z0):  # (2.7.1 Butterworth Filter)
    g1 = 1.4142  # 2nd Butterworth lowpass prototype filter coefficients
    g2 = 1.4142
    wc = 2 * np.pi * fc
    L = Z0 * g1 / wc
    C = g2 / (Z0 * wc)
    return L, C

fc = 10000
Z0 = 0.01   # System impedance (scales the impedance of all circuit elements in filter by same amount) (2.9.1 Impedance Transformation)

# Filter components
L, C = butterworth_pi_components(fc, Z0)

f = np.logspace(2, 6, 1000)  # 100 Hz to 1 MHz
omega = 2 * np.pi * f

# Transfer function
Z_L = 1j * omega * L
Z_C = 1 / (1j * omega * C)
Z_shunt = 1 / (1 / Z_C + 1 / Z_C)
Z_total = Z_L + Z_shunt
H = Z_shunt / Z_total


fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogx(f, 20 * np.log10(np.abs(H)), label="2nd-order Butterworth π-filter", color="orange")
ax.axvline(fc, color='red', linestyle='--', label=f"Cutoff ≈ {fc} Hz")
ax.set_title(f"Butterworth π-Filter Response (fc = {fc} Hz, Z0 = {Z0} Ω)")
ax.set_xlabel("Frequency")
ax.set_ylabel("Attenuation [dB]")
ax.grid(True, which="both", ls="--", lw=0.5)
ax.legend()

ax.set_xticks([1e2, 1e3, 1e4, 1e5, 1e6])
ax.get_xaxis().set_major_formatter(ScalarFormatter())
ax.set_xticklabels(['100Hz', '1KHz', '10KHz', '100KHz', '1MHz'])

plt.tight_layout()
plt.show()

#=================================================================================================

def pi_filter_cutoff(L_uH, C_uF):
    L = L_uH * 1e-6  # Convert µH to H
    C = C_uF * 1e-6  # Convert µF to F
    fc = 1 / (2 * np.pi * np.sqrt(L * C))
    return fc, L, C

# Filter components
L_uH = 1.4
C_uF = 470
fc, L, C = pi_filter_cutoff(L_uH, C_uF)

f = np.logspace(2, 6, 1000)  # 100 Hz to 1 MHz
omega = 2 * np.pi * f

# Transfer function
Z_L = 1j * omega * L
Z_C = 1 / (1j * omega * C)
Z_total = Z_L + Z_C
H = Z_C / Z_total


fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogx(f, 20 * np.log10(abs(H)), label="Attenuation")
ax.axvline(fc, color='red', linestyle='--', label=f"Cutoff ≈ {fc:.1f} Hz")
ax.set_title("π-Filter Attenuation")
ax.set_xlabel("Frequency")
ax.set_ylabel("Attenuation [dB]")
ax.grid(True, which="both", ls="--", lw=0.5)
ax.legend()

ax.set_xticks([1e2, 1e3, 1e4, 1e5, 1e6])
ax.get_xaxis().set_major_formatter(ScalarFormatter())
ax.set_xticklabels(['100Hz', '1KHz', '10KHz', '100KHz', '1MHz'])

plt.tight_layout()
plt.show()