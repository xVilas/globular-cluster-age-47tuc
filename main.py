import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import ezpadova
import time

from modules import calculations
from config import (
    CLEAN_DATA_PATH,
    PM_RADIUS,
    E_BV,
    A_G,
    A_BP,
    A_RP,
    DISTANCE_MODULUS,
    AGES_GYR,
    MHS_1,
    MHS_2,
    PHOTSYS,
    BEST_AGE_GYR,
    BEST_MH,
)

# =============================================================================
# 1. Load data
# =============================================================================

df = pd.read_csv(CLEAN_DATA_PATH)

ra = df["ra"].to_numpy()
dec = df["dec"].to_numpy()
parallax = df["parallax"].to_numpy()
pmra = df["pmra"].to_numpy()
pmdec = df["pmdec"].to_numpy()
pmra_error = df["pmra_error"].to_numpy()
pmdec_error = df["pmdec_error"].to_numpy()
phot_g = df["phot_g_mean_mag"].to_numpy()
phot_bp = df["phot_bp_mean_mag"].to_numpy()
phot_rp = df["phot_rp_mean_mag"].to_numpy()
bp_rp = df["bp_rp"].to_numpy()

# =============================================================================
# 2. Coordinate calculations
# =============================================================================

distance = calculations.parallax_to_parsecs(parallax)
ra_rad = calculations.degrees_to_radians(ra)
dec_rad = calculations.degrees_to_radians(dec)
x, y, z = calculations.cartesian_coordinates(distance, ra_rad, dec_rad)

# =============================================================================
# 3. Proper motion membership selection
# =============================================================================

x_c = np.median(pmra)
y_c = np.median(pmdec)
mask = (pmra - x_c) ** 2 + (pmdec - y_c) ** 2 <= PM_RADIUS**2

print(f"Stars selected as cluster members: {mask.sum()} / {len(mask)}")

# --- Proper motion diagram ---
plt.figure(figsize=(6, 6))
plt.scatter(pmra, pmdec, color="red", s=2, alpha=0.4, label="All stars")
plt.scatter(pmra[mask], pmdec[mask], color="black", s=2, label="Members")
plt.xlabel("pmra (mas/yr)")
plt.ylabel("pmdec (mas/yr)")
plt.title("Proper motion diagram — 47 Tuc")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================================================
# 4. Colour-magnitude diagram (observed)
# =============================================================================

g_abs = df["phot_g_mean_mag"] + 5 * np.log10(parallax) - 10

plt.figure(figsize=(6, 6))
plt.scatter(bp_rp, g_abs, s=2, alpha=0.3, color="grey", label="All stars")
plt.scatter(bp_rp[mask], g_abs[mask], s=2, alpha=0.6, color="blue", label="Members")
plt.gca().invert_yaxis()
plt.xlabel("BP − RP")
plt.ylabel("G (abs)")
plt.title("CMD — 47 Tuc (observed)")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================================================
# 5. Extinction correction
# =============================================================================

bp_rp_0 = (phot_bp - phot_rp) - (A_BP - A_RP)  # intrinsic colour
g_0 = phot_g - A_G  # intrinsic G magnitude

# =============================================================================
# 6. Isochrone grid — age and metallicity exploration
# =============================================================================

logages = [np.log10(age * 1e9) for age in AGES_GYR]

base_cmap = cm.Reds
dark_reds = colors.LinearSegmentedColormap.from_list(
    "dark_reds", base_cmap(np.linspace(0.4, 0.9, 256))
)


start = time.perf_counter()

for logage, age_gyr in zip(logages, AGES_GYR):
    for mhs, suffix in [(MHS_1, "1"), (MHS_2, "2")]:
        norm = colors.Normalize(vmin=min(mhs), vmax=max(mhs))
        fig, ax = plt.subplots(figsize=(6, 6))

        ax.scatter(bp_rp[mask], g_abs[mask], s=2, color="blue", alpha=0.5, zorder=1)

        for mh in mhs:
            iso = ezpadova.get_isochrones(
                logage=(logage, logage, 0), MH=(mh, mh, 0), photsys_file=PHOTSYS
            )
            iso["BP_RP_0"] = iso["G_BPmag"] - iso["G_RPmag"]
            iso["G_0"] = iso["Gmag"]

            ax.scatter(
                iso["BP_RP_0"],
                iso["G_0"],
                s=0.9,
                color=dark_reds(norm(mh)),
                alpha=0.75,
                label=f"[M/H] = {mh}",
                zorder=2,
            )

        ax.set_xlabel("BP − RP")
        ax.set_ylabel("G")
        ax.set_xlim(0, 3)
        ax.set_ylim(9, -3)
        ax.set_title(f"Isochrones — {age_gyr:.1f} Gyr")
        ax.legend()
        fig.savefig(f"plots/isochrones/isochrones_{age_gyr:.1f}Gyr_{suffix}.pdf")
        plt.close(fig)

end = time.perf_counter()
print(f"Isochrone grid completed in {end - start:.2f} s")

# =============================================================================
# 7. Best-fit CMD (dereddened)
# =============================================================================

logage_best = np.log10(BEST_AGE_GYR * 1e9)

iso_best = ezpadova.get_isochrones(
    logage=(logage_best, logage_best, 0),
    MH=(BEST_MH, BEST_MH, 0),
    photsys_file=PHOTSYS,
)

iso_best["BP_RP_0"] = iso_best["G_BPmag"] - iso_best["G_RPmag"]
iso_best["G_0"] = iso_best["Gmag"]

plt.figure(figsize=(6, 6))
plt.scatter(
    bp_rp_0[mask],
    g_0[mask] - DISTANCE_MODULUS,
    s=2,
    color="blue",
    alpha=0.5,
    label="47 Tuc (dereddened)",
)
plt.scatter(
    iso_best["BP_RP_0"],
    iso_best["G_0"],
    s=1,
    color="red",
    label=f"PARSEC {BEST_AGE_GYR} Gyr, [M/H] = {BEST_MH}",
)
plt.xlabel("(BP − RP)₀")
plt.ylabel("G₀")
plt.title(f"Best-fit CMD — {BEST_AGE_GYR} Gyr, [M/H] = {BEST_MH}")
plt.xlim(0, 3)
plt.ylim(9, -3)
plt.legend()
plt.tight_layout()
plt.show()
