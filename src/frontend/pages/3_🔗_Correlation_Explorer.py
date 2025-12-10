"""
Correlation Explorer Page
CIS 301 Capstone Project - Clark Atlanta CIS301

Analyze relationships between different economic metrics
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add frontend directory to path
frontend_path = Path(__file__).parent.parent
sys.path.insert(0, str(frontend_path))

from utils.api_client import api_client
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, METRIC_NAMES

# Page configuration
st.set_page_config(page_title=f"{PAGE_TITLE} - Correlation Explorer", page_icon="🔗", layout=LAYOUT)

# Title
st.title("🔗 Correlation Explorer")
st.markdown("Analyze relationships between different economic inclusion metrics")

st.markdown("---")

# Available metrics for correlation
CORRELATION_METRICS = list(METRIC_NAMES.keys())

# Filters
col1, col2 = st.columns(2)

with col1:
    # Get available states
    try:
        states_data = api_client.get_states()
        state_options = ["All States"] + [s['state'] for s in states_data]
        selected_state = st.selectbox("Select State", state_options)
    except Exception as e:
        st.error(f"Error loading states: {str(e)}")
        st.stop()

with col2:
    year_options = ["All Years"] + list(range(2017, 2025))
    selected_year = st.selectbox("Select Year", year_options)

st.markdown("---")

# Metric selection
st.markdown("### Select Metrics to Compare")

col1, col2 = st.columns(2)

with col1:
    metric_x = st.selectbox(
        "X-Axis Metric",
        CORRELATION_METRICS,
        index=CORRELATION_METRICS.index('minority_women_owned_businesses_score') if 'minority_women_owned_businesses_score' in CORRELATION_METRICS else 0,
        format_func=lambda x: METRIC_NAMES.get(x, x)
    )

with col2:
    metric_y = st.selectbox(
        "Y-Axis Metric",
        CORRELATION_METRICS,
        index=CORRELATION_METRICS.index('inclusive_growth_score') if 'inclusive_growth_score' in CORRELATION_METRICS else 1,
        format_func=lambda x: METRIC_NAMES.get(x, x)
    )

# Fetch data
try:
    with st.spinner("Loading data and calculating correlation..."):
        # Prepare filters
        state_filter = None if selected_state == "All States" else selected_state
        year_filter = None if selected_year == "All Years" else selected_year
        
        # Get tract data
        response = api_client.get_tracts(
            state=state_filter,
            year=year_filter,
            limit=500
        )
        
        tracts = response['tracts']
        
        if not tracts:
            st.warning("No data found for the selected filters.")
            st.stop()
        
        # Convert to DataFrame
        df = pd.DataFrame(tracts)
        
        # Filter for valid data points
        valid_data = df[[metric_x, metric_y, 'state', 'census_tract_fips']].dropna()
        
        if len(valid_data) < 2:
            st.warning("Insufficient data points for correlation analysis.")
            st.stop()
        
        # Calculate correlation
        try:
            corr_result = api_client.get_correlation(
                metric_x=metric_x,
                metric_y=metric_y,
                state=state_filter,
                year=year_filter
            )
            correlation_coef = corr_result['correlation_coefficient']
        except:
            # Fallback to manual calculation
            correlation_coef = valid_data[metric_x].corr(valid_data[metric_y])
        
        # Display correlation summary
        st.markdown("---")
        st.markdown("### Correlation Analysis Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Sample Size", len(valid_data))
        
        with col2:
            st.metric("Correlation Coefficient", f"{correlation_coef:.3f}")
        
        with col3:
            # Interpret correlation strength
            abs_corr = abs(correlation_coef)
            if abs_corr >= 0.7:
                strength = "Strong"
                color = "🟢"
            elif abs_corr >= 0.4:
                strength = "Moderate"
                color = "🟡"
            else:
                strength = "Weak"
                color = "🔴"
            
            st.metric("Correlation Strength", f"{color} {strength}")
        
        with col4:
            # Direction
            direction = "Positive" if correlation_coef > 0 else "Negative"
            arrow = "↗️" if correlation_coef > 0 else "↘️"
            st.metric("Direction", f"{arrow} {direction}")
        
        st.markdown("---")
        
        # Visualization tabs
        tab1, tab2, tab3 = st.tabs(["📈 Scatter Plot", "🔥 Heatmap", "📊 Analysis"])
        
        with tab1:
            st.markdown(f"### {METRIC_NAMES.get(metric_x, metric_x)} vs. {METRIC_NAMES.get(metric_y, metric_y)}")
            
            # Create scatter plot
            fig = px.scatter(
                valid_data,
                x=metric_x,
                y=metric_y,
                color='state' if selected_state == "All States" else None,
                hover_data=['census_tract_fips', 'state'],
                title=f"Correlation: r = {correlation_coef:.3f}",
                labels={
                    metric_x: METRIC_NAMES.get(metric_x, metric_x),
                    metric_y: METRIC_NAMES.get(metric_y, metric_y)
                }
            )
            
            # Add manual trend line using correlation
            if len(valid_data) > 1:
                import numpy as np
                # Calculate linear regression manually
                x_vals = valid_data[metric_x].values
                y_vals = valid_data[metric_y].values
                z = np.polyfit(x_vals, y_vals, 1)
                p = np.poly1d(z)
                
                # Add trend line
                x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
                fig.add_scatter(
                    x=x_trend,
                    y=p(x_trend),
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', width=2, dash='dash')
                )
            
            fig.update_layout(
                height=600,
                xaxis_title=METRIC_NAMES.get(metric_x, metric_x),
                yaxis_title=METRIC_NAMES.get(metric_y, metric_y)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            st.markdown("#### Interpretation")
            
            if correlation_coef > 0.7:
                st.success(f"**Strong positive correlation**: As {METRIC_NAMES.get(metric_x, metric_x)} increases, {METRIC_NAMES.get(metric_y, metric_y)} tends to increase significantly.")
            elif correlation_coef > 0.4:
                st.info(f"**Moderate positive correlation**: Higher {METRIC_NAMES.get(metric_x, metric_x)} is somewhat associated with higher {METRIC_NAMES.get(metric_y, metric_y)}.")
            elif correlation_coef > 0:
                st.warning(f"**Weak positive correlation**: Little relationship between {METRIC_NAMES.get(metric_x, metric_x)} and {METRIC_NAMES.get(metric_y, metric_y)}.")
            elif correlation_coef > -0.4:
                st.warning(f"**Weak negative correlation**: Little inverse relationship between the metrics.")
            elif correlation_coef > -0.7:
                st.info(f"**Moderate negative correlation**: Higher {METRIC_NAMES.get(metric_x, metric_x)} is somewhat associated with lower {METRIC_NAMES.get(metric_y, metric_y)}.")
            else:
                st.error(f"**Strong negative correlation**: As {METRIC_NAMES.get(metric_x, metric_x)} increases, {METRIC_NAMES.get(metric_y, metric_y)} tends to decrease significantly.")
        
        with tab2:
            st.markdown("### Correlation Heatmap")
            st.markdown("Explore correlations between multiple metrics")
            
            # Select metrics for heatmap (remove duplicates from default)
            default_metrics = list(dict.fromkeys([
                metric_x, metric_y, 'inclusive_growth_score', 
                'internet_access_score', 'affordable_housing_score'
            ]))
            
            heatmap_metrics = st.multiselect(
                "Select metrics to include in heatmap",
                CORRELATION_METRICS,
                default=default_metrics,
                format_func=lambda x: METRIC_NAMES.get(x, x)
            )
            
            if len(heatmap_metrics) >= 2:
                # Calculate correlation matrix
                corr_matrix = df[heatmap_metrics].corr()
                
                # Create heatmap
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=[METRIC_NAMES.get(m, m) for m in corr_matrix.columns],
                    y=[METRIC_NAMES.get(m, m) for m in corr_matrix.index],
                    colorscale='RdBu',
                    zmid=0,
                    zmin=-1,
                    zmax=1,
                    text=corr_matrix.values,
                    texttemplate='%{text:.2f}',
                    textfont={"size": 10},
                    colorbar=dict(title="Correlation")
                ))
                
                fig.update_layout(
                    title="Correlation Heatmap",
                    height=600,
                    xaxis_title="",
                    yaxis_title=""
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select at least 2 metrics for the heatmap")
        
        with tab3:
            st.markdown("### Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"#### {METRIC_NAMES.get(metric_x, metric_x)} Statistics")
                x_data = valid_data[metric_x]
                st.write(f"• Mean: {x_data.mean():.2f}")
                st.write(f"• Median: {x_data.median():.2f}")
                st.write(f"• Std Dev: {x_data.std():.2f}")
                st.write(f"• Range: {x_data.min():.2f} - {x_data.max():.2f}")
            
            with col2:
                st.markdown(f"#### {METRIC_NAMES.get(metric_y, metric_y)} Statistics")
                y_data = valid_data[metric_y]
                st.write(f"• Mean: {y_data.mean():.2f}")
                st.write(f"• Median: {y_data.median():.2f}")
                st.write(f"• Std Dev: {y_data.std():.2f}")
                st.write(f"• Range: {y_data.min():.2f} - {y_data.max():.2f}")
            
            st.markdown("---")
            
            # Quadrant analysis
            st.markdown("#### Quadrant Analysis")
            
            x_median = valid_data[metric_x].median()
            y_median = valid_data[metric_y].median()
            
            quadrants = {
                'High-High': len(valid_data[(valid_data[metric_x] >= x_median) & (valid_data[metric_y] >= y_median)]),
                'High-Low': len(valid_data[(valid_data[metric_x] >= x_median) & (valid_data[metric_y] < y_median)]),
                'Low-High': len(valid_data[(valid_data[metric_x] < x_median) & (valid_data[metric_y] >= y_median)]),
                'Low-Low': len(valid_data[(valid_data[metric_x] < x_median) & (valid_data[metric_y] < y_median)])
            }
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "High-High",
                    quadrants['High-High'],
                    delta=f"{quadrants['High-High']/len(valid_data)*100:.1f}%"
                )
            
            with col2:
                st.metric(
                    "High-Low",
                    quadrants['High-Low'],
                    delta=f"{quadrants['High-Low']/len(valid_data)*100:.1f}%"
                )
            
            with col3:
                st.metric(
                    "Low-High",
                    quadrants['Low-High'],
                    delta=f"{quadrants['Low-High']/len(valid_data)*100:.1f}%"
                )
            
            with col4:
                st.metric(
                    "Low-Low",
                    quadrants['Low-Low'],
                    delta=f"{quadrants['Low-Low']/len(valid_data)*100:.1f}%"
                )
            
            st.markdown("---")
            
            # Data table
            st.markdown("#### Sample Data Points")
            
            display_df = valid_data[['census_tract_fips', 'state', metric_x, metric_y]].copy()
            display_df.columns = ['Census Tract', 'State', METRIC_NAMES.get(metric_x, metric_x), METRIC_NAMES.get(metric_y, metric_y)]
            
            # Round numeric columns
            for col in [METRIC_NAMES.get(metric_x, metric_x), METRIC_NAMES.get(metric_y, metric_y)]:
                if col in display_df.columns:
                    display_df[col] = display_df[col].round(1)
            
            st.dataframe(display_df.head(20), use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the backend API is running at http://localhost:8000")

# Footer
st.markdown("---")
st.caption("CIS 301 Capstone Project - Clark Atlanta CIS301 | Developer: Emery")

