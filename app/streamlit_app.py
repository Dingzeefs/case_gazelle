
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path

st.set_page_config(page_title='Pon Bike NL - Network Analysis Dashboard', layout='wide')
st.title('🚴‍♀️ Pon Bike Nederland - Dealer Network Dashboard')

# Sidebar with enhanced filters
st.sidebar.title('🔧 Filters & Controls')

# Add explanation section
with st.sidebar.expander("ℹ️ **Hoe werken deze filters?**", expanded=True):
    st.markdown("""
    **🏷️ Select Brands**  
    Kies specifieke Pon-merken om te bekijken. Laat leeg voor alle merken.
    *Gebruik: Focus op één merk voor merkspecifieke analyse*
    
    **📏 Coverage Radius**  
    Stel de serviceradius in (km). Standaard 7.5km = fietsafstand.
    *Gebruik: Test verschillende serviceniveaus (5km stad, 10km ruraal)*
    
    **🌿 ZE-Zones only**  
    Toon alleen dealers in zero-emissie zones (vanaf 2025).
    *Gebruik: Focus op duurzame mobiliteit hotspots*
    
    **⭕ Coverage Rings**  
    Visualiseer servicebereik rond Pon-dealers.
    *Gebruik: Identificeer overlappende servicegebieden*
    
    **🎯 Pon Dealers Only**  
    Verberg concurrenten, toon alleen Pon-netwerk.
    *Gebruik: Interne netwerkanalyse zonder marktruis*
    """)

st.sidebar.markdown("---")

@st.cache_data
def load_csv(path):
    """Load CSV with caching and error handling"""
    return pd.read_csv(path, dtype={'pc4': str}) if Path(path).exists() else None

@st.cache_data
def load_parquet(path):
    """Load parquet with caching"""
    return pd.read_parquet(path) if Path(path).exists() else None

# Load all datasets
dealers = load_parquet('data/processed/dealers.parquet')
if dealers is None:
    dealers = load_csv('data/raw/dealer_lijst.csv')

white_spots = load_csv('outputs/tables/white_spots_with_policy.csv')
if white_spots is None:
    white_spots = load_csv('outputs/tables/white_spots_ranked.csv')

gemeente_kpis = load_csv('outputs/tables/kpi_overview.csv')
coverage_overall = load_csv('outputs/tables/coverage_overall.csv')
policy_index = load_csv('outputs/tables/policy_index.csv')
proximity_kpis = load_csv('outputs/tables/proximity_kpis.csv')
ua_intl = load_csv('outputs/tables/ua_intl_shortlist.csv')

# Enhanced Sidebar Filters
if dealers is not None and 'brand_clean' in dealers.columns:
    brands = sorted([b for b in dealers['brand_clean'].dropna().unique() if b])
    pon_brands = ['gazelle', 'cannondale', 'union', 'kalkhoff', 'urban_arrow', 'cervélo', 'cervelo', 'focus', 'santa_cruz']
    pon_display = [b.title().replace('_', ' ') for b in pon_brands if b in brands]
    selected_brands = st.sidebar.multiselect('🏷️ Select Brands', pon_display, default=[])
    selected_brands_clean = [b.lower().replace(' ', '_') for b in selected_brands]
else:
    selected_brands_clean = []

radius_km = st.sidebar.slider('📏 Coverage Radius (km)', 1.0, 15.0, 7.5, 0.5)
ze_only = st.sidebar.checkbox('🌿 Show ZE-Zones only (policy ≥ 0.8)', False)
show_rings = st.sidebar.checkbox('⭕ Show Coverage Rings', True)
show_pon_only = st.sidebar.checkbox('🎯 Show Pon Dealers Only', False)

