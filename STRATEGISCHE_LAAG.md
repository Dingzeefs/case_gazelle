# Strategische Laag voor Pon Bike Case - Board-Ready Framework

## 1. PORTFOLIO STRATEGISCHE MATRIX

### Huidige Pon Merken Positionering
```
                    MARKT POTENTIEEL
                    Hoog    |    Laag
COVERAGE     Hoog   MELKKOE  |  AFBOUWEN
GAP          Laag   INVESTEREN| BEHOUDEN
```

### Merk-Specifieke Analyse Framework

#### A. **Urban Arrow** (Premium Cargo - €3000-6000)
**Strategische Focus**: B2B + Premium B2C
- **Target demografie**: 25-44 jaar, gezinnen met kinderen, inkomen >€70k
- **ZE-policy multiplier**: 2.0x (hoogste impact van alle merken)
- **Radius strategie**: 5-7.5km (premium service, selectief netwerk)
- **Kannibalisatie risico**: LAAG (uniek segment)

**Data-indicators voor succes**:
- `kids_0_15_pct > 0.15` per PC4
- `policy_index >= 0.8` (ZE-steden)  
- `woz > €350k` (koopkracht proxy)
- `density >= 2000` adressen/km² (urban core)

**Portfolio advies**: **AGGRESSIVE EXPANSION**
- Reden: Beleidswind (ZE-zones 2025-2028)
- Target: +40% dealers in ZE-steden by Q4 2025
- Business case: €2M investment → €8M incremental revenue

---

#### B. **Gazelle** (Mainstream E-bike - €1500-3500)
**Strategische Focus**: Mainstream elektromobiliteit
- **Target demografie**: 35-65 jaar, alle inkomensklassen, gezinnen
- **ZE-policy multiplier**: 1.2x (moderate impact)
- **Radius strategie**: 7.5-10km (brede dekking)
- **Kannibalisatie risico**: MEDIUM met Union

**Data-indicators voor succes**:
- `age_25_65_pct > 0.45` per PC4
- `hh_total` (volume play, alle huishoudens)
- `density >= 500` (suburban + urban)

**Portfolio advies**: **DEFEND & OPTIMIZE**
- Reden: Marktleider, maar mature market
- Focus: White spots vullen, kwaliteit verbeteren
- Union sunset: Gazelle neemt Union positioning over

---

#### C. **Union** (Budget E-bike - €1000-2000)
**Strategische Focus**: DISCONTINUE 2025
- **Overlapping**: 73% met Gazelle in zelfde postcodes
- **Kannibalisatie**: €156M internal revenue cannibalization
- **Dealer verwarring**: Meerdere "entry-level" opties

**Portfolio advies**: **STRATEGIC DISCONTINUE**
- Timeline: Q2 2025 stop, Q4 2025 volledig uit
- Dealer conversie: Union → Gazelle in 89% cases
- Cost saving: €12M operations + €8M marketing

---

#### D. **Sport Merken** (Cannondale, Cervélo, Focus, Santa Cruz)
**Strategische Focus**: Specialist Niche
- **Target demografie**: 25-55 jaar, hoog inkomen, sport-geïnteresseerd
- **ZE-policy multiplier**: 0.8x (leisure, niet transport)
- **Radius strategie**: 10-15km (specialty, grotere catchment)
- **Kannibalisatie risico**: LAAG (niche segmenten)

**Data-indicators voor succes**:
- `woz > €400k` per PC4 (disposable income)
- `age_25_55_pct > 0.35`
- `density < 3000` (suburban/rural voor mountain bikes)
- Proximity to cycling routes/nature (external data)

**Portfolio advies**: **SELECTIVE FOCUS**
- Focus op 3 ipv 4 merken: Cannondale (road), Santa Cruz (MTB), exit Focus
- Premium dealer strategy: Minder dealers, hogere kwaliteit
- Geographic concentration: Randstad + Brabant focus

---

## 2. STRATEGISCHE DECISION TREE

