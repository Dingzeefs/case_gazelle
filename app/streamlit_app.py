
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
# Force clear cache and try to load the dashboard-optimized version first
if Path('data/processed/dealers_dashboard.parquet').exists():
    dealers = pd.read_parquet('data/processed/dealers_dashboard.parquet')
    st.write("✅ **Loaded enhanced dashboard data**")
else:
    # Fallback to original dealers data
    dealers = load_parquet('data/processed/dealers.parquet')
    if dealers is None:
        dealers = load_csv('data/raw/dealer_lijst.csv')
    st.write("⚠️ **Using fallback dealer data**")

white_spots = load_csv('outputs/tables/white_spots_with_policy.csv')
if white_spots is None:
    white_spots = load_csv('outputs/tables/white_spots_ranked.csv')

gemeente_kpis = load_csv('outputs/tables/kpi_overview.csv')
coverage_overall = load_csv('outputs/tables/coverage_overall.csv')
policy_index = load_csv('outputs/tables/policy_index.csv')
proximity_kpis = load_csv('outputs/tables/proximity_kpis.csv')
ua_intl = load_csv('outputs/tables/ua_intl_shortlist.csv')

# Enhanced Sidebar Filters
if dealers is not None:
    # Check if we have brand_clean column (relationship data) or brands_display (dashboard data)
    if 'brand_clean' in dealers.columns:
        brands = sorted([b for b in dealers['brand_clean'].dropna().unique() if b])
        pon_brands = ['gazelle', 'cannondale', 'union', 'kalkhoff', 'urban_arrow', 'cervélo', 'cervelo', 'focus', 'santa_cruz']
        pon_display = [b.title().replace('_', ' ') for b in pon_brands if b in brands]
        selected_brands = st.sidebar.multiselect('🏷️ Select Brands', pon_display, default=[])
        selected_brands_clean = [b.lower().replace(' ', '_') for b in selected_brands]
    elif 'pon_brands_display' in dealers.columns:
        # Dashboard data - get unique Pon brands from pon_brands_display
        all_pon_brands = set()
        for brands_str in dealers['pon_brands_display'].dropna():
            if brands_str:
                all_pon_brands.update([b.strip() for b in brands_str.split(',')])
        pon_display = sorted([b.title().replace('_', ' ') for b in all_pon_brands if b])
        selected_brands = st.sidebar.multiselect('🏷️ Select Brands', pon_display, default=[])
        selected_brands_clean = [b.lower().replace(' ', '_') for b in selected_brands]
    else:
        selected_brands_clean = []
else:
    selected_brands_clean = []

radius_km = st.sidebar.slider('📏 Coverage Radius (km)', 1.0, 15.0, 7.5, 0.5)
ze_only = st.sidebar.checkbox('🌿 Show ZE-Zones only (policy ≥ 0.8)', False)
show_rings = st.sidebar.checkbox('⭕ Show Coverage Rings', True)
show_pon_only = st.sidebar.checkbox('🎯 Show Pon Dealers Only', False)

