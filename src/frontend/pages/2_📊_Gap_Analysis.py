"""
County Gap Analysis Page
CIS 301 Capstone Project - Clark Atlanta CIS301

Compare counties against each other to identify opportunity gaps
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

# Add frontend directory to path
frontend_path = Path(__file__).parent.parent
sys.path.insert(0, str(frontend_path))

from utils.api_client import api_client
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, METRIC_NAMES

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Gap Analysis", page_icon="📊", layout=LAYOUT)

# Title
st.title("📊 County Gap Analysis")
st.markdown("Compare counties against each other to identify DEI and opportunity gaps")

st.markdown("---")

# Key metrics for DEI analysis
KEY_METRICS = [
    'inclusive_growth_score',
    'minority_women_owned_businesses_score',
    'internet_access_score',
    'affordable_housing_score',
    'personal_income_score',
    'health_insurance_coverage_score',
    'new_businesses_score'
]

# Fetch all data first
try:
    with st.spinner("Loading county data..."):
        # Get all tract data
        response = api_client.get_tracts(limit=500)
        tracts = response.get('tracts', [])
        
        if not tracts:
            st.error("No data found. Please ensure the backend is running.")
            st.stop()
        
        df = pd.DataFrame(tracts)
        
        # Get latest year
        df['year'] = df['year'].astype(int)
        latest_year = df['year'].max()
        
        # Filter to latest year
        df = df[df['year'] == latest_year]
        
        # Aggregate by county
        county_metrics = df.groupby(['county', 'state']).agg({
            metric: 'mean' for metric in KEY_METRICS if metric in df.columns
        }).reset_index()
        
        # Create county labels
        county_metrics['county_label'] = county_metrics['county'] + " (" + county_metrics['state'] + ")"
        
        if len(county_metrics) < 2:
            st.error("Need at least 2 counties to compare.")
            st.stop()

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the backend API is running at http://localhost:8000")
    st.stop()

st.info(f"📅 Comparing data from **{latest_year}** (most recent year)")

st.markdown("---")

# County Selection
st.markdown("### Select Counties to Compare")

col1, col2 = st.columns(2)

county_options = county_metrics['county_label'].tolist()

with col1:
    st.markdown("#### 🔵 County A")
    county_a = st.selectbox(
        "Select first county",
        county_options,
        index=0,
        key="county_a"
    )

with col2:
    st.markdown("#### 🟠 County B")
    # Default to second county if available
    default_b = 1 if len(county_options) > 1 else 0
    county_b = st.selectbox(
        "Select second county",
        county_options,
        index=default_b,
        key="county_b"
    )

if county_a == county_b:
    st.warning("Please select two different counties to compare.")
    st.stop()

# Get data for selected counties
county_a_data = county_metrics[county_metrics['county_label'] == county_a].iloc[0]
county_b_data = county_metrics[county_metrics['county_label'] == county_b].iloc[0]

st.markdown("---")

# Summary comparison
st.markdown("### Quick Comparison")

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown(f"#### 🔵 {county_a_data['county']}")
    st.markdown(f"📍 {county_a_data['state']}")
    igs_a = county_a_data.get('inclusive_growth_score')
    if pd.notna(igs_a):
        st.metric("Inclusive Growth Score", f"{igs_a:.1f}")

with col2:
    st.markdown("#### vs")
    # Show which is better overall
    if pd.notna(igs_a) and pd.notna(county_b_data.get('inclusive_growth_score')):
        diff = igs_a - county_b_data.get('inclusive_growth_score')
        if diff > 0:
            st.success(f"🔵 +{diff:.1f}")
        elif diff < 0:
            st.error(f"🟠 +{abs(diff):.1f}")
        else:
            st.info("Tie")

with col3:
    st.markdown(f"#### 🟠 {county_b_data['county']}")
    st.markdown(f"📍 {county_b_data['state']}")
    igs_b = county_b_data.get('inclusive_growth_score')
    if pd.notna(igs_b):
        st.metric("Inclusive Growth Score", f"{igs_b:.1f}")

st.markdown("---")

# Build comparison data
comparison_data = []

for metric in KEY_METRICS:
    if metric in county_metrics.columns:
        val_a = county_a_data.get(metric)
        val_b = county_b_data.get(metric)
        
        if pd.notna(val_a) and pd.notna(val_b):
            gap = val_a - val_b
            winner = "A" if gap > 0 else "B" if gap < 0 else "Tie"
            
            comparison_data.append({
                'metric': METRIC_NAMES.get(metric, metric.replace('_', ' ').title()),
                'metric_key': metric,
                'county_a': val_a,
                'county_b': val_b,
                'gap': gap,
                'winner': winner
            })

if not comparison_data:
    st.warning("No valid metrics found for comparison")
    st.stop()

comp_df = pd.DataFrame(comparison_data)

# Visualization tabs
tab1, tab2, tab3 = st.tabs(["📊 Side-by-Side", "📈 Gap Analysis", "📋 Detailed Comparison"])

with tab1:
    st.markdown("### Side-by-Side Comparison")
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=f"🔵 {county_a_data['county']}",
        x=comp_df['metric'],
        y=comp_df['county_a'],
        marker_color='#3b82f6',
        text=[f"{v:.0f}" for v in comp_df['county_a']],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name=f"🟠 {county_b_data['county']}",
        x=comp_df['metric'],
        y=comp_df['county_b'],
        marker_color='#f97316',
        text=[f"{v:.0f}" for v in comp_df['county_b']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{county_a_data['county']} vs {county_b_data['county']}",
        xaxis_title="",
        yaxis_title="Score",
        barmode='group',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(range=[0, 110])
    )
    
    # Add baseline at 50
    fig.add_hline(y=50, line_dash="dash", line_color="gray", 
                  annotation_text="State Baseline (50)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Winner summary
    a_wins = len(comp_df[comp_df['winner'] == 'A'])
    b_wins = len(comp_df[comp_df['winner'] == 'B'])
    ties = len(comp_df[comp_df['winner'] == 'Tie'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"🔵 {county_a_data['county']} Leads", f"{a_wins} metrics")
    with col2:
        st.metric(f"🟠 {county_b_data['county']} Leads", f"{b_wins} metrics")
    with col3:
        st.metric("Ties", f"{ties} metrics")

with tab2:
    st.markdown("### Gap Analysis")
    st.markdown(f"*Positive = {county_a_data['county']} is higher, Negative = {county_b_data['county']} is higher*")
    
    # Create gap visualization
    fig = go.Figure()
    
    # Color based on which county is better
    colors = ['#3b82f6' if gap > 0 else '#f97316' if gap < 0 else '#6b7280' 
              for gap in comp_df['gap']]
    
    fig.add_trace(go.Bar(
        x=comp_df['gap'],
        y=comp_df['metric'],
        orientation='h',
        marker_color=colors,
        text=[f"{gap:+.1f}" for gap in comp_df['gap']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Gap Between Counties (A - B)",
        xaxis_title=f"Gap ({county_a_data['county']} minus {county_b_data['county']})",
        yaxis_title="",
        height=500,
        showlegend=False
    )
    
    # Add vertical line at 0
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.markdown("### 🔑 Key Insights")
    
    # Largest gaps
    largest_a_lead = comp_df[comp_df['gap'] > 0].nlargest(2, 'gap') if len(comp_df[comp_df['gap'] > 0]) > 0 else pd.DataFrame()
    largest_b_lead = comp_df[comp_df['gap'] < 0].nsmallest(2, 'gap') if len(comp_df[comp_df['gap'] < 0]) > 0 else pd.DataFrame()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🔵 {county_a_data['county']} Strengths")
        if len(largest_a_lead) > 0:
            for _, row in largest_a_lead.iterrows():
                st.success(f"**{row['metric']}**: +{row['gap']:.1f} points ahead")
        else:
            st.info("No significant advantages")
    
    with col2:
        st.markdown(f"#### 🟠 {county_b_data['county']} Strengths")
        if len(largest_b_lead) > 0:
            for _, row in largest_b_lead.iterrows():
                st.success(f"**{row['metric']}**: +{abs(row['gap']):.1f} points ahead")
        else:
            st.info("No significant advantages")

with tab3:
    st.markdown("### Detailed Metrics Comparison")
    
    # Create detailed comparison table
    display_df = comp_df.copy()
    display_df['county_a'] = display_df['county_a'].round(1)
    display_df['county_b'] = display_df['county_b'].round(1)
    display_df['gap'] = display_df['gap'].round(1)
    
    # Add winner indicator
    display_df['Better'] = display_df['winner'].apply(
        lambda x: f"🔵 {county_a_data['county']}" if x == 'A' 
        else f"🟠 {county_b_data['county']}" if x == 'B' 
        else "➖ Tie"
    )
    
    display_df = display_df[['metric', 'county_a', 'county_b', 'gap', 'Better']]
    display_df.columns = ['Metric', county_a_data['county'], county_b_data['county'], 'Gap', 'Leader']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Recommendation
    st.markdown("---")
    st.markdown("### 💡 DEI Recommendation")
    
    # Calculate overall DEI advantage
    dei_metrics = ['minority_women_owned_businesses_score', 'inclusive_growth_score', 
                   'affordable_housing_score', 'internet_access_score']
    
    dei_a_avg = comp_df[comp_df['metric_key'].isin(dei_metrics)]['county_a'].mean()
    dei_b_avg = comp_df[comp_df['metric_key'].isin(dei_metrics)]['county_b'].mean()
    
    if dei_a_avg > dei_b_avg:
        better_county = county_a_data['county']
        better_state = county_a_data['state']
        better_score = dei_a_avg
        other_score = dei_b_avg
    else:
        better_county = county_b_data['county']
        better_state = county_b_data['state']
        better_score = dei_b_avg
        other_score = dei_a_avg
    
    st.success(f"""
    **{better_county}, {better_state}** has a stronger DEI profile with an average DEI score of **{better_score:.1f}** 
    compared to **{other_score:.1f}** for the other county.
    
    This suggests {better_county} may offer better opportunities for:
    - Minority and women-owned business growth
    - Inclusive economic development
    - Digital equity and affordable housing access
    """)

# Footer
st.markdown("---")
st.caption("CIS 301 Capstone Project - Clark Atlanta CIS301 | Developer: Emery")
