"""
Equity Map Page
CIS 301 Capstone Project - Clark Atlanta CIS301

Interactive choropleth map showing Inclusive Growth Scores by geography
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
st.set_page_config(page_title=f"{PAGE_TITLE} - Equity Map", page_icon="📍", layout=LAYOUT)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .equity-map-container {
        background-color: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .equity-map-title {
        color: #e0e0e0;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📍 Equity Map")
st.markdown("Interactive visualization of Inclusive Growth Scores across census tracts")

st.markdown("---")

# Filters
col1, col2, col3 = st.columns(3)

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

with col3:
    metric_options = list(METRIC_NAMES.keys())
    selected_metric = st.selectbox(
        "Select Metric",
        metric_options,
        format_func=lambda x: METRIC_NAMES.get(x, x)
    )

# Fetch data
try:
    with st.spinner("Loading data..."):
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
        
        # Display summary
        st.markdown("### Data Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tracts", len(df))
        
        with col2:
            if selected_metric in df.columns:
                avg_score = df[selected_metric].mean()
                st.metric(
                    f"Avg {METRIC_NAMES.get(selected_metric, selected_metric)}", 
                    f"{avg_score:.1f}" if pd.notna(avg_score) else "N/A"
                )
        
        with col3:
            states_count = df['state'].nunique()
            st.metric("States", states_count)
        
        with col4:
            years_count = df['year'].nunique()
            st.metric("Years", years_count)
        
        st.markdown("---")
        
        # Visualization tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Equity Map", "🏘️ County Comparison", "📈 Distribution", "📋 Data Table"])
        
        with tab1:
            st.markdown(f"### Equity Map - {METRIC_NAMES.get(selected_metric, selected_metric)}")
            st.markdown("*Grid visualization showing score distribution across census tracts*")
            
            if selected_metric in df.columns:
                # Get data and remove nulls
                map_data = df[[selected_metric, 'county', 'census_tract_fips']].dropna()
                
                if len(map_data) > 0:
                    # Group by county and create a grid representation
                    county_groups = map_data.groupby('county')
                    
                    # Get all metric values for consistent color scaling
                    all_values = map_data[selected_metric].values
                    min_val = all_values.min()
                    max_val = all_values.max()
                    
                    # Create grid data - reshape into rows and columns
                    values_list = map_data[selected_metric].tolist()
                    tract_list = map_data['census_tract_fips'].tolist()
                    county_list = map_data['county'].tolist()
                    
                    # Calculate grid dimensions (aim for ~8-10 columns)
                    n_values = len(values_list)
                    n_cols = min(10, n_values)
                    n_rows = int(np.ceil(n_values / n_cols))
                    
                    # Pad the lists to fill the grid
                    pad_size = n_rows * n_cols - n_values
                    values_padded = values_list + [None] * pad_size
                    tracts_padded = tract_list + [''] * pad_size
                    counties_padded = county_list + [''] * pad_size
                    
                    # Reshape into 2D arrays
                    z_data = np.array(values_padded, dtype=float).reshape(n_rows, n_cols)
                    tract_labels = np.array(tracts_padded).reshape(n_rows, n_cols)
                    county_labels = np.array(counties_padded).reshape(n_rows, n_cols)
                    
                    # Create custom hover text
                    hover_text = []
                    for i in range(n_rows):
                        row_text = []
                        for j in range(n_cols):
                            if tract_labels[i, j]:
                                row_text.append(
                                    f"Tract: {tract_labels[i, j]}<br>"
                                    f"County: {county_labels[i, j]}<br>"
                                    f"IGS Score: {z_data[i, j]:.1f}"
                                )
                            else:
                                row_text.append('')
                        hover_text.append(row_text)
                    
                    # Create the heatmap
                    fig = go.Figure(data=go.Heatmap(
                        z=z_data,
                        text=hover_text,
                        hovertemplate='%{text}<extra></extra>',
                        colorscale=[
                            [0.0, '#1e3a5f'],      # Dark blue
                            [0.25, '#2e5984'],     # Medium-dark blue
                            [0.5, '#4a90c2'],      # Medium blue
                            [0.75, '#7bb8e0'],     # Light blue
                            [1.0, '#a8d4f0']       # Very light blue
                        ],
                        colorbar=dict(
                            title=dict(text='IGS Score', side='right'),
                            tickfont=dict(color='#e0e0e0'),
                            titlefont=dict(color='#e0e0e0')
                        ),
                        showscale=True,
                        zmin=min_val,
                        zmax=max_val,
                        xgap=2,
                        ygap=2
                    ))
                    
                    fig.update_layout(
                        title=dict(
                            text=f"Equity Map",
                            font=dict(color='#e0e0e0', size=16),
                            x=0.02
                        ),
                        plot_bgcolor='#1a1a2e',
                        paper_bgcolor='#1a1a2e',
                        height=450,
                        margin=dict(l=20, r=80, t=60, b=20),
                        xaxis=dict(
                            showgrid=False,
                            showticklabels=False,
                            zeroline=False
                        ),
                        yaxis=dict(
                            showgrid=False,
                            showticklabels=False,
                            zeroline=False,
                            autorange='reversed'
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Score legend explanation
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.info(f"🔵 **Low Score** (≤{min_val + (max_val-min_val)*0.33:.1f}): Areas needing investment")
                    with col_b:
                        st.info(f"🔷 **Mid Score** ({min_val + (max_val-min_val)*0.33:.1f}-{min_val + (max_val-min_val)*0.66:.1f}): Moderate equity levels")
                    with col_c:
                        st.success(f"💎 **High Score** (≥{min_val + (max_val-min_val)*0.66:.1f}): Strong equity indicators")
                else:
                    st.warning("No valid data points for the equity map")
            else:
                st.warning(f"Metric '{selected_metric}' not found in data")
        
        with tab2:
            st.markdown(f"### {METRIC_NAMES.get(selected_metric, selected_metric)} by County")
            st.markdown("*Compare metrics across counties for more granular data-driven decisions*")
            
            if selected_metric in df.columns and 'county' in df.columns:
                # County filter within the tab
                county_list = sorted(df['county'].dropna().unique().tolist())
                
                if len(county_list) > 0:
                    # Option to select specific counties or view top/bottom
                    view_mode = st.radio(
                        "View Mode",
                        ["Top/Bottom Counties", "Select Specific Counties"],
                        horizontal=True,
                        key="county_view_mode"
                    )
                    
                    if view_mode == "Top/Bottom Counties":
                        col_top, col_n = st.columns([1, 1])
                        with col_top:
                            show_type = st.selectbox(
                                "Show",
                                ["Top Counties", "Bottom Counties", "Both"],
                                key="county_show_type"
                            )
                        with col_n:
                            n_counties = st.slider("Number of counties", 5, 20, 10, key="n_counties")
                        
                        # Aggregate by county
                        county_avg = df.groupby('county')[selected_metric].agg(['mean', 'count']).reset_index()
                        county_avg.columns = ['county', 'avg_score', 'tract_count']
                        county_avg = county_avg.sort_values('avg_score', ascending=False)
                        
                        if show_type == "Top Counties":
                            display_counties = county_avg.head(n_counties)
                            chart_title = f"Top {n_counties} Counties"
                        elif show_type == "Bottom Counties":
                            display_counties = county_avg.tail(n_counties).sort_values('avg_score', ascending=True)
                            chart_title = f"Bottom {n_counties} Counties"
                        else:  # Both
                            top_counties = county_avg.head(n_counties // 2)
                            bottom_counties = county_avg.tail(n_counties // 2)
                            display_counties = pd.concat([top_counties, bottom_counties])
                            chart_title = f"Top & Bottom {n_counties // 2} Counties"
                        
                        # Create bar chart
                        fig = px.bar(
                            display_counties,
                            x='county',
                            y='avg_score',
                            title=chart_title,
                            labels={
                                'county': 'County',
                                'avg_score': METRIC_NAMES.get(selected_metric, selected_metric)
                            },
                            color='avg_score',
                            color_continuous_scale='RdYlGn',
                            hover_data={'tract_count': True}
                        )
                        
                        fig.update_layout(
                            height=500,
                            showlegend=False,
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show summary statistics
                        st.markdown("#### County Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Counties", len(county_avg))
                        with col2:
                            st.metric("Avg Score (All)", f"{county_avg['avg_score'].mean():.1f}")
                        with col3:
                            st.metric("Highest", f"{county_avg['avg_score'].max():.1f}")
                        with col4:
                            st.metric("Lowest", f"{county_avg['avg_score'].min():.1f}")
                        
                    else:  # Select Specific Counties
                        selected_counties = st.multiselect(
                            "Select Counties to Compare",
                            county_list,
                            default=county_list[:min(5, len(county_list))],
                            key="selected_counties"
                        )
                        
                        if selected_counties:
                            # Filter and aggregate
                            filtered_df = df[df['county'].isin(selected_counties)]
                            county_avg = filtered_df.groupby('county')[selected_metric].agg(['mean', 'count']).reset_index()
                            county_avg.columns = ['county', 'avg_score', 'tract_count']
                            county_avg = county_avg.sort_values('avg_score', ascending=False)
                            
                            # Create bar chart
                            fig = px.bar(
                                county_avg,
                                x='county',
                                y='avg_score',
                                title=f"County Comparison - {METRIC_NAMES.get(selected_metric, selected_metric)}",
                                labels={
                                    'county': 'County',
                                    'avg_score': METRIC_NAMES.get(selected_metric, selected_metric)
                                },
                                color='avg_score',
                                color_continuous_scale='RdYlGn',
                                hover_data={'tract_count': True}
                            )
                            
                            fig.update_layout(
                                height=500,
                                showlegend=False,
                                xaxis_tickangle=-45
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Detailed comparison table
                            st.markdown("#### Detailed Comparison")
                            comparison_table = county_avg.copy()
                            comparison_table['avg_score'] = comparison_table['avg_score'].round(2)
                            comparison_table.columns = ['County', 'Avg Score', 'Census Tracts']
                            st.dataframe(
                                comparison_table,
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.info("Select at least one county to view comparison")
                else:
                    st.warning("No county data available for comparison")
            else:
                st.warning(f"Required data not found for county comparison")
        
        with tab3:
            st.markdown(f"### {METRIC_NAMES.get(selected_metric, selected_metric)} Distribution")
            
            if selected_metric in df.columns:
                # Remove null values for histogram
                metric_data = df[selected_metric].dropna()
                
                if len(metric_data) > 0:
                    fig = px.histogram(
                        metric_data,
                        x=selected_metric,
                        nbins=30,
                        title=f"Distribution of {METRIC_NAMES.get(selected_metric, selected_metric)}",
                        labels={selected_metric: METRIC_NAMES.get(selected_metric, selected_metric)},
                        marginal="box"
                    )
                    
                    fig.update_layout(
                        height=500,
                        showlegend=False,
                        xaxis_title=METRIC_NAMES.get(selected_metric, selected_metric),
                        yaxis_title="Frequency"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Statistics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Mean", f"{metric_data.mean():.2f}")
                    with col2:
                        st.metric("Median", f"{metric_data.median():.2f}")
                    with col3:
                        st.metric("Min", f"{metric_data.min():.2f}")
                    with col4:
                        st.metric("Max", f"{metric_data.max():.2f}")
                    with col5:
                        st.metric("Std Dev", f"{metric_data.std():.2f}")
                else:
                    st.warning("No valid data points for this metric")
            else:
                st.warning(f"Metric '{selected_metric}' not found in data")
        
        with tab4:
            st.markdown("### Census Tract Data")
            
            # Select key columns to display
            display_columns = [
                'census_tract_fips', 'state', 'county', 'year',
                'inclusive_growth_score'
            ]
            
            # Add selected metric if it's not already in the list
            if selected_metric not in display_columns:
                display_columns.append(selected_metric)
            
            # Filter columns that exist
            available_columns = [col for col in display_columns if col in df.columns]
            
            # Format year column to remove comma separators
            display_df = df[available_columns].copy()
            if 'year' in display_df.columns:
                display_df['year'] = display_df['year'].astype(str)
            
            # Display table with column configuration
            st.dataframe(
                display_df.sort_values('state'),
                use_container_width=True,
                height=400,
                column_config={
                    "year": st.column_config.TextColumn("Year")
                }
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name=f"igs_data_{selected_state}_{selected_year}.csv",
                mime="text/csv"
            )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the backend API is running at http://localhost:8000")

# Footer
st.markdown("---")
st.caption("CIS 301 Capstone Project - Clark Atlanta CIS301 | Developer: Emery")