# Data filtering
if dealers is not None:
    df = dealers.copy()
    
    # Brand filtering
    if selected_brands_clean:
        df = df[df['brand_clean'].isin(selected_brands_clean)]
    
    # Pon only filtering
    if show_pon_only:
        df = df[df.get('is_pon_dealer', False)]
    
    # ZE-zone filtering - need to map PC4 to gemeente first
    if policy_index is not None and ze_only:
        if 'pc4' in df.columns:
            # Load demographic data to get PC4->gemeente mapping
            demo = load_parquet('data/processed/demografie.parquet')
            if demo is not None and 'gemeente' in demo.columns:
                # Map PC4 to gemeente
                pc4_gemeente = demo[['pc4', 'gemeente']].drop_duplicates()
                df = df.merge(pc4_gemeente, on='pc4', how='left')
                # Now filter by ZE-zones
                df = df.merge(policy_index[['gemeente','policy_index']], on='gemeente', how='left')
                df = df[df['policy_index'].fillna(0) >= 0.8]
        
        # If we can't do the mapping, show message
        if len(df) == 0 and ze_only:
            st.sidebar.info("ZE-zone filtering requires gemeente mapping. No dealers found in ZE-zones.")

# Dashboard Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader('🗺️ Dealer Network Map')
    
    with st.expander("ℹ️ **Hoe lees je deze kaart?**"):
        st.markdown("""
        **Kleurcodering:**
        - 🔵 **Blauwe markers** = Pon dealers (Gazelle, Urban Arrow, etc.)
        - 🔴 **Rode markers** = Concurrenten (niet-Pon merken)
        
        **Markergrootte:**
        - Grote markers = Pon dealers (belangrijker voor ons netwerk)
        - Kleine markers = Concurrenten
        
        **Groene cirkels** (indien aan):
        - Tonen het servicebereik rond Pon dealers
        - Radius instelbaar via slider (standaard 7.5km)
        - Overlappende cirkels = mogelijke kannibalisatie
        
        **Tips:**
        - Klik op markers voor dealer details (naam, merk, rating)
        - Zoom in voor straatnauwkeurigheid
        - Gebruik filters links om specifieke scenario's te testen
        """)
    
    if dealers is not None and not df.empty:
        # Create map
        center = [52.2, 5.3]  # Netherlands center
        m = folium.Map(location=center, zoom_start=8, tiles='cartodbpositron')
        
        # Add dealer markers
        for _, r in df.dropna(subset=['google_lat','google_lng']).iterrows():
            is_pon = r.get('is_pon_dealer', False)
            color = '#1f77b4' if is_pon else '#d62728'
            popup_text = f"{r.get('name', 'Dealer')}<br>Brand: {r.get('brand', 'Unknown')}<br>Rating: {r.get('rating', 'N/A')}"
            
            folium.CircleMarker(
                [float(r['google_lat']), float(r['google_lng'])],
                radius=5 if is_pon else 3,
                color=color,
                fill=True,
                fillOpacity=0.8 if is_pon else 0.5,
                popup=popup_text,
                tooltip=r.get('brand', 'Dealer')
            ).add_to(m)
        
        # Add coverage rings for Pon dealers
        if show_rings and not show_pon_only:
            pon_df = df[df.get('is_pon_dealer', False)].dropna(subset=['google_lat','google_lng']).head(300)  # Limit for performance
            for _, r in pon_df.iterrows():
                lat, lng = float(r['google_lat']), float(r['google_lng'])
                folium.Circle(
                    [lat, lng], 
                    radius=radius_km*1000, 
                    color='green', 
                    fill=False, 
                    weight=1, 
                    opacity=0.3
                ).add_to(m)
        
        st_folium(m, use_container_width=True, height=600)
    else:
        st.info("No dealer data available or no dealers match current filters.")

