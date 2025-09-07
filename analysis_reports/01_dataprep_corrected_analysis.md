# 01_Dataprep Analysis Report: Critical Data Quality Corrections

**Date**: September 6, 2025  
**Notebook**: 01_dataprep.ipynb  
**Status**: ✅ CORRECTED - Major data quality issues resolved  

## Executive Summary

This analysis reveals **critical data quality corrections** that fundamentally change the Gazelle/Pon market analysis. The primary issue was Urban Arrow's exclusion from PON_BRANDS due to a format mismatch, leading to severely underestimated performance metrics.

### Key Corrections Made:
- **Urban Arrow inclusion**: Fixed PON_BRANDS definition (213 relationships vs 13)
- **True market share**: Corrected from 43.8% to realistic 22.3% 
- **Multi-brand preservation**: Retained 1,374 multi-brand locations (66% of dealers)
- **Geographic accuracy**: Achieved 99.9% PC4 mapping coverage

---

## Critical Findings

### 1. Urban Arrow Data Correction (MAJOR)

**Problem Identified:**
- PON_BRANDS defined "urban arrow" (space) but data contains "urban_arrow" (underscore)
- This excluded Urban Arrow from all Pon analysis despite being a key cargo bike brand

**Before Fix:**
```
Urban Arrow: 13 locations (severely underestimated)
```

**After Fix:**
```
Urban Arrow: 211 locations, 213 relationships (10.1% market presence)
Rating: 4.36/5.0, Reviews: 99.1 average
```

**Impact:**
- Urban Arrow is now the **3rd largest Pon brand** by dealer count
- Essential for cargo bike market analysis and ZE-zone strategy
- Changes international expansion benchmarks

### 2. Market Share Recalculation

**Relationship-Based Analysis (TRUE):**
- Total dealer relationships: 6,748
- Pon relationships: 1,507
- **True market share: 22.3%**

**Location-Based Analysis:**
- Unique locations: 2,080
- Pon locations: 978
- Location share: 47.0%

**Previous Estimate (INCORRECT):** 43.8% (due to data aggregation issues)

### 3. Multi-Brand Dealer Reality

**Discovery:** 66.1% of dealers (1,374 locations) sell multiple brands

**Multi-Brand Statistics:**
- Average brands per multi-brand location: 4.2
- Multi-Pon locations: 391 (internal cannibalization risk)
- Pure single-brand locations: Only 706 (34%)

**Strategic Implication:** Dealer relationships are complex; simple location counts mislead strategy

---

## Detailed Brand Performance (CORRECTED)

| Brand | Unique Locations | Total Relationships | Market Presence | Avg Rating | Avg Reviews |
|-------|------------------|-------------------|-----------------|------------|-------------|
| Gazelle | 700 | 701 | 33.7% | 4.47 | 69.8 |
| Union | 247 | 247 | 11.9% | 4.40 | 76.4 |
| **Urban Arrow** | **211** | **213** | **10.1%** | **4.36** | **99.1** |
| Kalkhoff | 191 | 199 | 9.2% | 4.46 | 97.5 |
| Cannondale | 92 | 92 | 4.4% | 4.56 | 153.2 |
| Cervélo | 35 | 35 | 1.7% | 4.58 | 74.6 |
| Santa Cruz | 12 | 12 | 0.6% | 4.44 | 90.2 |
| Focus | 8 | 8 | 0.4% | 4.89 | 56.3 |

**Key Insights:**
- **Gazelle dominance**: 33.7% of dealer network, mass-market positioning
- **Urban Arrow significance**: Major cargo bike presence, higher review engagement
- **Premium brands**: Cannondale/Cervélo have higher ratings but lower coverage
- **Union presence**: Strong traditional bike segment (11.9% presence)

---

## Geographic and Demographic Processing

### Geographic Coverage
- **PC4 areas processed**: 4,070 (complete Netherlands)
- **Valid PC4 extraction**: 2,078/2,080 (99.9%)
- **Gemeente mapping**: 1,357 PC4s mapped via dealer addresses (33.3%)
- **Population coverage**: 17.8M people

### Demographic Clustering (K=5)
Five distinct market segments identified:

