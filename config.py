# =============================================================================
# config.py — Centralised parameters for 47 Tucanae analysis
# =============================================================================

# --- Cluster identity ---
CLUSTER_NAME = "47 Tucanae (NGC 104)"

# --- Gaia query region ---
PARALLAX_MIN = 0.202  # mas
PARALLAX_MAX = 0.262  # mas
RA_MIN = 5.0  # deg
RA_MAX = 7.0  # deg
DEC_MIN = -74.0  # deg
DEC_MAX = -70.0  # deg

# --- Data paths ---
RAW_DATA_PATH = "data/raw/original_stellar_data.csv"
CLEAN_DATA_PATH = "data/processed/clean_data.csv"

# --- Quality filtering thresholds ---
MAX_ASTROMETRIC_EXCESS_NOISE = 1.0
MIN_BP_FLUX_OVER_ERROR = 10.0
MIN_RP_FLUX_OVER_ERROR = 10.0
MAX_BP_RP_EXCESS_FACTOR = 2.5

# --- Proper motion membership ---
PM_RADIUS = 1.0  # mas/yr — radius around median proper motion

# --- Extinction (Schlegel/Schlafly, Gaia EDR3 coefficients) ---
E_BV = 0.03
A_G = 0.85926 * E_BV
A_BP = 1.06794 * E_BV
A_RP = 0.65199 * E_BV

# --- Distance ---
DISTANCE_MODULUS = 13.21  # mag

# --- Isochrone grid ---
AGES_GYR = [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0]  # Gyr
MHS_1 = [-0.8, -0.6, -0.4]
MHS_2 = [-0.9, -0.7, -0.5]
PHOTSYS = "gaiaEDR3"

# --- Best fit result ---
BEST_AGE_GYR = 13.5  # Gyr
BEST_MH = -0.6
