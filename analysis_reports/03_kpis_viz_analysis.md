# 03_KPIs & Visualization Analysis Report: Market Metrics & Strategic Insights

**Date**: September 6, 2025  
**Notebook**: 03_kpis_viz.ipynb  
**Status**: ✅ COMPLETED - Comprehensive KPIs with corrected market share

## Executive Summary

The KPI analysis reveals a **fundamental market reality**: while Pon has presence in 47% of dealer locations, the **true market share is only 22.3%** based on brand relationships. This discrepancy (224% more brand relationships than locations) highlights the multi-brand nature of the bicycle retail market. The analysis confirms excellent coverage (97.3% population within 7.5km) but reveals significant internal competition with a cannibalization index of 6.5 dealers within 7.5km.

### Key Findings:
- **TRUE Market Share**: 22.3% (1,507/6,748 brand relationships)  
- **Location Presence**: 47.0% (978/2,080 locations)
- **Coverage Excellence**: 97.3% population within 7.5km
- **Multi-brand Reality**: 224% more relationships than locations
- **High Cannibalization**: 6.5 Pon dealers within 7.5km average

---

## Market Share Analysis (CORRECTED)

### The Two-Metric Reality

**Location-Based Metrics (Coverage Context):**
- Total dealer locations: 2,080
- Pon presence: 978 locations (47.0%)
- Used for: Coverage analysis, geographic strategy

**Relationship-Based Metrics (TRUE Market Share):**
- Total brand-dealer relationships: 6,748
- Pon relationships: 1,507 (22.3%)
- Used for: Market share, competitive position

**Strategic Insight**: The 224% ratio (6,748/2,080) indicates each location sells 3.2 brands on average, explaining why location presence (47%) vastly overstates actual market share (22.3%).

---

## Geographic KPI Analysis

### Gemeente-Level Performance (817 municipalities analyzed)

#### Top 10 Cities by Population & Pon Performance

| City | Population | Pon Dealers | Total Dealers | Pon Share | Pon/100k | Coverage |
|------|------------|-------------|---------------|-----------|----------|----------|
| **Amsterdam** | 627,180 | 45 | 115 | 39.1% | 7.2 | High |
| **Rotterdam** | 266,400 | 13 | 31 | 41.9% | 4.9 | Good |
| **Utrecht** | 234,045 | 17 | 36 | 47.2% | 7.3 | High |
| **Den Haag** | 204,870 | 14 | 34 | 41.2% | 6.8 | High |
| **Eindhoven** | 121,100 | 11 | 16 | 68.8% | 9.1 | High |
| **Nijmegen** | 119,350 | 9 | 19 | 47.4% | 7.5 | High |
| **Enschede** | 115,100 | 9 | 18 | 50.0% | 7.8 | High |
| **Tilburg** | 111,880 | 6 | 14 | 42.9% | 5.4 | High |
| **Haarlem** | 109,300 | 7 | 21 | 33.3% | 6.4 | High |
| **Groningen** | 105,360 | 12 | 27 | 44.4% | 11.4 | High |

**Key Insights:**
- **Eindhoven** shows highest Pon dominance (68.8% share)
- **Groningen** has highest dealer density (11.4 per 100k)
- **Rotterdam** relatively underserved (4.9 per 100k) despite size
- All major cities classified as "High Coverage"

### Coverage Category Distribution

Analysis of 817 gemeenten coverage levels:

| Category | Count | Population | % of Total |
|----------|-------|------------|------------|
| **High Coverage** (>5/100k) | 312 | 8.2M | 46.1% |
| **Good Coverage** (2-5/100k) | 287 | 5.8M | 32.6% |
| **Low Coverage** (0.5-2/100k) | 186 | 3.2M | 18.0% |
| **Underserved** (<0.5/100k) | 32 | 0.6M | 3.3% |

**Strategic Finding**: 78.7% of population in well-served areas (Good/High coverage)

---

## Provincie-Level Analysis

### Regional Performance Metrics

