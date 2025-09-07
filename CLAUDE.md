# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a board-ready market analysis and dealer network optimization project for Gazelle/Pon Bike Netherlands. The project was designed as a 2nd round interview case for a Data Scientist position. It analyzes dealer coverage, identifies white spots (underserved areas), provides strategic recommendations, and answers three key business questions with data-driven insights including CSR/policy considerations.

## Case Requirements & Deliverables

### Core Questions to Answer:
1. **Regional Analysis**: In welke regio's zijn we te veel, goed, of juist weinig aanwezig? ✅ ANSWERED
2. **International Strategy**: Urban Arrow expansion advise for comparable countries ✅ ANSWERED  
3. **Portfolio Strategy**: Should Pon stop/add brands (with CSR/political considerations)? ✅ ANSWERED

### Required Deliverables:
- **Slide deck** (max 15 min presentation)
- **Working notebooks/scripts** with data prep, analysis, and visualizations
- **Interactive dashboard** with region and brand filters
- **README** with assumptions, limitations, and data quality notes

## Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit dashboard
streamlit run app/streamlit_app.py
```

### Data Processing Pipeline (Critical Path)
```bash
# MUST run in sequence - contains all core analysis
jupyter notebook notebooks/01_dataprep.ipynb      # ✅ COMPLETED - Data cleaning & geographic mapping 
jupyter notebook notebooks/02_coverage.ipynb      # ✅ COMPLETED - White spots & proximity analysis  
jupyter notebook notebooks/03_kpis_viz.ipynb      # ✅ COMPLETED - KPIs & visualization for slides
jupyter notebook notebooks/04_enrichment.ipynb    # ✅ COMPLETED - ZE-zones & cargo bike analysis
jupyter notebook notebooks/05_intl_shortlist.ipynb # ✅ COMPLETED - International expansion analysis
jupyter notebook notebooks/06_portfolio_advies.ipynb # ✅ COMPLETED - Brand portfolio strategy

# Non-interactive execution (preferred for CI/local runs)
jupyter nbconvert --to notebook --execute notebooks/01_dataprep.ipynb --inplace  # ✅ WORKS
jupyter nbconvert --to notebook --execute notebooks/02_coverage.ipynb --inplace  # ✅ WORKS  
jupyter nbconvert --to notebook --execute notebooks/03_kpis_viz.ipynb --inplace  # ✅ WORKS
jupyter nbconvert --to notebook --execute notebooks/04_enrichment.ipynb --inplace # ✅ WORKS
jupyter nbconvert --to notebook --execute notebooks/05_intl_shortlist.ipynb --inplace # ✅ WORKS
jupyter nbconvert --to notebook --execute notebooks/06_portfolio_advies.ipynb --inplace # ✅ WORKS

# Build policy index for ZE-zones
python src/build_policy_index.py

# Optional: fetch external data updates
python src/fetch_external.py
```

### Testing & Validation
```bash
# Validate data quality
python src/validate_data.py

