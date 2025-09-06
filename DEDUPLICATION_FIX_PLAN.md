# Deduplication Distortion Fix Plan

## Executive Summary

The current deduplication logic in `01_dataprep.ipynb` has severely distorted our analysis by:
- **Reducing 6,748 dealer records to 2,080** (69% data loss)
- **Artificially inflating Pon market share from 19% to 44%**
- **Eliminating multi-brand dealers entirely** (cannibalization analysis impossible)
- **Losing 370 Pon dealer records** critical for brand performance analysis

## Root Cause Analysis

**Current Logic (PROBLEMATIC):**
```python
dealers = dealers.sort_values(["google_place_id","is_pon_dealer"], ascending=[True,False])
dealers = dealers.drop_duplicates("google_place_id")
```

**Problem:** This keeps only ONE brand per physical location, prioritizing Pon brands but losing all multi-brand information.

**Impact:** A dealer selling Gazelle + Kalkhoff + Cannondale becomes just "Gazelle dealer" in processed data.

## Data Quality Impact Analysis

| Metric | Raw Data | Processed Data | Distortion |
|--------|----------|----------------|------------|
| **Total Records** | 6,748 | 2,080 | -69% |
| **Pon Dealer Records** | 1,282 | 912 | -29% |
| **Market Share (Pon)** | 19.0% | 43.8% | +130% |
| **Multi-brand Locations** | 1,404 | 0 | -100% |

### Brand-Specific Data Loss:
- **Union**: 247 → 57 dealers (**-77% loss**)
- **Kalkhoff**: 199 → 75 dealers (**-62% loss**)
- **Focus**: 8 → 4 dealers (**-50% loss**)
- **Cervélo**: 35 → 23 dealers (**-34% loss**)
- **Gazelle**: 701 → 661 dealers (**-6% loss** - prioritized by dedup logic)

## Notebook-by-Notebook Fix Requirements

### ✅ **01_dataprep.ipynb** - NEEDS MAJOR REWRITE
**Status:** CRITICAL - Root cause of all distortions

**Current Issues:**
- Eliminates multi-brand dealers completely
- Loses 370 Pon dealer relationships
- Creates artificial market share inflation

**Required Changes:**
```python
# REPLACE current deduplication logic with proper aggregation:

# Method 1: Preserve all brand relationships
dealers_by_location = dealers_raw.groupby('google_place_id').agg({
    'name': 'first',
    'brand_clean': lambda x: list(sorted(set(x))),  # All brands per location
    'is_pon_dealer': 'any',  # True if any Pon brand present
    'google_rating': 'first',
    'google_lat': 'first',
    'google_lng': 'first',
    'pc4': 'first',
    'pon_brand_count': lambda x: sum(brand in PON_BRANDS for brand in x),
    'total_brand_count': 'count'
}).reset_index()

# Method 2: Create brand-location matrix for detailed analysis
brand_location_matrix = dealers_raw.pivot_table(
    index='google_place_id',
    columns='brand_clean', 
    values='is_pon_dealer',
    aggfunc='any',
    fill_value=False
)
```

**Deliverables:**
- `data/processed/dealers_locations.parquet` (unique locations with all brands)
- `data/processed/dealers_brands.parquet` (brand-location relationships)
- `data/processed/brand_location_matrix.parquet` (cannibalization analysis ready)

---

### ⚠️ **02_coverage.ipynb** - MINOR ADJUSTMENTS
**Status:** MOSTLY OK - Uses unique locations only

**Current Issues:**
- None for coverage calculation (uses unique locations)
- KPIs section may use wrong dealer counts

**Required Changes:**
```python
# Update dealer density calculations to use location-based counts:
dealers_per_pc4 = dealers_locations.groupby('pc4').size()  # Use location count
pon_dealers_per_pc4 = dealers_locations[dealers_locations['is_pon_dealer']].groupby('pc4').size()
```

**Deliverables:**
- Updated proximity analysis with correct dealer counts
- Revised `proximity_kpis.csv` with accurate metrics

---

### ❌ **03_kpis_viz.ipynb** - NEEDS SIGNIFICANT UPDATES  
**Status:** AFFECTED - Dealer density and market share wrong

**Current Issues:**
- Dealer density underestimated (missing 69% of data)
- Pon market share overestimated (44% vs actual 19%)
- Brand performance comparisons invalid

**Required Changes:**
```python
# Fix gemeente KPIs with correct counts:
gemeente_kpis = dealers_raw.groupby(['gemeente']).agg({
    'google_place_id': 'nunique',  # Unique locations (not records)
    'is_pon_dealer': 'sum',  # Total Pon relationships
    'brand_clean': 'count'  # Total brand relationships
}).reset_index()

gemeente_kpis['dealers_per_100k'] = gemeente_kpis['unique_locations'] / population * 100000
gemeente_kpis['pon_brand_share'] = gemeente_kpis['pon_brands'] / gemeente_kpis['total_brands']
gemeente_kpis['pon_location_share'] = gemeente_kpis['pon_locations'] / gemeente_kpis['unique_locations']
```