with col2:
    st.subheader('📊 Key Metrics')
    
    if dealers is not None:
        # For proper market share, we need to load the all brands data
        dealers_all_brands = load_parquet('data/processed/dealers_all_brands.parquet')
        
        if dealers_all_brands is not None:
            # Calculate relationship-based market share (the correct metric)
            total_relationships = len(dealers_all_brands)
            pon_relationships = len(dealers_all_brands[dealers_all_brands.get('is_pon_dealer', False)]) if 'is_pon_dealer' in dealers_all_brands.columns else 0
            true_market_share = (pon_relationships / total_relationships * 100) if total_relationships > 0 else 0
            
            # Also show location-based metrics
            total_locations = len(df)
            pon_locations = len(df[df.get('is_pon_dealer', False)]) if 'is_pon_dealer' in df.columns else 0
            location_presence = (pon_locations / total_locations * 100) if total_locations > 0 else 0
            
            st.metric("Total Locations", f"{total_locations:,}")
            st.metric("Pon Locations", f"{pon_locations:,}")
            st.metric("Pon Market Share", f"{true_market_share:.1f}%", 
                     help="Based on brand-dealer relationships (22.3%)")
            st.metric("Location Presence", f"{location_presence:.1f}%",
                     help="% of locations with Pon brands (47.0%)")
        else:
            # Fallback to location-based only
            total_dealers = len(df)
            pon_dealers = len(df[df.get('is_pon_dealer', False)]) if 'is_pon_dealer' in df.columns else 0
            pon_share = (pon_dealers / total_dealers * 100) if total_dealers > 0 else 0
            
            st.metric("Total Dealers", f"{total_dealers:,}")
            st.metric("Pon Dealers", f"{pon_dealers:,}")
            st.metric("Location Presence", f"{pon_share:.1f}%",
                     help="Location-based, not true market share")
        

# White Spots Analysis
st.subheader('🎯 White Spots Analysis')

with st.expander("ℹ️ **Wat zijn white spots?**"):
    st.markdown("""
    **White spots** zijn gebieden waar Pon onvoldoende aanwezig is:
    
    **Definitie:**
    - Postcodegebieden >7.5km van dichtstbijzijnde Pon dealer
    - Ondervertegenwoordigd t.o.v. concurrentie
    - Groeipotentieel op basis van bevolkingsdichtheid
    
    **Kolommen uitleg:**
    - **pc4**: Postcode gebied
    - **gemeente**: Gemeente naam
    - **inwoners**: Aantal inwoners in dit gebied
    - **dist_nearest_pon_km**: Afstand tot dichtstbijzijnde Pon dealer
    - **score**: Prioriteitsscore (hoger = belangrijker)
    - **policy_index**: ZE-zone beleidsscore (0-1)
    - **S_dem**: Demografische geschiktheidsscore
    
    **Actiepunten:**
    - Top 10 zijn prioriteit voor netwerkuitbreiding
    - Focus op gebieden met hoge score EN veel inwoners
    - ZE-zones (policy_index > 0.8) extra belangrijk voor Urban Arrow
    """)

if white_spots is not None:
    # Filter white spots by ZE-zones if enabled
    ws = white_spots.copy()
    if ze_only and policy_index is not None and 'gemeente' in ws.columns:
        if 'policy_index' not in ws.columns:
            ws = ws.merge(policy_index[['gemeente','policy_index']], on='gemeente', how='left')
        ws = ws[ws['policy_index'].fillna(0) >= 0.8]
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.write("**Top White Spots (Areas Underserved by Pon Dealers)**")
        display_cols = [c for c in ['pc4','gemeente','inwoners','dist_nearest_pon_km','score','policy_index','score_policy','S_dem'] 
                       if c in ws.columns]
        
        if display_cols:
            # Format the dataframe for display
            ws_display = ws[display_cols].head(20).copy()
            if 'dist_nearest_pon_km' in ws_display.columns:
                ws_display['dist_nearest_pon_km'] = ws_display['dist_nearest_pon_km'].round(1)
            if 'policy_index' in ws_display.columns:
                ws_display['policy_index'] = ws_display['policy_index'].round(2)
            
            st.dataframe(ws_display, use_container_width=True)
        else:
            st.info("White spots data available but missing expected columns.")
    
    with col4:
        if len(ws) > 0:
            st.metric("Total White Spots", f"{len(ws):,}")
            total_underserved = ws['inwoners'].sum() if 'inwoners' in ws.columns else 0
            st.metric("Underserved Population", f"{total_underserved:,}")
            
            if 'dist_nearest_pon_km' in ws.columns:
                avg_distance = ws['dist_nearest_pon_km'].mean()
                st.metric("Avg Distance to Pon", f"{avg_distance:.1f} km")