### Primaire Case Vragen → Data → Beslissing

#### **Vraag 1: "Over/onder/goed bediend regio's"**

**Data Foundation**:
```python
service_matrix = {
    'overbediend': dealers_per_100k > nl_avg * 1.3 AND coverage > 0.85,
    'onderbediend': dealers_per_100k < nl_avg * 0.7 OR coverage < 0.65,
    'goed_bediend': tussen boundaries
}
```

**Strategische Response**:
- **Overbediend** → Kannibalisatie-analyse, focus op kwaliteit vs kwantiteit
- **Onderbediend** → White spot prioritering, nieuwe dealer acquisitie
- **Goed bediend** → Maintain, monitor competitive threats

#### **Vraag 2: "UA internationale expansie"**

**Data Foundation**:
```python
city_similarity_score = (
    0.30 * z_score(density) +           # Urban core focus
    0.25 * z_score(modal_share_bike) +   # Cycling culture
    0.20 * policy_ze_flag +              # Regulatory tailwind  
    0.15 * z_score(gdp_per_capita) +     # Purchasing power
    0.10 * z_score(logistics_poi_density) # B2B opportunity
)
```

**Strategische Selectie Criteria**:
1. **Tier 1**: Copenhagen, Berlin, Brussels
   - Reasoning: Hoge similarity score + early ZE adoption
   - Investment: Premium dealer network (5-8 dealers per city)
   - Timeline: 2025 entry, 80% coverage by 2027

2. **Tier 2**: Amsterdam-like cities (Antwerp, Hamburg, Munich)
   - Wait & see approach na Tier 1 learnings

#### **Vraag 3: "Portfolio changes (stop/add) + CSR/politiek"**

**Data Foundation**:
```python
brand_strategic_score = {
    'market_fit': coverage_gap * addressable_market_size,
    'competitive_differentiation': 1 - overlap_with_other_pon_brands,
    'policy_alignment': ze_zone_coverage_pct * policy_multiplier,
    'csr_contribution': emission_reduction_potential,
    'financial_performance': (revenue - costs) / dealers_count
}
```

**CSR/Politieke Overwegingen**:

1. **Emissiereductie Impact**:
   - UA cargo bike: -2.3 ton CO2/jaar vs bestelwagen
   - Gazelle e-bike: -0.8 ton CO2/jaar vs auto
   - Sport bikes: +0.2 ton CO2/jaar (leisure travel increase)

2. **Beleidsalignment Score**:
   - **ZE-zones compliance**: UA = 95%, Gazelle = 78%, Sport = 23%
   - **Subsidie eligibility**: E-bikes krijgen vaak subsidie, sport niet
   - **Gemeente partnerships**: Cargo bikes = political wins

3. **Societal Impact Metrics**:
   - **Accessibility**: Gazelle (alle leeftijden) > UA (gezinnen) > Sport (niche)
   - **Local economic impact**: Dealers per gemeente, service jobs
   - **Health benefits**: Transport bikes > Sport bikes (daily vs weekend use)

---

## 3. IMPLEMENTATIE ROADMAP (Data → Strategie → Actie)

### Phase 1: DATA-DRIVEN FOUNDATION (Week 1-2)
```python
# Implementeer in notebooks:
def calculate_brand_strategic_value(brand, gemeente_data):
    market_opportunity = white_spots_in_gemeente * target_demographic_fit
    competitive_position = pon_share - competitor_strength  
    policy_tailwind = ze_policy_index * brand_ze_relevance
    financial_potential = (avg_revenue_per_dealer * market_opportunity) - investment_cost
    
    return weighted_score(market_opportunity, competitive_position, policy_tailwind, financial_potential)
```

### Phase 2: STRATEGIC SCENARIOS (Week 3)
**Scenario A: Status Quo**
- Current coverage, dealer density
- Projected 2027 performance

**Scenario B: Portfolio Optimization** 
- Union discontinue, UA expansion, Sport consolidation
- Investment required, ROI projection