| Province | Population | Pon Dealers | Total | Pon Share | Pon/100k | Market % |
|----------|------------|-------------|-------|-----------|----------|----------|
| **Noord-Holland** | 5,471,905 | 262 | 584 | 44.9% | 4.8 | 30.7% |
| **Zuid-Holland** | 4,415,325 | 219 | 475 | 46.1% | 5.0 | 24.8% |
| **Noord-Brabant** | 2,211,325 | 131 | 253 | 51.8% | 5.9 | 12.4% |
| **Limburg** | 1,875,590 | 87 | 207 | 42.0% | 4.6 | 10.5% |
| **Overijssel** | 1,704,005 | 130 | 242 | 53.7% | 7.6 | 9.6% |
| **Flevoland/Overijssel** | 1,065,960 | 77 | 168 | 45.8% | 7.2 | 6.0% |
| **Groningen/Friesland/Drenthe** | 1,065,065 | 72 | 149 | 48.3% | 6.8 | 6.0% |

**Regional Insights:**
- **Overijssel** shows strongest Pon position (53.7% share, 7.6/100k)
- **Noord-Brabant** second strongest (51.8% share)
- **Randstad** (NH+ZH) represents 55.5% of population but lower density
- **Limburg** weakest position (42.0% share, 4.6/100k)

---

## Competition & Cannibalization Metrics

### Proximity Analysis Results

| Distance Ring | Pon near Pon | Pon near Competitors | Cannibalization | Competition |
|---------------|--------------|---------------------|-----------------|-------------|
| 3 km | 1,862 | 2,758 | 1.9 dealers | 2.8 dealers |
| 5 km | 3,622 | 5,202 | 3.7 dealers | 5.3 dealers |
| **7.5 km** | **6,350** | **8,466** | **6.5 dealers** | **8.7 dealers** |
| 10 km | 9,502 | 12,173 | 9.7 dealers | 12.4 dealers |

**Critical Findings:**
- **High Internal Competition**: 6.5 Pon dealers within standard service radius
- **Intense Market Competition**: 8.7 competitors in same radius
- **Cannibalization Risk**: 75% ratio (6.5/8.7) suggests oversaturation
- **Density Problem**: More internal than optimal for market share

---

## White Spot & Growth Opportunities

### Coverage Gaps Analysis

- **Total white spots**: 59 PC4 areas
- **Population affected**: 270,220 people (2.7% of mapped population)
- **Average distance to Pon**: 9.7 km
- **Largest white spot**: Valkenburg (10,530 people)

### Top 15 White Spots by Population

Visualized in coverage_analysis.png, ranked by combined score:

1. **Vaals** - 7,900 people, 13.2km from Pon
2. **Ouddorp** - 6,295 people, 14.6km
3. **Wieringerwerf** - 6,120 people, 12.6km
4. **Valkenburg** - 10,530 people, 9.9km
5. **Hulst** - 9,930 people, 10.3km

**White Spot Characteristics:**
- Primarily rural/border regions
- Small population centers (<10k)
- Limited growth potential
- No overlap with ZE-zones

---

## Visualization Insights

### Coverage Analysis Chart (4-panel dashboard)

**Panel 1: Coverage by Radius**
- Shows exponential coverage curve
- 92.4% at 5km → 97.3% at 7.5km → 99.2% at 10km
- Diminishing returns beyond 7.5km

**Panel 2: Proximity & Competition**
- Visual comparison of internal vs external competition
- Clear cannibalization risk visualization
- Competition exceeds cannibalization at all distances

**Panel 3: Coverage Categories**
- Pie chart showing gemeente distribution
- 78.7% in Good/High coverage
- Only 3.3% truly underserved

**Panel 4: White Spot Priorities**
- Bar chart of top 15 white spots
- Color-coded by opportunity score
- Shows limited individual opportunity sizes

---

## Data Quality & Methodology

