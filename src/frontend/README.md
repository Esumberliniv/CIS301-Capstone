# Frontend - Streamlit Dashboard

This directory will contain the Streamlit dashboard for visualizing IGS data.

## Planned Architecture

```
frontend/
├── app.py                  # Main dashboard entry point
├── pages/
│   ├── 1_Equity_Map.py    # Interactive choropleth map
│   ├── 2_Gap_Analysis.py  # Comparative analysis view
│   └── 3_Correlations.py  # Correlation explorer
├── components/
│   ├── filters.py         # Reusable filter widgets
│   ├── charts.py          # Chart generation functions
│   └── maps.py            # Map visualization functions
├── utils.py               # Helper functions
├── config.py              # Configuration (API URL)
├── requirements.txt       # Python dependencies
└── assets/
    ├── styles.css         # Custom CSS styling
    └── logo.png           # Project logo
```

## Dashboard Pages Overview

### Home Page (app.py)
**Purpose:** Project overview and navigation

**Components:**
- Project title and description
- Key metrics summary cards
- Quick statistics (total tracts, states covered, date range)
- Navigation to main analysis pages

### Page 1: The Equity Map
**Purpose:** Geographic visualization of economic inclusion

**Features:**
- Interactive choropleth map (Plotly/Folium)
- Filters:
  - State dropdown
  - County dropdown (dependent on state)
  - Year slider (2017-2024)
  - Metric selector (IGS, Internet Access, Minority Business, etc.)
- Color-coded census tracts by score
- Hover tooltips showing detailed metrics
- Click to view tract details

**Visualization:**
```python
# Pseudocode
map = folium.Map(location=[39.8, -98.6], zoom_start=4)
for tract in tracts:
    color = get_color(tract.score)
    folium.GeoJson(
        tract.geometry,
        style_function=lambda x: {'fillColor': color}
    ).add_to(map)
```

### Page 2: The Opportunity Gap Analysis
**Purpose:** Compare census tracts against state averages

**Features:**
- Census tract search/selector
- Selected tract profile card
  - FIPS code, county, state
  - Summary scores
- Bar charts comparing:
  - Tract value vs. State average
  - Multiple metrics side-by-side
- Gap calculation (percentage above/below average)
- Historical trend line chart (2017-2024)

**Visualization:**
```python
# Pseudocode
fig = px.bar(
    x=['Internet Access', 'Minority Business', 'Affordable Housing'],
    y=[tract_values, state_averages],
    barmode='group',
    title='Tract vs. State Average'
)
```

### Page 3: Correlation Explorer
**Purpose:** Analyze relationships between metrics

**Features:**
- Two metric selectors (X-axis, Y-axis)
- State filter (optional)
- Year range slider
- Scatter plot with trendline
- Correlation coefficient display
- Insights panel:
  - "Strong positive correlation (r=0.78)"
  - "Areas with high Internet Access tend to have higher Small Business Loan scores"

**Visualization:**
```python
# Pseudocode
fig = px.scatter(
    x=metric1_values,
    y=metric2_values,
    trendline='ols',
    hover_data=['county', 'state']
)
```

## API Integration

### API Client (utils.py)

```python
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/api"

@st.cache_data(ttl=600)
def get_tracts(state=None, year=None):
    """Fetch census tracts from API."""
    params = {}
    if state:
        params['state'] = state
    if year:
        params['year'] = year
    response = requests.get(f"{API_BASE_URL}/tracts", params=params)
    return response.json()

@st.cache_data(ttl=600)
def get_states():
    """Fetch list of states."""
    response = requests.get(f"{API_BASE_URL}/states")
    return response.json()
```

## UI/UX Design Principles

1. **Simplicity:** Clean, uncluttered interface
2. **Responsiveness:** Fast loading with caching
3. **Accessibility:** High contrast, clear labels
4. **Guidance:** Help text and tooltips
5. **Framing:** Emphasize "opportunity potential" not "deficits"

## Styling

### Custom CSS (assets/styles.css)

```css
/* Color scheme based on equity theme */
:root {
    --primary-color: #2E86AB;      /* Blue - trust, stability */
    --secondary-color: #A23B72;    /* Purple - creativity */
    --accent-color: #F18F01;       /* Orange - opportunity */
    --success-color: #5FA777;      /* Green - growth */
    --warning-color: #E63946;      /* Red - gaps */
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Score indicators */
.score-high { color: var(--success-color); }
.score-medium { color: var(--accent-color); }
.score-low { color: var(--warning-color); }
```

## Development Commands (Future)

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard (development)
streamlit run app.py

# Run dashboard (production)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Clear cache
streamlit cache clear
```

## Dependencies (requirements.txt - planned)

```
streamlit==1.29.0
plotly==5.18.0
folium==0.15.0
streamlit-folium==0.15.1
pandas==2.1.3
requests==2.31.0
matplotlib==3.8.2
seaborn==0.13.0
numpy==1.26.2
```

## Example Dashboard Layout

```
┌────────────────────────────────────────────────────┐
│  EQUITY IN FOCUS 🎯                       [Filters]│
├────────────────────────────────────────────────────┤
│  Overview                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         │
│  │ 32   │  │  4   │  │ 2017 │  │ 2024 │         │
│  │Tracts│  │States│  │-2024 │  │ Year │         │
│  └──────┘  └──────┘  └──────┘  └──────┘         │
├────────────────────────────────────────────────────┤
│  Pages:                                            │
│  → 🗺️  Equity Map                                │
│  → 📊 Opportunity Gap Analysis                    │
│  → 🔗 Correlation Explorer                        │
└────────────────────────────────────────────────────┘
```

---

**Status:** Planning Phase  
**Next Steps:** Build basic Streamlit app structure and API integration  
**Developer:** Emery