**Cluster 0 (11.1%): Affluent Families**
- High kids percentage (1.74 std dev above mean)
- High income/WOZ values (0.91 std dev above mean)
- Target for premium e-bikes and cargo bikes

**Cluster 1 (36.7%): Suburban Mainstream** 
- Balanced demographics, largest segment
- Core Gazelle and traditional bike market

**Cluster 2 (15.1%): Urban Renters**
- High rental percentage, higher density
- Target for mobility services and compact bikes

**Cluster 3 (5.0%): Dense Urban Centers**
- Highest density (2.98 std dev), young adults (2.62 std dev)
- Prime Urban Arrow and ZE-zone target areas

**Cluster 4 (32.2%): Suburban Homeowners**
- High ownership rates, lower density
- Traditional bike and recreational market

---

## Data Quality Assessment

### Strengths ✅
- **High geographic coverage**: 99.9% PC4 mapping success
- **Complete brand identification**: All 8 Pon brands correctly identified
- **Multi-brand preservation**: Complex dealer relationships maintained
- **Population completeness**: 17.8M people covered (entire Netherlands)
- **Clean numeric processing**: CBS -99997 values properly handled

### Limitations ⚠️
- **Gemeente mapping**: Only 33.3% coverage (needs external mapping file)
- **Address parsing**: Municipal boundaries extracted from Google addresses
- **Snapshot data**: Single point-in-time analysis (2024)
- **Missing revenue data**: Using ratings/reviews as performance proxy

---

## Impact on Downstream Analysis

### Notebooks Requiring Rerun:
1. **02_coverage.ipynb**: Urban Arrow coverage analysis now meaningful
2. **03_kpis_viz.ipynb**: Market share visualizations need 22.3% correction
3. **04_enrichment.ipynb**: Demographics clustering with full UA network
4. **05_intl_shortlist.ipynb**: UA international expansion benchmarks corrected
5. **06_portfolio_advies.ipynb**: Portfolio strategy with true brand performance

### Strategic Implications:
- **Urban Arrow expansion**: Now viable with 211-dealer network baseline
- **Market share targets**: Realistic 22.3% starting point vs inflated 43.8%
- **Cannibalization analysis**: Multi-brand locations enable internal competition assessment
- **Geographic targeting**: 5-cluster demographic segmentation for precision marketing

---

## Technical Data Files Created

### Primary Datasets:
- **`dealers.parquet`**: 2,080 unique locations with multi-brand aggregation
- **`dealers_all_brands.parquet`**: 6,748 brand-dealer relationships (detailed)
- **`demografie.parquet`**: 4,070 PC4 demographics with 5 clusters

### Analysis Exports:
- **`brand_performance_corrected.csv`**: True brand metrics by relationships
- **`kpis_by_pc4_with_clusters.csv`**: PC4-level KPIs with demographic segments
- **`gemeente_summary.csv`**: Municipal-level population aggregations

---

## Recommendations

### Immediate Actions:
1. **Rerun all downstream notebooks** with corrected data
2. **Update board presentations** with 22.3% market share
3. **Revise Urban Arrow strategy** based on 211-dealer network reality
4. **Implement multi-brand cannibalization analysis** using preserved relationships

### Data Quality Improvements:
1. **Obtain official PC4-gemeente mapping** to improve 33.3% coverage
2. **Validate address parsing** against municipal boundary databases  
3. **Add temporal data** for trend analysis beyond 2024 snapshot
4. **Integrate revenue/sales data** to replace rating-based performance proxies

---

## Conclusion

The data quality corrections fundamentally improve the accuracy and strategic value of the Gazelle/Pon analysis. **Urban Arrow's proper inclusion as the 3rd largest Pon brand** enables meaningful cargo bike strategy development, while **realistic market share calculations** provide achievable growth targets.

The preserved multi-brand dealer relationships reveal a complex market reality where 66% of dealers sell multiple brands, requiring nuanced cannibalization and competitive analysis rather than simple location-based metrics.

**Next Steps**: Systematically rerun notebooks 02-06 with corrected data to update all strategic recommendations and board-level insights.

---

*Report generated from notebook outputs analysis on September 6, 2025*