**Deliverables:**
- `kpi_overview_corrected.csv` with accurate dealer densities
- `brand_performance_corrected.csv` with true brand counts
- `market_share_analysis.csv` with location-based vs brand-based metrics

---

### ❌ **06_portfolio_advies.ipynb** - NEEDS COMPLETE OVERHAUL
**Status:** SEVERELY AFFECTED - All brand analysis invalid

**Current Issues:**
- Brand performance scores completely wrong
- Missing 370 Pon dealer relationships
- Cannibalization analysis impossible (0% multi-brand dealers)
- Union brand appears to underperform (77% data loss)

**Required Changes:**
```python
# Brand performance with correct data:
brand_performance = dealers_raw[dealers_raw['is_pon_dealer']].groupby('brand_clean').agg({
    'google_place_id': 'nunique',  # Unique locations per brand
    'name': 'count',  # Total brand relationships
    'google_rating': 'mean',
    'google_user_ratings_total': 'mean'
}).reset_index()

# Cannibalization analysis with multi-brand locations:
multi_brand_locations = dealers_locations[dealers_locations['pon_brand_count'] > 1]
cannibalization_rate = len(multi_brand_locations) / len(dealers_locations[dealers_locations['is_pon_dealer']])

# Brand co-occurrence matrix:
brand_matrix = dealers_raw.pivot_table(
    index='google_place_id',
    columns='brand_clean',
    values='is_pon_dealer',
    aggfunc='any',
    fill_value=False
)
```

**Deliverables:**
- `brand_performance_corrected.csv` with accurate dealer counts
- `cannibalization_analysis.csv` with true multi-brand rates
- `brand_cooccurrence_matrix.csv` for portfolio overlap analysis
- `portfolio_recommendations_revised.csv` based on correct data

---

### ✅ **05_intl_shortlist.ipynb** - NO CHANGES NEEDED
**Status:** UNAFFECTED - Uses independent academic data

**Reason:** Uses Goel et al. (2022) academic research data, not dealer data.

---

## Implementation Strategy

### Phase 1: Critical Path (Immediate)
1. **Fix `01_dataprep.ipynb`** - Rewrite deduplication logic
2. **Update `06_portfolio_advies.ipynb`** - Use corrected data for brand analysis
3. **Validate results** - Ensure market share = 19%, not 44%

### Phase 2: Refinement (Next)
1. **Update `03_kpis_viz.ipynb`** - Correct gemeente KPIs
2. **Refine `02_coverage.ipynb`** - Update proximity analysis
3. **Re-run Streamlit dashboard** with corrected data

### Phase 3: Validation (Final)
1. **Cross-check all analyses** for consistency
2. **Update board presentation** with accurate metrics
3. **Document methodology changes**

## Risk Assessment

### High Risk (Address Immediately):
- **Portfolio recommendations based on wrong data** → Could recommend exiting profitable brands
- **Market share inflation** → Wrong strategic positioning vs competitors
- **Missing cannibalization insights** → Suboptimal dealer network strategy

### Medium Risk:
- **Gemeente KPIs underestimated** → Wrong resource allocation priorities
- **Coverage analysis slightly off** → Minor impact on expansion decisions

### Low Risk:
- **White spots analysis** → Minimal impact (location-based)
- **International analysis** → No impact (independent data)

## Expected Outcomes After Fix

| Metric | Before Fix | After Fix | Impact |
|--------|------------|-----------|--------|
| **Pon Market Share** | 43.8% | ~19% | Realistic positioning |
| **Multi-brand Dealers** | 0% | ~25-30% | Cannibalization visible |
| **Union Performance** | Appears weak | True performance | Accurate portfolio decisions |
| **Total Pon Relationships** | 912 | 1,282 | +40% brand relationships |

## Implementation Timeline

- **Day 1:** Fix `01_dataprep.ipynb` and regenerate processed data
- **Day 2:** Update `06_portfolio_advies.ipynb` with corrected analysis  
- **Day 3:** Validate all dependent notebooks and outputs
- **Day 4:** Update board presentation with accurate insights

## Success Criteria

✅ **Market share drops to realistic ~19%**  
✅ **Multi-brand dealers detected (expected ~25-30%)**  
✅ **Union brand shows true performance (not artificially low)**  
✅ **Cannibalization analysis provides actionable insights**  
✅ **All brand performance scores based on complete data**

---

**Priority: CRITICAL**  
**Impact: HIGH**  
**Effort: MEDIUM**

This fix is essential for credible board-level recommendations and strategic decision-making.