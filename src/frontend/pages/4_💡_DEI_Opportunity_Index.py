"""
DEI Opportunity Index Page
CIS 301 Capstone Project - Clark Atlanta CIS301

Simple view to identify which counties are best for DEI and opportunity growth
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add frontend directory to path
frontend_path = Path(__file__).parent.parent
sys.path.insert(0, str(frontend_path))

from utils.api_client import api_client
from config import PAGE_TITLE, LAYOUT

# Page configuration
st.set_page_config(
    page_title=f"{PAGE_TITLE} - DEI Opportunity Index",
    page_icon="💡",
    layout=LAYOUT
)

# Custom CSS
st.markdown("""
<style>
    .dei-score-excellent { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; padding: 1rem; border-radius: 12px; text-align: center;
    }
    .dei-score-good { 
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white; padding: 1rem; border-radius: 12px; text-align: center;
    }
    .dei-score-moderate { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white; padding: 1rem; border-radius: 12px; text-align: center;
    }
    .dei-score-developing { 
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white; padding: 1rem; border-radius: 12px; text-align: center;
    }
    .county-card {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        background: white;
    }
    .rank-badge {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .metric-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    .pill-high { background: #d1fae5; color: #065f46; }
    .pill-medium { background: #fef3c7; color: #92400e; }
    .pill-low { background: #fee2e2; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💡 DEI Opportunity Index")
st.markdown("""
**Which counties are best for DEI and economic opportunity?**  
This index ranks all counties in the dataset by their potential for inclusive growth and diversity-friendly business environments.
""")

st.markdown("---")


def calculate_dei_opportunity_score(row):
    """
    Calculate a DEI Opportunity Score (0-100) based on key metrics
    
    Components weighted by DEI relevance:
    - Minority/Women-Owned Businesses (25%) - Direct DEI indicator
    - Inclusive Growth Score (20%) - Overall inclusion measure
    - Internet Access (15%) - Digital equity
    - Affordable Housing (15%) - Economic accessibility
    - Personal Income (10%) - Economic opportunity
    - Health Insurance (10%) - Social safety net
    - New Businesses (5%) - Entrepreneurship opportunity
    """
    weights = {
        'minority_women_owned_businesses_score': 0.25,
        'inclusive_growth_score': 0.20,
        'internet_access_score': 0.15,
        'affordable_housing_score': 0.15,
        'personal_income_score': 0.10,
        'health_insurance_coverage_score': 0.10,
        'new_businesses_score': 0.05
    }
    
    total_weight = 0
    weighted_sum = 0
    
    for metric, weight in weights.items():
        value = row.get(metric)
        if pd.notna(value) and value is not None:
            weighted_sum += value * weight
            total_weight += weight
    
    if total_weight > 0:
        return weighted_sum / total_weight
    return None


def get_score_category(score):
    """Categorize DEI Opportunity Score"""
    if score is None:
        return "Unknown", "❓"
    elif score >= 65:
        return "Excellent", "🌟"
    elif score >= 50:
        return "Good", "✅"
    elif score >= 40:
        return "Moderate", "📊"
    else:
        return "Developing", "📈"


def get_score_class(score):
    """Get CSS class for score styling"""
    if score is None:
        return ""
    elif score >= 65:
        return "dei-score-excellent"
    elif score >= 50:
        return "dei-score-good"
    elif score >= 40:
        return "dei-score-moderate"
    else:
        return "dei-score-developing"


# Fetch DEI Opportunity data from API
try:
    with st.spinner("Loading DEI Opportunity rankings across all counties..."):
        # Use the dedicated DEI opportunity endpoint
        dei_data = api_client.get_dei_opportunity_rankings()
        
        rankings = dei_data.get('rankings', [])
        year = dei_data.get('year', 2024)
        
        if not rankings:
            st.error("No data found. Please ensure the backend is running and database has data.")
            st.stop()
        
        st.info(f"📅 Analyzing data from **{year}** (most recent year available)")
        
        # Convert to DataFrame
        county_scores = pd.DataFrame(rankings)
        
        # Flatten metrics into columns
        for metric in ['inclusive_growth_score', 'minority_women_owned_businesses_score', 
                       'internet_access_score', 'affordable_housing_score', 
                       'personal_income_score', 'health_insurance_coverage_score', 
                       'new_businesses_score']:
            county_scores[metric] = county_scores['metrics'].apply(lambda x: x.get(metric))
        
        # Rename columns for display
        county_scores = county_scores.rename(columns={
            'county': 'County',
            'state': 'State', 
            'dei_score': 'DEI Score',
            'category': 'Category',
            'rank': 'Rank',
            'tract_count': 'Tract Count',
            'inclusive_growth_score': 'IGS',
            'minority_women_owned_businesses_score': 'Minority/Women Biz',
            'internet_access_score': 'Internet Access',
            'affordable_housing_score': 'Affordable Housing',
            'personal_income_score': 'Personal Income',
            'health_insurance_coverage_score': 'Health Insurance',
            'new_businesses_score': 'New Businesses'
        })
        
        # Add Icon
        county_scores['Icon'] = county_scores['DEI Score'].apply(lambda x: get_score_category(x)[1])

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the backend API is running at http://localhost:8000")
    st.stop()

# ==================== MAIN DASHBOARD ====================

# Summary Stats
st.markdown("## 📊 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Counties Analyzed", len(county_scores))

with col2:
    st.metric("States Covered", county_scores['State'].nunique())

with col3:
    avg_score = county_scores['DEI Score'].mean()
    st.metric("Average DEI Score", f"{avg_score:.1f}")

with col4:
    top_score = county_scores['DEI Score'].max()
    st.metric("Highest DEI Score", f"{top_score:.1f}")

st.markdown("---")

# ==================== COUNTY RANKINGS ====================

st.markdown("## 🏆 County Rankings by DEI Opportunity")

# Quick filters
col1, col2 = st.columns([2, 1])

with col1:
    category_filter = st.multiselect(
        "Filter by Category",
        ["Excellent", "Good", "Moderate", "Developing"],
        default=["Excellent", "Good", "Moderate", "Developing"]
    )

with col2:
    sort_by = st.selectbox(
        "Sort By",
        ["DEI Score", "Minority/Women Biz", "Internet Access", "Affordable Housing", "IGS"]
    )

# Apply filters
filtered_df = county_scores[county_scores['Category'].isin(category_filter)]
filtered_df = filtered_df.sort_values(sort_by, ascending=False)

# Display rankings
for idx, row in filtered_df.iterrows():
    rank = row['Rank']
    score = row['DEI Score']
    category, icon = get_score_category(score)
    
    # Medal for top 3
    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"
    else:
        medal = f"#{rank}"
    
    col1, col2, col3 = st.columns([1, 3, 2])
    
    with col1:
        st.markdown(f"""
        <div class="{get_score_class(score)}" style="height: 100%;">
            <div style="font-size: 2rem; font-weight: bold;">{medal}</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{score:.0f}</div>
            <div>{category}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {row['County']}")
        st.markdown(f"📍 **{row['State']}**")
        
        # Key metrics as pills
        metrics_html = ""
        
        mwb = row['Minority/Women Biz']
        if pd.notna(mwb):
            pill_class = "pill-high" if mwb >= 60 else "pill-medium" if mwb >= 40 else "pill-low"
            metrics_html += f'<span class="metric-pill {pill_class}">Minority/Women Biz: {mwb:.0f}</span> '
        
        internet = row['Internet Access']
        if pd.notna(internet):
            pill_class = "pill-high" if internet >= 60 else "pill-medium" if internet >= 40 else "pill-low"
            metrics_html += f'<span class="metric-pill {pill_class}">Internet: {internet:.0f}</span> '
        
        housing = row['Affordable Housing']
        if pd.notna(housing):
            pill_class = "pill-high" if housing >= 60 else "pill-medium" if housing >= 40 else "pill-low"
            metrics_html += f'<span class="metric-pill {pill_class}">Housing: {housing:.0f}</span> '
        
        st.markdown(metrics_html, unsafe_allow_html=True)
    
    with col3:
        # Mini radar chart showing key metrics
        metrics_for_radar = ['Minority/Women Biz', 'Internet Access', 'Affordable Housing', 
                            'Personal Income', 'Health Insurance']
        values = [row[m] if pd.notna(row[m]) else 0 for m in metrics_for_radar]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=metrics_for_radar + [metrics_for_radar[0]],
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                angularaxis=dict(showticklabels=False)
            ),
            showlegend=False,
            height=150,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

# ==================== COMPARISON CHART ====================

st.markdown("## 📈 Visual Comparison")

# Bar chart of all counties
fig = go.Figure()

colors = [
    '#10b981' if s >= 65 else '#3b82f6' if s >= 50 else '#f59e0b' if s >= 40 else '#ef4444'
    for s in filtered_df['DEI Score']
]

fig.add_trace(go.Bar(
    x=filtered_df['County'] + " (" + filtered_df['State'].str[:2] + ")",
    y=filtered_df['DEI Score'],
    marker_color=colors,
    text=[f"{s:.0f}" for s in filtered_df['DEI Score']],
    textposition='outside'
))

fig.update_layout(
    title="DEI Opportunity Score by County",
    xaxis_title="County",
    yaxis_title="DEI Score",
    height=500,
    showlegend=False,
    yaxis=dict(range=[0, 100])
)

# Add threshold lines
fig.add_hline(y=65, line_dash="dash", line_color="green", annotation_text="Excellent (65+)")
fig.add_hline(y=50, line_dash="dash", line_color="blue", annotation_text="Good (50+)")
fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Moderate (40+)")

st.plotly_chart(fig, use_container_width=True)

# ==================== KEY INSIGHTS ====================

st.markdown("## 🔑 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌟 Best Counties for DEI")
    
    top_counties = county_scores.head(3)
    for _, row in top_counties.iterrows():
        mwb_val = f"{row['Minority/Women Biz']:.0f}" if pd.notna(row['Minority/Women Biz']) else 'N/A'
        st.success(f"""
        **{row['County']}, {row['State']}**  
        DEI Score: **{row['DEI Score']:.0f}**  
        Minority/Women Businesses: {mwb_val}
        """)

with col2:
    st.markdown("### 📈 Growth Opportunities")
    
    # Counties with good minority business scores but lower overall DEI (potential)
    growth_potential = county_scores[
        (county_scores['Minority/Women Biz'] >= 50) & 
        (county_scores['DEI Score'] < 60)
    ]
    
    if len(growth_potential) > 0:
        for _, row in growth_potential.head(3).iterrows():
            mwb_val = f"{row['Minority/Women Biz']:.0f}" if pd.notna(row['Minority/Women Biz']) else 'N/A'
            internet_val = f"{row['Internet Access']:.0f}" if pd.notna(row['Internet Access']) else 'N/A'
            housing_val = f"{row['Affordable Housing']:.0f}" if pd.notna(row['Affordable Housing']) else 'N/A'
            st.info(f"""
            **{row['County']}, {row['State']}**  
            Strong minority business presence ({mwb_val}) with room to grow  
            Focus areas: Internet ({internet_val}), Housing ({housing_val})
            """)
    else:
        st.write("All counties with strong minority business presence also have high overall DEI scores.")

# ==================== METHODOLOGY ====================

with st.expander("📋 How is the DEI Opportunity Score Calculated?"):
    st.markdown("""
    ### DEI Opportunity Score Methodology
    
    The DEI Opportunity Score is a weighted composite that measures how favorable a county is for diversity, equity, and inclusive economic growth.
    
    #### Component Weights:
    
    | Metric | Weight | Why It Matters |
    |--------|--------|----------------|
    | **Minority/Women-Owned Businesses** | 25% | Direct measure of entrepreneurial diversity and DEI success |
    | **Inclusive Growth Score** | 20% | Overall economic inclusion (Mastercard's composite measure) |
    | **Internet Access** | 15% | Digital equity enables remote work and education opportunities |
    | **Affordable Housing** | 15% | Economic accessibility and stability for diverse populations |
    | **Personal Income** | 10% | Economic opportunity and upward mobility |
    | **Health Insurance Coverage** | 10% | Social safety net and community well-being |
    | **New Businesses** | 5% | Entrepreneurship opportunity and economic dynamism |
    
    #### Score Interpretation:
    
    - 🌟 **Excellent (65+)**: Leading DEI environment - strong across all metrics
    - ✅ **Good (50-64)**: Above average DEI indicators - favorable for growth
    - 📊 **Moderate (40-49)**: Average DEI environment - has potential
    - 📈 **Developing (<40)**: Below average - significant opportunity for improvement
    
    #### Data Source:
    Mastercard Inclusive Growth Score (IGS) dataset - scores are normalized to state averages (50 = state baseline).
    """)

# Footer
st.markdown("---")
st.caption("CIS 301 Capstone Project - Clark Atlanta CIS301 | Developer: Emery")
st.caption("💡 Higher scores indicate better DEI and economic opportunity environments")