# Data filtering
if dealers is not None:
    df = dealers.copy()
    
    # --- Normalize columns for fallback datasets ---
    # Ensure a unified schema regardless of source (dashboard parquet, dealers.parquet, raw CSV)
    # 1) Name
    if 'name' not in df.columns and 'google_name' in df.columns:
        df['name'] = df['google_name']
    
    # 2) Ratings
    if 'rating' not in df.columns and 'google_rating' in df.columns:
        df['rating'] = df['google_rating']
    if 'n_reviews' not in df.columns and 'google_user_ratings_total' in df.columns:
        df['n_reviews'] = df['google_user_ratings_total']
    
    # 3) is_pon_dealer
    if 'is_pon_dealer' not in df.columns:
        pon_set = {
            'gazelle', 'cannondale', 'union', 'kalkhoff', 'urban_arrow', 'cervélo', 'cervelo', 'focus', 'santa_cruz'
        }
        if 'brand_clean' in df.columns:
            df['is_pon_dealer'] = df['brand_clean'].astype(str).str.lower().isin(pon_set)
        elif 'brand' in df.columns:
            df['is_pon_dealer'] = df['brand'].astype(str).str.lower().str.replace(' ', '_', regex=False).isin(pon_set)
        else:
            df['is_pon_dealer'] = False
    
    # Brand filtering
    if selected_brands_clean:
        if 'brand_clean' in df.columns:
            # Relationship data filtering
            df = df[df['brand_clean'].isin(selected_brands_clean)]
        elif 'pon_brands_display' in df.columns:
            # Dashboard data filtering - check if any selected brands are in the pon_brands_display
            def has_selected_brand(brands_str):
                if brands_str is None or brands_str == '' or pd.isna(brands_str):
                    return False
                brands_list = [b.strip().lower().replace(' ', '_') for b in brands_str.split(',')]
                return any(brand in selected_brands_clean for brand in brands_list)
            
            df = df[df['pon_brands_display'].apply(has_selected_brand)]
    
    # Pon only filtering
    if show_pon_only:
        df = df[df.get('is_pon_dealer', False)]
    
    # ZE-zone filtering - need to map PC4 to gemeente first
    if policy_index is not None and ze_only:
        try:
            # Check if we already have gemeente column from dashboard data
            if 'gemeente' in df.columns:
                # Direct merge with policy_index
                if 'gemeente' in policy_index.columns:
                    df = df.merge(policy_index[['gemeente','policy_index']], on='gemeente', how='left')
                    df = df[df['policy_index'].fillna(0) >= 0.8]
                else:
                    st.sidebar.warning("Policy index missing gemeente column - ZE-zone filter disabled")
            elif 'pc4' in df.columns:
                # Load demographic data to get PC4->gemeente mapping
                demo = load_parquet('data/processed/demografie.parquet')
                if demo is not None and 'gemeente' in demo.columns:
                    # Map PC4 to gemeente
                    pc4_gemeente = demo[['pc4', 'gemeente']].drop_duplicates()
                    df = df.merge(pc4_gemeente, on='pc4', how='left')
                    # Now filter by ZE-zones
                    if 'gemeente' in policy_index.columns:
                        df = df.merge(policy_index[['gemeente','policy_index']], on='gemeente', how='left')
                        df = df[df['policy_index'].fillna(0) >= 0.8]
                    else:
                        st.sidebar.warning("Policy index missing gemeente column - ZE-zone filter disabled")
                else:
                    st.sidebar.warning("Cannot map PC4 to gemeente - ZE-zone filter disabled")
            else:
                st.sidebar.warning("No geographic data available - ZE-zone filter disabled")
            
            # Show info if no results
            if len(df) == 0 and ze_only:
                st.sidebar.info("No dealers found in ZE-zones with policy ≥ 0.8")
        except Exception as e:
            st.sidebar.error(f"ZE-zone filtering error: {str(e)}")
            # Continue without ZE-zone filtering

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
        
        # Group by unique location to handle multi-brand dealers
        # First ensure we have the necessary columns
        required_cols = ['google_lat', 'google_lng', 'name']
        if all(col in df.columns for col in required_cols):
            # Safe groupby with explicit aggregation for each column
            agg_dict = {'name': 'first'}
            if 'is_pon_dealer' in df.columns:
                agg_dict['is_pon_dealer'] = 'any'
            
            # Add brand aggregation - prefer brands_display if available
            if 'brands_display' in df.columns:
                agg_dict['brands_display'] = 'first'
            elif 'brand' in df.columns:
                agg_dict['brand'] = lambda x: ', '.join(sorted(set(str(b) for b in x if pd.notna(b))))
            
            # Add rating aggregation if exists
            if 'rating' in df.columns:
                agg_dict['rating'] = lambda x: x.iloc[0] if len(x) > 0 and pd.notna(x.iloc[0]) else None
            
            if 'n_reviews' in df.columns:
                agg_dict['n_reviews'] = lambda x: x.iloc[0] if len(x) > 0 and pd.notna(x.iloc[0]) else 0
            
            location_groups = df.dropna(subset=['google_lat','google_lng']).groupby(
                ['google_lat', 'google_lng'], as_index=False
            ).agg(agg_dict)
        else:
            # Fallback if columns are missing
            location_groups = df.dropna(subset=['google_lat','google_lng'])
        
        # Add dealer markers
        for _, r in location_groups.iterrows():
            is_pon = r.get('is_pon_dealer', False)
            color = '#1f77b4' if is_pon else '#d62728'
            
            # Format dealer name
            dealer_name = str(r.get('name', 'Dealer'))
            
            # Format brands - use enhanced display columns if available
            if 'brands_display' in location_groups.columns and not pd.isna(r.get('brands_display')):
                brands = r.get('brands_display', 'Unknown')
            elif 'brand' in location_groups.columns:
                brands = r.get('brand', 'Unknown')
            else:
                brands = 'Unknown'
            
            if pd.isna(brands) or brands == '':
                brands = 'Unknown'
            
            # Format rating with proper handling
            rating = r.get('rating', None)
            n_reviews = r.get('n_reviews', 0)
            
            if rating is not None and not pd.isna(rating) and float(rating) > 0:
                rating_text = f"{float(rating):.1f} ({int(n_reviews)} reviews)"
            else:
                rating_text = "No rating"
            
            # Create popup text
            popup_text = f"""<b>{dealer_name}</b><br>
            Brands: {brands}<br>
            Rating: {rating_text}"""
            
            # Create tooltip
            brand_count = len(str(brands).split(', ')) if brands != 'Unknown' else 0
            tooltip_text = f"{dealer_name}"
            if brand_count > 1:
                tooltip_text += f" ({brand_count} brands)"
            
            folium.CircleMarker(
                [float(r['google_lat']), float(r['google_lng'])],
                radius=5 if is_pon else 3,
                color=color,
                fill=True,
                fillOpacity=0.8 if is_pon else 0.5,
                popup=popup_text,
                tooltip=tooltip_text
            ).add_to(m)
        
        # Add coverage rings for Pon dealers
        if show_rings and not show_pon_only:
            pon_df = df[df.get('is_pon_dealer', False)].dropna(subset=['google_lat','google_lng'])  # All Pon dealers
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
        display_cols = [c for c in ['pc4','gemeente','inwoners','dist_nearest_pon_km','score','policy_index','score_policy'] 
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

# Multi-Brand Network Analytics
st.subheader('🏢 Multi-Brand Network Analytics')


# Check if we have the dashboard data with multi-brand info
if dealers is not None and 'n_brands' in df.columns and 'dealer_type' in df.columns:
    import plotly.express as px
    
    st.write(f"**Analyzing {len(df):,} dealer locations**")
    
    # Create two columns for the main charts
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Dealer Type Distribution
        dealer_counts = df['dealer_type'].value_counts()
        fig_pie = px.pie(
            values=dealer_counts.values,
            names=dealer_counts.index,
            title="Dealer Network Composition",
            color_discrete_map={
                'Non-Pon': '#e74c3c',
                'Single Pon': '#3498db', 
                'Multi Pon': '#f39c12'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Show key stats
        pon_dealers = len(df[df['is_pon_dealer']])
        multi_pon = len(df[df['dealer_type'] == 'Multi Pon'])
        st.metric("Pon Dealers", f"{pon_dealers:,}")
        st.metric("Multi-Pon Risk", f"{multi_pon:,}")
    
    with col2:
        # 2. Brands per Location Distribution
        brand_dist = df['n_brands'].value_counts().sort_index()[:10]  # Top 10 to avoid clutter
        fig_bar = px.bar(
            x=brand_dist.index,
            y=brand_dist.values,
            title="Brand Diversity Distribution",
            labels={'x': 'Brands per Location', 'y': 'Number of Dealers'},
            color_discrete_sequence=['#3498db']
        )
        fig_bar.update_layout(showlegend=False, xaxis_title="Brands per Location", yaxis_title="Number of Dealers")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Show diversity metrics
        avg_brands = df['n_brands'].mean()
        max_brands = df['n_brands'].max()
        multi_brand_pct = (df['n_brands'] > 1).mean() * 100
        st.metric("Avg Brands/Location", f"{avg_brands:.1f}")
        st.metric("Multi-Brand Locations", f"{multi_brand_pct:.1f}%")
    
    # 3. Provincial Analysis (if available)
    if 'provincie' in df.columns and df['provincie'].notna().sum() > 5:
        st.write("### 🗺️ Provincial Market Penetration")
        st.write("*Toont het percentage van alle fietsdealers per provincie die Pon-dealers zijn. Hogere percentages geven een sterkere marktpositie aan.*")
        
        # Calculate provincial metrics
        prov_data = df[df['provincie'].notna()].groupby('provincie').agg({
            'google_place_id': 'count',
            'is_pon_dealer': ['sum', 'mean']
        }).round(2)
        
        prov_data.columns = ['total_dealers', 'pon_dealers', 'pon_penetration']
        prov_data['penetration_pct'] = prov_data['pon_penetration'] * 100
        prov_data = prov_data.sort_values('penetration_pct', ascending=True)
        
        # Create horizontal bar chart
        fig_prov = px.bar(
            x=prov_data['penetration_pct'],
            y=prov_data.index,
            orientation='h',
            title="Pon Market Penetration by Province",
            labels={'x': 'Market Penetration (%)', 'y': 'Province'},
            color=prov_data['penetration_pct'],
            color_continuous_scale='RdYlGn',
            text=prov_data['penetration_pct'].round(1)
        )
        fig_prov.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_prov.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_prov, use_container_width=True)
        
        # Show top/bottom provinces
        st.write(f"**🏆 Highest Penetration:** {prov_data.tail(3).index.tolist()}")
        st.write(f"**🎯 Growth Opportunities:** {prov_data.head(3).index.tolist()}")
    
    # 4. Pon Brand Performance (if we have brand data)
    if 'pon_brands_display' in df.columns:
        st.write("### 🏆 Pon Brand Network Size")
        st.write("*Aantal dealerlocaties per Pon-merk. Merken met een groter netwerk hebben betere marktdekking en toegankelijkheid voor klanten.*")
        
        # Count Pon brand presence
        pon_brand_counts = {}
        for _, row in df[df['is_pon_dealer']].iterrows():
            brands = str(row.get('pon_brands_display', ''))
            if brands and brands != 'nan':
                for brand in brands.split(','):
                    brand = brand.strip().title()
                    if brand:
                        pon_brand_counts[brand] = pon_brand_counts.get(brand, 0) + 1
        
        if pon_brand_counts:
            # Create DataFrame and sort
            brands_df = pd.DataFrame(list(pon_brand_counts.items()), columns=['Brand', 'Locations'])
            brands_df = brands_df.sort_values('Locations', ascending=True)
            
            # Create horizontal bar chart
            fig_brands = px.bar(
                brands_df,
                x='Locations',
                y='Brand',
                orientation='h',
                title="Pon Brand Dealer Network",
                labels={'Locations': 'Number of Dealer Locations', 'Brand': 'Pon Brand'},
                color='Locations',
                color_continuous_scale='Blues',
                text='Locations'
            )
            fig_brands.update_traces(texttemplate='%{text}', textposition='outside')
            fig_brands.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_brands, use_container_width=True)

else:
    st.info("📊 Multi-brand analytics require the enhanced dataset from notebook 07.")

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

