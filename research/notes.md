
# Research notes – externe voorbeelden (kort)

## Starbucks vs Ediya (proximity/overlap)
- Methode: Haversine + KD‑Tree; bins (0.1/0.3/0.5/1/3/5 km); folium/histogram.
- Relevantie: meet co‑locatie en saturatie; vertaalbaar naar dealers Pon vs niet‑Pon.
- Toevoeging aan KPIs: % niet‑Pon binnen 1/3/5/7.5 km; NN‑afstand‑verdeling; saturatie‑index.

## GNN‑site selection (luxury auto)
- Idee: nodes=regio’s, edges=adjacentie/reistijd; features=demografie+dealers+concurrentie.
- Voor nu: parkeer in roadmap; eerst simpele baseline (logit/XGB) voor ranking.

## CSR/policy haakjes
- Stedelijke leefbaarheid, emissievrij (UA), lokale economie; benutten in portfolio‑adviezen.

Bronnen (korte verwijzing): GitHub proximity‑analyse (Seoul coffee), GNN dealership selection paper/repo.


## Policy/ZE & Benchmarks (kort)
- ZE‑zones verhogen adoptie UA/e‑city → zwaarder wegen in score
- Benchmarks: UA‑dekking als lat; stedelijk target ~85%, ruraal ~70% (placeholder, vervang met NL‑meting)

## Proximity (300 m/500 m)
- 300 m = interne kannibalisatie‑risico; 500 m = concurrent‑nabijheid
- KPI’s en visuals integreren in backup en rapport

## H3 (optioneel, roadmap)
- Res 8–9; features per cel; potential heatmap + top‑N ranking
