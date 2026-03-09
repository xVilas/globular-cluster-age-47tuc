import pandas as pd
from config import (
    RAW_DATA_PATH,
    CLEAN_DATA_PATH,
    MAX_ASTROMETRIC_EXCESS_NOISE,
    MIN_BP_FLUX_OVER_ERROR,
    MIN_RP_FLUX_OVER_ERROR,
    MAX_BP_RP_EXCESS_FACTOR,
)

# --- Load raw data ---
Tuc47_raw = pd.read_csv(RAW_DATA_PATH)
Tuc47_dirty = Tuc47_raw.copy()

# --- Cast columns to float ---
cols_to_cast = [
    "ra",
    "dec",
    "parallax",
    "pmra",
    "pmdec",
    "pmra_error",
    "pmdec_error",
    "radial_velocity",
    "phot_g_mean_mag",
    "phot_bp_mean_mag",
    "phot_rp_mean_mag",
    "bp_rp",
    "phot_bp_rp_excess_factor",
    "phot_bp_mean_flux_over_error",
    "phot_rp_mean_flux_over_error",
    "astrometric_excess_noise",
]

Tuc47_dirty[cols_to_cast] = Tuc47_dirty[cols_to_cast].astype(float)

# --- Diagnostics ---
print("AVG phot_bp_mean_flux_over_error:", Tuc47_dirty["phot_bp_mean_flux_over_error"].mean())
print("AVG phot_rp_mean_flux_over_error:", Tuc47_dirty["phot_rp_mean_flux_over_error"].mean())
print("AVG astrometric_excess_noise:    ", Tuc47_dirty["astrometric_excess_noise"].mean())
print("AVG phot_bp_rp_excess_factor:    ", Tuc47_dirty["phot_bp_rp_excess_factor"].mean())

# --- Quality filtering ---
Tuc47_clean = Tuc47_dirty[
    (Tuc47_dirty["astrometric_excess_noise"]      < MAX_ASTROMETRIC_EXCESS_NOISE)
    & (Tuc47_dirty["phot_bp_mean_flux_over_error"] > MIN_BP_FLUX_OVER_ERROR)
    & (Tuc47_dirty["phot_rp_mean_flux_over_error"] > MIN_RP_FLUX_OVER_ERROR)
    & (Tuc47_dirty["phot_bp_rp_excess_factor"]     < MAX_BP_RP_EXCESS_FACTOR)
].copy()

print(f"\nStars before filtering: {len(Tuc47_dirty)}")
print(f"Stars after filtering:  {len(Tuc47_clean)}")

# --- Drop quality columns no longer needed ---
cols_to_drop = [
    "phot_rp_mean_flux_over_error",
    "phot_bp_mean_flux_over_error",
    "astrometric_excess_noise",
    "phot_bp_rp_excess_factor",
]

Tuc47_clean.drop(columns=cols_to_drop, inplace=True)

# --- Save ---
Tuc47_clean.to_csv(CLEAN_DATA_PATH, index=False)
print(f"\nClean data saved to {CLEAN_DATA_PATH}")
