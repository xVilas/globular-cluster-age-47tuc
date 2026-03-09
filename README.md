# Globular Cluster Age Estimation with Gaia DR3

Estimation of the age and metallicity of the globular cluster **47 Tucanae (NGC 104)** using real photometric and astrometric data from the Gaia DR3 catalogue, isochrone fitting with PARSEC models, and quality filtering based on proper motion membership selection.

**Result:** 13.5 Gyr, [M/H] = −0.6 — consistent with current literature values.

> **⚠️ Note (March 2025):** The PARSEC isochrone server (`stev.oapd.inaf.it`) is currently returning empty responses. Sections 6 and 7 of `main.py` will fail at runtime. See [Known issues](#known-issues) for details and the required fix.

---

## Project Structure

```
globular-cluster-age/
│
├── data/
│   ├── raw/                        # Original Gaia DR3 query output
│   │   └── original_stellar_data.csv
│   └── processed/                  # Cleaned data ready for analysis
│       └── clean_data.csv
│
├── modules/
│   ├── __init__.py
│   ├── calculations.py             # Coordinate and distance conversions
│   └── data_cleaner.py             # Quality filtering pipeline
│
├── plots/
│   └── isochrones/                 # Output figures (PDF)
│
├── config.py                       # Centralised parameters
├── main.py                         # Main analysis script
├── requirements.txt
└── README.md
```

---

## Method

### 1. Data acquisition

Stars were queried from the Gaia DR3 catalogue (`gaiadr3.gaia_source`) using ADQL, selecting sources in the sky region of 47 Tuc with a parallax range consistent with its known distance (~4 kpc):

```sql
SELECT ra, dec, parallax, pmra, pmdec, pmra_error, pmdec_error, radial_velocity,
       phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, bp_rp,
       phot_bp_rp_excess_factor, phot_bp_mean_flux_over_error,
       phot_rp_mean_flux_over_error, astrometric_excess_noise
FROM gaiadr3.gaia_source
WHERE parallax BETWEEN 0.202 AND 0.262
  AND ra BETWEEN 5 AND 7
  AND dec BETWEEN -74 AND -70
```

### 2. Quality filtering

Photometric and astrometric quality cuts are applied to remove unreliable sources:

| Filter | Condition |
|--------|-----------|
| Astrometric excess noise | < 1 |
| BP flux / error | > 10 |
| RP flux / error | > 10 |
| BP/RP excess factor | < 2.5 |

### 3. Membership selection

Cluster members are selected by filtering stars within a circular region of radius r = 1 mas/yr around the median proper motion of the sample in the (μ_α*, μ_δ) plane. This removes foreground and background field stars.

### 4. Extinction correction

Interstellar reddening is corrected using E(B−V) = 0.03 (literature value for 47 Tuc) with Gaia EDR3 extinction coefficients:

- A_G = 0.859 × E(B−V)
- A_BP = 1.068 × E(B−V)  
- A_RP = 0.652 × E(B−V)

### 5. Isochrone fitting

PARSEC isochrones are retrieved via `ezpadova` for a grid of ages (10–14 Gyr) and metallicities ([M/H] = −0.9 to −0.4) in the Gaia EDR3 photometric system. The best-fit isochrone is selected by visual comparison on the dereddened colour-magnitude diagram (CMD).

**Best fit: 13.5 Gyr, [M/H] = −0.6**

---

## Results

The dereddened CMD of 47 Tuc with the best-fit PARSEC isochrone:

- Age: **13.5 Gyr**
- Metallicity: **[M/H] = −0.6**
- Distance modulus: **13.21 mag** (~4.4 kpc)
- Reddening: **E(B−V) = 0.03**

---

## Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

```
pandas
numpy
matplotlib
ezpadova
astropy
```

---

## Usage

1. Place the raw Gaia query output in `data/raw/original_stellar_data.csv`
2. Run the cleaning pipeline:
```bash
python -m modules.data_cleaner
```
3. Run the main analysis:
```bash
python -X utf8 main.py
```

---

## Known issues

**PARSEC server unavailable (as of March 2025)**

The PARSEC isochrone server (`stev.oapd.inaf.it`) appears to be returning empty responses as of March 2025, causing sections 6 and 7 to fail at runtime. The pre-generated PDFs in `plots/isochrones/` were produced when the server was operational. Check server status before running.

**ezpadova 2.0 — `IndexError: string index out of range`**

ezpadova 2.0 crashes when the PARSEC server returns a response containing empty lines. Apply the following one-line fix in `venv/Lib/site-packages/ezpadova/parsec.py` (line 84):

```python
# Before
if line[0] != comment:

# After
if line and line[0] != comment:
```

---

## Data source

European Space Agency (ESA), *Gaia* mission, Data Release 3.  
Catalogue: `gaiadr3.gaia_source`, queried via the [Gaia Archive](https://gea.esac.esa.int/archive/).

PARSEC isochrones retrieved via [ezpadova](https://github.com/mfouesneau/ezpadova) (Bressan et al. 2012).

---

## Acknowledgements

This project is based on coursework from the *Extragalactic Astrophysics* module of the MSc in Astrophysics at the Universidad de La Laguna, taught by Prof. Jairo Méndez Abreu. Special thanks to him for the guidance and inspiration.

---

## Author

**Xoán Vilas Currás**  
MSc in Astrophysics, Universidad de La Laguna  
[github.com/xvilas](https://github.com/xvilas)