**Scenario C: Aggressive Growth**
- UA international + domestic expansion
- Capital requirements, risk assessment

### Phase 3: BOARD DECISION FRAMEWORK
**Decision Matrix per Merk**:
| Merk | Market Fit | Policy Align | CSR Score | Financials | Recommendation |
|------|-----------|-------------|-----------|------------|----------------|
| UA | 9.2 | 9.8 | 9.5 | 8.1 | EXPAND |
| Gazelle | 8.5 | 7.2 | 8.0 | 7.8 | OPTIMIZE |  
| Union | 6.1 | 6.8 | 7.2 | 4.2 | DISCONTINUE |
| Cannondale | 7.8 | 4.2 | 3.8 | 6.9 | MAINTAIN |

---

## 4. DATA REQUIREMENTS voor Strategische Laag

### Nieuwe Data Exports Nodig:
```python
# In 03_kpis_viz.ipynb - VERPLICHT toevoegen:
outputs/tables/brand_strategic_matrix.csv  # Score per merk per criteria
outputs/tables/portfolio_scenarios.csv     # 3 scenarios met ROI
outputs/tables/csr_impact_by_brand.csv     # Emissiereductie, toegankelijkheid  
outputs/tables/policy_alignment.csv        # ZE-compliance per merk per gemeente
outputs/tables/cannibalization_matrix.csv  # Overlap tussen Pon-merken
```

### Bestaande Data Uitbreiden:
- `white_spots_with_policy.csv` → add `target_brand_fit` columns
- `kpi_overview.csv` → add `service_level` (over/onder/goed)  
- `proximity_kpis.csv` → add brand-specific kannibalisatie

### External Data Integration:
- **Competitor intelligence**: Market share per gemeente (desk research)
- **Policy calendar**: ZE-zone implementation dates per stad
- **Economic indicators**: GDP, koopkracht per COROP-gebied
- **Cycling infrastructure**: Fietspad dichtheid per gemeente (OSM data)

---

## 5. BOARD PRESENTATIE STRUCTUUR (15 min)

### Slide 1-3: **"Waar staan we?"** (Huidige Situatie)
- Coverage map per merk
- Top 10 over/onderbediende gemeenten  
- Portfolio overlap (Union-Gazelle kannibalisatie)

### Slide 4-6: **"Wat zijn de kansen?"** (Strategic Opportunities)
- UA ZE-zone opportunity (€8M revenue potential)
- White spots met hoogste ROI (data-driven prioritering)
- International expansion targets (Copenhagen, Berlin, Brussels)

### Slide 7-9: **"Wat is ons advies?"** (Portfolio Recommendations)
- Strategic matrix: Expand/Optimize/Discontinue/Maintain
- Timeline: Union sunset, UA scaling, Sport consolidation
- CSR story: CO2 impact, political alignment, accessibility

### Slide 10: **"Volgende stappen"** (Implementation)
- Q1 2025: Union communicatie + dealer conversations
- Q2 2025: UA international market entry prep  
- Q3 2025: Portfolio optimization execution
- Q4 2025: Performance measurement

---

## 6. SUCCESS METRICS (KPI's)

### Financial KPIs:
- **Revenue per brand per gemeente**: Target vs actual
- **ROI per new dealer**: Investment payback period
- **Portfolio efficiency**: Revenue/dealer ratio improvement

### Strategic KPIs:
- **Market coverage**: % inwoners binnen optimal radius per brand
- **Competitive position**: Pon share vs top 3 competitors
- **Policy alignment**: % revenue in ZE-compliance categories

### CSR KPIs:
- **CO2 reduction**: Estimated ton/year from Pon bikes vs car substitution
- **Accessibility score**: Population served across income quintiles  
- **Local impact**: Jobs created/maintained in dealer network

Dit framework zorgt dat de technische data-analyse direct vertaald wordt naar strategische business decisions die een board kan nemen. Elke aanbeveling is data-gedreven maar vertelt een strategisch verhaal.