### Coverage Metrics
- **Population analyzed**: 17.8M total
- **Gemeenten covered**: 817/850+ (96% coverage)
- **Provincie mapping**: 99.9% accuracy
- **Missing data**: 3 dealers (0.1%) lack gemeente mapping

### Market Share Calculation (CORRECTED)
- **Previous (incorrect)**: 43.8% based on aggregated locations
- **Corrected method**: Count all brand-dealer relationships
- **True market share**: 22.3% (1,507/6,748 relationships)
- **Validation**: Multi-brand reality explains discrepancy

---

## Strategic Implications

### 1. Market Position Reality Check
- **Actual market share (22.3%)** far below perceived presence (47%)
- Multi-brand dealers dilute Pon's true market position
- Need exclusive dealer strategy to improve conversion

### 2. Coverage vs Efficiency Trade-off
- Excellent coverage (97.3%) achieved but at high cost
- Cannibalization index (6.5) suggests over-distribution
- Consolidation opportunity in high-density areas

### 3. Regional Prioritization
- **Strong regions**: Overijssel (53.7%), Noord-Brabant (51.8%)
- **Growth regions**: Rotterdam (underserved), Limburg (weak share)
- **Optimization regions**: Amsterdam, Utrecht (high cannibalization)

### 4. Competitive Response Required
- 8.7 competitors within 7.5km demands differentiation
- Cannot compete on location alone (already saturated)
- Focus on exclusive models, service quality, brand strength

---

## Key Performance Indicators Summary

### National KPIs
- **True Market Share**: 22.3% ✅
- **Location Presence**: 47.0% ✅
- **Population Coverage (7.5km)**: 97.3% ✅
- **White Spot Population**: 2.7% ✅

### Efficiency KPIs
- **Cannibalization Index**: 6.5 ⚠️ (HIGH)
- **Competition Index**: 8.7 ⚠️ (HIGH)
- **Multi-brand Ratio**: 224% ⚠️ (DILUTION)
- **Dealers per 100k**: 5.5 (national average)

### Growth KPIs
- **Underserved Gemeenten**: 32 (3.9%)
- **Growth Potential**: 270k people (1.5%)
- **High Coverage Cities**: 312 (38.2%)
- **Expansion ROI**: Limited due to saturation

---

## Recommendations

### Immediate Actions
1. **Recalibrate market share targets** based on 22.3% reality
2. **Audit multi-brand dealers** for exclusivity opportunities
3. **Consolidate high-cannibalization areas** (Amsterdam, Utrecht)
4. **Target Rotterdam** for strategic expansion (underserved)

### Strategic Initiatives
1. **Exclusive Dealer Program**: Convert multi-brand to Pon-only
2. **Brand Specialization**: Assign primary brands per dealer
3. **Service Differentiation**: Compete on quality not location
4. **Regional Focus**: Strengthen Overijssel/Brabant dominance

### Metrics to Track
1. **Relationship share** (not just location share)
2. **Exclusive dealer percentage**
3. **Revenue per dealer** (efficiency metric)
4. **Brand overlap reduction** (cannibalization mitigation)

---

## Conclusion

The KPI analysis reveals a market where Pon's perceived dominance (47% location presence) masks a more modest reality (22.3% true market share). While coverage is excellent (97.3%), the high cannibalization index (6.5) and intense competition (8.7 competitors per dealer) indicate an inefficient distribution strategy.

The path forward requires **consolidation and specialization** rather than expansion, with focus on converting multi-brand dealers to exclusive partnerships and improving per-dealer performance rather than adding locations.

---

## Export Files Created

### Data Tables
1. **gemeente_kpis.csv** - 817 municipality-level metrics
2. **provincie_kpis.csv** - 7 province-level aggregates  
3. **market_summary_corrected.csv** - True 22.3% market share
4. **market_summary.csv** - Location-based metrics for coverage

### Visualizations
1. **coverage_analysis.png** - 4-panel executive dashboard

---

*Report generated from notebook 03_kpis_viz.ipynb outputs on September 6, 2025*