# Run dashboard locally
streamlit run app/streamlit_app.py --server.port 8501
```

## Architecture & Key Components

### Data Flow & Critical Issues

#### 1. **Raw Data** (`data/raw/`):
   - `dealer_lijst.csv`: 6,749 bike shops with brands, locations, ratings (Pon + competitors)
   - `demografie.csv`: 4,073 CBS demographics per postal code (-99997 = missing/confidential)

#### 2. **External Data** (`data/external/`):
   - `Woonplaatsen_in_Nederland_2024_*.csv`: **CRITICAL** - 2,507 places→municipality→province mapping
   - `ze_steden.csv`: 29 zero-emission zones with start dates (2025-2028)
   - `pc4_gemeente.csv`: **WARNING** - appears empty, use woonplaatsen data instead

#### 3. **Processing Pipeline** (`notebooks/`):
   - `01_dataprep.ipynb`: **PRIORITY** - Geographic mapping, brand normalization, dealer deduplication
   - `02_coverage.ipynb`: Coverage calculation, white spot identification, proximity analysis
   - `03_kpis_viz.ipynb`: Board presentation KPIs and visualizations
   - `04_enrichment.ipynb`: Demographics integration (income, households, age)
   - `05_intl_shortlist.ipynb`: International expansion analysis

### Core Metrics & Calculations

#### Geographic Hierarchy:
```python
# Use woonplaatsen data for geographic aggregation:
Woonplaats → Gemeente → Provincie → Landsdeel (Noord/Oost/West/Zuid)
```

#### Key KPIs:
- **Coverage**: % population within radius R of a Pon dealer
- **White spots**: Areas >R km from any Pon dealer (prioritized by population)
- **Dealers per 100k**: Density metric by region (benchmark: NL average)
- **Pon-share**: % Pon dealers vs total dealers per region
- **Proximity metrics**: Co-location analysis (cannibalization risk)
- **Policy integration**: ZE-zone weighting for urban priority

#### Brand-Specific Analysis:
- **Pon brands**: Gazelle, Cannondale, Union, Kalkhoff, Urban Arrow, Cervélo, Focus, Santa Cruz
- **Performance metrics**: dealers × avg_rating × log(1+reviews) per brand
- **Cannibalization matrix**: % dealers selling multiple Pon brands
- **Demographic fit**: brand suitability per region (income, age, family composition)

### Technical Implementation Details

#### Data Cleaning & Normalization:
```python
# CBS demografie handling:
df.replace(-99997, np.nan)  # Missing/confidential values
df['brand_clean'] = df['brand'].str.lower().str.strip()
df['is_pon'] = df['brand_clean'].isin(PON_BRANDS)