else:
    st.info("Run `notebooks/02_coverage.ipynb` to generate white spots analysis.")

# KPI Overview
if gemeente_kpis is not None:
    st.subheader('🏘️ Municipality KPIs')
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.write("**Top 10 Best Served Municipalities**")
        top_served = gemeente_kpis.nlargest(10, 'dealers_per_100k')[['gemeente', 'dealers_per_100k', 'pon_share']]
        st.dataframe(top_served, use_container_width=True)
    
    with col6:
        st.write("**Top 10 Underserved Municipalities**") 
        underserved = gemeente_kpis.nsmallest(10, 'dealers_per_100k')[['gemeente', 'dealers_per_100k', 'pon_share']]
        st.dataframe(underserved, use_container_width=True)

# Proximity Analysis
if proximity_kpis is not None:
    st.subheader('🔄 Cannibalization Analysis')
    
    with st.expander("ℹ️ **Wat is kannibalisatie?**"):
        st.markdown("""
        **Kannibalisatie** meet hoeveel dealers elkaar beconcurreren:
        
        **Pon-to-Pon (Interne Competitie):**
        - Aantal andere Pon dealers binnen bepaalde afstand
        - Hoge waarden = dealers "vechten" om dezelfde klanten
        - Ideaal: 3-5 dealers binnen 10km (service zonder overlap)
        - Probleem bij >8 dealers binnen 7.5km
        
        **Pon-to-Competitor (Externe Competitie):**
        - Aantal concurrent dealers binnen bepaalde afstand
        - Hoge waarden = sterke marktconcurrentie
        - Benchmark: gemiddeld 12.8 concurrenten binnen 10km
        
        
        **Interpretatie:**
        - Interne > Externe = veel eigen dealers (Union/Gazelle)
        - Externe > Interne = gezonde marktpositie
        - Beiden hoog = verzadigde markt (Randstad)
        """)
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.write("**Pon-to-Pon Proximity (Internal Competition)**")
        st.dataframe(proximity_kpis[['ring_km', 'pon_near_pon']], use_container_width=True)
    
    with col8:
        st.write("**Pon-to-Competitor Proximity (External Competition)**") 
        st.dataframe(proximity_kpis[['ring_km', 'pon_near_nonpon']], use_container_width=True)



# Footer with instructions
st.markdown("---")
st.caption("""
**📝 Usage Instructions:**
- Use sidebar filters to explore different brand combinations and coverage scenarios
- Toggle ZE-zones to see policy-aligned opportunities
- Coverage rings show 7.5km radius around Pon dealers
- White spots indicate areas >7.5km from nearest Pon dealer
- Download CSV files for detailed analysis

**🔄 Data Refresh:** Run notebooks in order (01→02→03→04→05) to update analysis
""")

# Debug info (hidden by default)
with st.expander("🔍 Debug Information"):
    st.write("**Data Loading Status:**")
    st.write(f"- Dealers: {'✅ Loaded' if dealers is not None else '❌ Missing'}")
    st.write(f"- White Spots: {'✅ Loaded' if white_spots is not None else '❌ Missing'}")
    st.write(f"- Municipality KPIs: {'✅ Loaded' if gemeente_kpis is not None else '❌ Missing'}")
    st.write(f"- Coverage Data: {'✅ Loaded' if coverage_overall is not None else '❌ Missing'}")
    st.write(f"- Policy Index: {'✅ Loaded' if policy_index is not None else '❌ Missing'}")
    st.write(f"- Proximity KPIs: {'✅ Loaded' if proximity_kpis is not None else '❌ Missing'}")
    st.write(f"- International Data: {'✅ Loaded' if ua_intl is not None else '❌ Missing'}")
    
    if dealers is not None:
        st.write(f"**Filtered Data:** {len(df):,} dealers shown")
        if 'brand_clean' in df.columns:
            brand_counts = df['brand_clean'].value_counts()
            st.write("**Brand Distribution:**")
            st.write(brand_counts)
