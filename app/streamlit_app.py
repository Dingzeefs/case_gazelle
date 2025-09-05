
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title='Pon Bike – Dealer Network', layout='wide')
st.title('Pon Bike – Dealer Network Explorer')

radius_km = st.sidebar.slider('Radius (km)', 5.0, 12.0, 7.5, 0.5)
brand = st.sidebar.multiselect('Merken (PON)', ['Gazelle','Cannondale','Kalkhoff','Urban Arrow','Cervélo','Focus','Santa Cruz'])
ze_only = st.sidebar.checkbox('Toon alleen ZE-steden (policy)', value=False)

try:
    dealers = pd.read_parquet('data/processed/dealers.parquet')
except Exception:
    dealers = pd.read_csv('dealer_lijst.csv')

if 'brand_clean' in dealers.columns and brand:
    dealers = dealers[dealers['brand_clean'].isin([b.lower() for b in brand])]

lat = dealers['google_lat'].dropna().astype(float).median() if 'google_lat' in dealers else 52.1
lng = dealers['google_lng'].dropna().astype(float).median() if 'google_lng' in dealers else 5.3
m = folium.Map(location=[lat, lng], zoom_start=7)

for _, r in dealers.dropna(subset=['google_lat','google_lng']).iterrows():
    color = 'blue' if r.get('is_pon_dealer', False) else 'gray'
    folium.CircleMarker([float(r['google_lat']), float(r['google_lng'])], radius=3, color=color, fill=True, fill_opacity=0.7).add_to(m)

st_folium(m, width=1100, height=700)

# Policy-aware white spots table
ws_path = 'outputs/tables/white_spots_with_policy.csv'
ws_base = 'outputs/tables/white_spots_ranked.csv'
pol_path = 'outputs/tables/policy_index.csv'
try:
    ws = pd.read_csv(ws_path)
except Exception:
    try:
        ws = pd.read_csv(ws_base)
    except Exception:
        ws = None

st.subheader('White-spots (policy-aware indien beschikbaar)')
if ws is not None:
    # Attach gemeente/policy if possible
    if 'policy_index' not in ws.columns and pd.io.common.file_exists(pol_path):
        try:
            pol = pd.read_csv(pol_path)
            # if ws has gemeente column, join; otherwise show without
            if 'gemeente' in ws.columns:
                ws = ws.merge(pol[['gemeente','policy_index']], on='gemeente', how='left')
        except Exception:
            pass
    # Filter ZE-only if gemeente available
    if ze_only and 'policy_index' in ws.columns:
        ws = ws[ws['policy_index'].fillna(0) >= 0.8]
    # Show top rows
    cols = [c for c in ['pc4','gemeente','inwoners','dist_nearest_pon_km','score','policy_index','score_policy'] if c in ws.columns]
    st.dataframe(ws[cols].head(50))
else:
    st.info('Run notebooks/02_coverage.ipynb en src/build_policy_index.py om white-spots en policy te genereren.')

st.caption('Tip: run notebooks/02_coverage.ipynb voor white-spots en proximity KPI\'s. Policy: src/build_policy_index.py.')