# Geographic mapping (CRITICAL):
# Use woonplaatsen file for plaats→gemeente→provincie mapping
# Link dealers via city/address parsing
```

#### Coverage Calculation:
- **Distance method**: Haversine (great-circle) - NOT travel time
- **Brand-specific radius**: UA: 5-7.5km, Gazelle: 7.5-10km, Sport: 10-15km
- **Urban adjustment**: Dense areas -2.5km, rural areas +2.5km from base radius

#### White Spot Scoring:
```python
# Multi-criteria scoring with policy weighting:
S_base = 0.3*z(population) + 0.25*z(distance_to_pon) - 0.2*z(competitor_density) + 0.25*z(market_gap)
S_policy = S_base * (1 + 0.5*policy_index + 0.3*urban_density_index)
S_final = S_policy * cannibalization_factor(nearby_pon_dealers)
```

Additional implemented variant in notebooks:

- Demography-augmented score S_dem used for ranking white-spots:
  - S_dem = S_policy
    + 0.4·z(kids_0_15_pct)
    + 0.4·z(age_25_44_pct)
    − 0.2·z(hh_1p_pct)
  - Weights are simple defaults and can be tuned per merk.

### Dashboard Features (`app/streamlit_app.py`)
Interactive Streamlit app with:
- **Map**: Folium markers for dealers (Pon vs non‑Pon colorized)
- **Filters**: Brand selection (Pon‑merken), radius slider, ZE‑steden toggle
- **White‑spots tabel**: reads `outputs/tables/white_spots_with_policy.csv` (fallback `white_spots_ranked.csv`), optional join with policy
- (Optional) Choropleth/KPI table can be added if exports exist

### Output Structure
- `outputs/tables/`: 
  - `coverage_overall.csv`: Coverage percentages for multiple radii
  - `white_spots_ranked.csv` / `white_spots_with_policy.csv`: Ranked white‑spots (policy/demography aware)
  - `kpi_overview.csv`: Dealers/100k, Pon‑share per gemeente
  - `white_spots_top10_gemeenten.csv`: Top‑10 onderbediend gemeenten
  - `brand_counts_top20.csv`: Brand counts/overview (portfolio view)
  - `proximity_kpis.csv` and `proximity_summary.csv`: proximity/cannibalisatie metrics
  - `ua_intl_shortlist.csv`: UA city shortlist with dealer targets
- `outputs/figures/`: Board-ready visualizations (PNG/SVG)
- `data/processed/`: Clean datasets for dashboard

### Competitor Definition
- We derive competitors directly from `dealer_lijst.csv` without scraping:
  - `brand_clean = brand.lower().strip()`
  - `is_pon_dealer = brand_clean in {gazelle,cannondale,union,kalkhoff,urban_arrow,cervélo,cervelo,focus,santa_cruz}`
  - Non‑Pon dealers (`is_pon_dealer == False`) are treated as competitors in share and proximity metrics.

## Critical Data Issues & Solutions

### 1. Geographic Mapping
**Problem**: Original `pc4_gemeente.csv` appears incomplete
**Solution**: Use `Woonplaatsen_in_Nederland_2024_*.csv` with 2,507 places→municipality mapping

### 2. Demographics Integration
**Issue**: Rich CBS data (income, households, age) not fully utilized in original plan
**Fix**: Implement demographic scoring for brand-market fit analysis

### 3. Portfolio Analysis
**Gap**: No data-driven brand performance comparison
**Solution**: Calculate revenue proxy, overlap analysis, and CSR scoring per brand

## Key Business Insights to Highlight

### Regional Strategy:
- **Noord-Nederland**: Lower Pon density, high UA potential (cargo bike culture)
- **Randstad** (Noord/Zuid-Holland + Utrecht): High competition, premium focus
- **Zuid-Nederland**: Traditional cycling, Gazelle stronghold
- **Oost-Nederland**: Balanced market, growth opportunities

### Brand Positioning:
- **Urban Arrow**: Premium cargo, ZE-zones priority, B2B+B2C strategy
- **Gazelle**: Mass market e-bikes, family-oriented, suburban focus  
- **Cannondale/Cervélo**: Performance/sport, higher income areas, less dense network
- **Union**: **DISCONTINUED** - overlapped with Gazelle, strategic focus

### International Expansion (Urban Arrow):
**Target countries**: Denmark, Germany (urban centers), Belgium
**Criteria**: Bike culture >15% modal split, ZE-policy, GDP >€30k, urban density >2000 addr/km²
**Strategy**: Premium dealer selection, 3-5km minimum spacing, B2B emphasis

## Development Priorities

### Immediate (Case Presentation):
1. **Implement working notebooks** with real calculations
2. **Fix geographic mapping** using woonplaatsen data
3. **Create board slides** with concrete numbers
4. **Build functional dashboard** with key filters

### Extended (Post-Interview):
1. **Machine learning model** for dealer success prediction
2. **Real-time data feeds** via APIs
3. **Advanced proximity analysis** with travel time
4. **Competitive intelligence** integration

## Assumptions & Limitations

### Data Assumptions:
- Dealer uniqueness based on `google_place_id`
- CBS value -99997 = missing/confidential (0 for counts, NaN for ratios)
- Distance = straight-line, not actual travel routes
- Snapshot data from 2024, no temporal trends

### Business Assumptions:
- Urban Arrow network is "successful" benchmark
- ZE-zones drive cargo bike demand significantly  
- Premium brands (UA, Cervélo) need wider catchment areas
- Dealer quality correlates with rating × log(reviews)

### Model Limitations:
- No revenue data (proxy via ratings/reviews)
- No seasonal variations in demand
- No competitive response modeling
- No supply chain/inventory constraints

## Current Progress & Key Findings (September 2025)

### Analysis Completed ✅:
- **01_dataprep.ipynb**: Successfully processed 2,080 dealers with CORRECTED deduplication (preserved 1,507 Pon brand relationships)
- **02_coverage.ipynb**: Identified 66 white spots affecting 289k people; 97.2% population within 7.5km of Pon dealer  
- **03_kpis_viz.ipynb**: Generated KPIs for 817 gemeenten and 7 provinces with CORRECTED market share (22.3% TRUE vs 43.8% location-based)
- **04_enrichment.ipynb**: Demographics clustering and ZE-zones integration with 5-cluster market segmentation
- **05_intl_shortlist.ipynb**: International expansion analysis with academic research (Germany #1 target)
- **06_portfolio_advies.ipynb**: Brand portfolio analysis with multi-brand cannibalization insights

### Key Market Insights Discovered:
- **Excellent Coverage**: 97.2% population coverage at 7.5km radius (best-in-class performance)
- **Corrected Market Share**: TRUE market share of 22.3% (relationship-based) vs 43.8% location presence
- **Multi-Brand Reality**: 1,374 multi-brand locations detected (68% of all dealers sell multiple brands)
- **Limited White Spots**: Only 66 underserved areas, mostly rural (Vaals, Ouddorp, Valkenburg top opportunities)  
- **High Competition**: 12.8 competitors per Pon dealer within 10km (fragmented market)
- **Internal Cannibalization**: 8.3 Pon dealers within 10km on average

### Current Data Outputs:
- `dealers_all_brands.parquet` - Complete brand-dealer relationship matrix (6,748 relationships)
- `gemeente_kpis.csv` - 817 gemeente performance metrics with CORRECTED densities
- `provincie_kpis.csv` - 7 provincie regional summaries
- `white_spots_with_policy.csv` - 66 growth opportunities with demographic scoring  
- `coverage_analysis.png` - 4-panel executive dashboard
- `market_summary_corrected.csv` - Board-level KPIs with TRUE 22.3% market share
- `ua_intl_academic_analysis.csv` - International expansion targets with opportunity scores
- `portfolio_recommendations.csv` - Strategic brand portfolio decisions
- `multi_pon_dealers.csv` - Cannibalization analysis (391 multi-brand locations)
- `proximity_kpis.csv` - Cannibalization vs competition analysis
- `brand_performance_analysis.csv` - Multi-brand portfolio insights

### ✅ ALL ANALYSIS COMPLETED - CASE READY FOR PRESENTATION

### Critical Issues Resolved:
- ✅ **Data Deduplication Fixed**: Corrected 69% data loss from aggressive deduplication, restored 1,507 Pon relationships
- ✅ **Market Share Corrected**: Fixed artificially inflated 43.8% to realistic 22.3% (relationship-based calculation)  
- ✅ **Multi-Brand Analysis Enabled**: Detected 1,374 multi-brand locations for cannibalization analysis
- ✅ **Geographic Mapping**: Successfully used dealer addresses for gemeente extraction
- ✅ **Data Quality**: Handled -99997 CBS missing values and PC4 data type conflicts
- ✅ **Policy Integration**: Built policy_index.csv for 29 ZE-zone gemeenten with temporal weighting
- ✅ **International Analysis**: Germany identified as #1 expansion target with academic backing
- ✅ **Portfolio Strategy**: Complete brand recommendations (EXPAND Gazelle, MAINTAIN 5 brands, EVALUATE Focus)
- ✅ **Cannibalization Quantified**: 40% of Pon dealers have internal competition (industry norm)

## Success Metrics for Case

### Technical Excellence:
- All notebooks run without errors
- Dashboard loads <3 seconds with full dataset
- Geographic mapping 95%+ accuracy
- Reproducible results with documented seeds

### Business Impact:
- Clear answer to all 3 core questions with data
- Actionable recommendations with ROI estimates
- Risk assessment for each strategic option
- Timeline for implementation with milestones

### Presentation Quality:
- Max 15 minutes with 3 key insights
- Board-level visualizations (clear, impactful)
- Confident handling of Q&A on methodology
- Demonstration of business acumen beyond technical skills