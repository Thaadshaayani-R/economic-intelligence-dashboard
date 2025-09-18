import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
 
 
# Page Setup
st.set_page_config(
    layout="wide",
    page_title="Economic Intelligence Platform",
    page_icon="📊",
    initial_sidebar_state="expanded"
)
 
# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f4e79, #2980b9);
        padding: 0.5rem;
        border-radius: 10px;
        margin: -1rem -1rem 1rem -1rem;
    }
   
    .metric-container {
        background: rgba(45, 55, 72, 0.9);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.5rem 0;
        text-align: left;
    }
   
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #00d4aa;
        margin: 0;
    }
   
    .metric-body {
        font-size: 1.25rem;
        margin: 0;
    }
   
    .metric-heading {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
    }
   
    .metric-label {
        font-size: 0.8rem;
        color: #888;
        margin: 0;
        text-transform: uppercase;
    }
   
    .metric-delta {
        font-size: 0.7rem;
        margin-top: 0.3rem;
    }
   
    .section-header {
        font-size: 1rem;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
        padding: 0.3rem 0;
        border-bottom: 2px solid #00d4aa;
    }
   
    .section-title {
        color: #ffffff;
        font-size: 1.5rem;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
   
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
    }
   
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 0.5rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
 
 
# Load Data
 
@st.cache_data
def load_data():
    df = pd.read_csv(r"Final_output.csv")
   
    region_map = {
        "North America": ["United States", "Canada", "Mexico"],
        "South America": ["Brazil", "Argentina", "Chile", "Colombia", "Peru", "Ecuador", "Uruguay", "Paraguay", "Venezuela"],
        "Europe": ["Germany", "France", "Italy", "United Kingdom", "Spain", "Netherlands", "Sweden", "Norway", "Poland", "Belgium", "Greece", "Portugal", "Finland", "Switzerland", "Ireland", "Denmark", "Hungary", "Austria", "Czech Republic", "Slovakia", "Ukraine", "Romania", "Bulgaria", "Serbia", "Croatia", "Slovenia", "Lithuania", "Latvia", "Estonia", "Iceland"],
        "Asia": ["China", "India", "Japan", "South Korea", "Indonesia", "Vietnam", "Thailand", "Philippines", "Pakistan", "Bangladesh", "Saudi Arabia", "Iran", "Iraq", "Malaysia", "Singapore", "Sri Lanka", "Nepal", "Kazakhstan", "Uzbekistan", "Israel"],
        "Africa": ["South Africa", "Nigeria", "Egypt", "Kenya", "Ethiopia", "Ghana", "Tanzania", "Uganda", "Morocco", "Algeria", "Tunisia", "Angola", "Zambia"],
        "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]
    }
   
    def map_region(country):
        for region, countries in region_map.items():
            if country in countries:
                return region
        return "Other"
   
    df["Region"] = df["Country"].apply(map_region)
    df['Trade Balance'] = df['Exports_Cleaned_Billion'] - df['Imports_Cleaned_Billion']
    return df
 
df = load_data()
 
 
# Header
st.markdown('<div class="main-header">Economic Intelligence Platform</div>', unsafe_allow_html=True)
 
 
# Sidebar Navigation
 
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Select Dashboard:", [
    "Country Analysis",
    "Global Overview",
    "Regional Insights",
    "Trade Analysis",
    "Download Data"
])
 
 
# Global Overview Dashboard
 
if section == "Country Analysis":
    st.markdown("<div class='section-title'>Country Profile</div>", unsafe_allow_html=True)
 
    # Country Selector
    st.markdown("<p style='color: #a0aec0; margin-bottom: 0.5rem;'>Select a Country</p>", unsafe_allow_html=True)
    country_list = sorted(df["Country"].dropna().unique())
    selected_country = st.selectbox("", country_list, key="country_select", label_visibility="collapsed")
 
    if selected_country:
        country_df = df[df["Country"] == selected_country].iloc[0]
 
                # 📘 Add Country Summary Block
 
        st.markdown(f"""
        <div class='metric-container'>
            <div class='metric-heading'>Country Summary</div>
            <div class='metric-body'>{country_df['summary']}</div>
        </div>
        """, unsafe_allow_html=True)
 
        # Display Metrics in 3x2 grid
        col1, col2, col3 = st.columns(3)
           
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Economic Class</div>
                <div class='metric-value'>{country_df['economic_class']}</div>
            </div>
            """, unsafe_allow_html=True)
               
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>GDP Growth Rate (%)</div>
                <div class='metric-value'>{country_df['GDP_growth_rate_cleaned']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
 
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Inflation Rate (%)</div>
                <div class='metric-value'>{country_df['Inflation_rate_cleaned']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
               
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Gov. Debt (% of GDP)</div>
                <div class='metric-value'>{country_df['Gov_Debt_Percent_GDP_Cleaned']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
 
        with col3:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Exports (Bn)</div>
                <div class='metric-value'>{country_df['Exports_Cleaned_Billion']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
               
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Imports (Bn)</div>
                <div class='metric-value'>{country_df['Imports_Cleaned_Billion']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
 
        # Second row
        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>GDP per Capita (PPP)</div>
                <div class='metric-value'>${country_df['GDP_per_capita_ppp_cleaned']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
 
        with col6:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-title'>Trade Openness (%)</div>
                <div class='metric-value'>{country_df['Trade_Openness']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
       
 
 
 
# Country Analysis Dashboard
 
elif section == "Global Overview":
   
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
   
    total_gdp = df['gdp_total_usd_billion_cleaned'].sum()
    avg_growth = df['GDP_growth_rate_cleaned'].mean()
    total_trade = (df['Exports_Cleaned_Billion'].sum() + df['Imports_Cleaned_Billion'].sum())
    avg_inflation = df['Inflation_rate_cleaned'].mean()
    total_countries = len(df)
   
    with col1:
        st.metric("Global GDP", f"${total_gdp:,.0f}T", delta=None)
    with col2:
        st.metric("Avg Growth Rate", f"{avg_growth:.1f}%", delta=None)
    with col3:
        st.metric("Total Trade", f"${total_trade:,.0f}B", delta=None)
    with col4:
        st.metric("Avg Inflation", f"{avg_inflation:.1f}%", delta=None)
    with col5:
        st.metric("Countries", f"{total_countries}", delta=None)
 
   
    # Main visualizations
    col1, col2 = st.columns([3, 2])
   
    with col1:
        st.markdown('<div class="section-header">World Economic Map</div>', unsafe_allow_html=True)
        fig_map = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color="gdp_total_usd_billion_cleaned",
            hover_name="Country",
            hover_data={"GDP_growth_rate_cleaned": ":.1f", "GDP_per_capita_ppp_cleaned": ":,.0f"},
            color_continuous_scale="Viridis",
            labels={"gdp_total_usd_billion_cleaned": "GDP (Billion USD)"}
        )
        fig_map.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_map, use_container_width=True)
   
    with col2:
        st.markdown('<div class="section-header">Regional GDP Share</div>', unsafe_allow_html=True)
        region_gdp = df.groupby('Region')['gdp_total_usd_billion_cleaned'].sum().reset_index()
        fig_donut = px.pie(
            region_gdp,
            values='gdp_total_usd_billion_cleaned',
            names='Region',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_donut.update_layout(
            height=220,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
   
    # Bottom row
    col3, col4 = st.columns(2)
   
    with col3:
        st.markdown('<div class="section-header">Economic Classes</div>', unsafe_allow_html=True)
        class_counts = df['economic_class'].value_counts()
        fig_pie = px.pie(
            values=class_counts.values,
            names=class_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            height=220,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
   
    with col4:
        st.markdown('<div class="section-header">Top 05 Economies</div>', unsafe_allow_html=True)
        top_10 = df.nlargest(5, 'gdp_total_usd_billion_cleaned')
        fig_bar = px.bar(
            top_10,
            y='Country',
            x='gdp_total_usd_billion_cleaned',
            orientation='h',
            color='gdp_total_usd_billion_cleaned',
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="GDP (Billion USD)",
            yaxis_title=""
        )
        st.plotly_chart(fig_bar, use_container_width=True)
 
 
# Regional Insights Dashboard
 
elif section == "Regional Insights":
   
    # Regional summary metrics
    regions = df['Region'].unique()
    region_metrics = []
   
    for region in regions:
        region_df = df[df['Region'] == region]
        region_metrics.append({
            'Region': region,
            'Countries': len(region_df),
            'Total GDP': region_df['gdp_total_usd_billion_cleaned'].sum(),
            'Avg Growth': region_df['GDP_growth_rate_cleaned'].mean(),
            'Total Trade': (region_df['Exports_Cleaned_Billion'].sum() + region_df['Imports_Cleaned_Billion'].sum())
        })
   
    region_summary = pd.DataFrame(region_metrics)
   
    # Display regional metrics
    cols = st.columns(len(regions))
    for i, region in enumerate(regions):
        with cols[i]:
            region_data = region_summary[region_summary['Region'] == region].iloc[0]
            st.metric(
                f"{region}",
                f"${region_data['Total GDP']:,.0f}B",
                delta=f"{region_data['Avg Growth']:.1f}% growth"
            )
   
    # Main regional analysis
    col1, col2 = st.columns(2)
   
    with col1:
        st.markdown('<div class="section-header">Regional Economic Performance</div>', unsafe_allow_html=True)
        fig_region_perf = px.scatter(
            region_summary,
            x='Total GDP',
            y='Avg Growth',
            size='Countries',
            color='Region',
            hover_name='Region',
            size_max=60,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_region_perf.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Total GDP (Billion USD)",
            yaxis_title="Average Growth Rate (%)"
        )
        st.plotly_chart(fig_region_perf, use_container_width=True)
   
    with col2:
        st.markdown('<div class="section-header">Regional GDP Share</div>', unsafe_allow_html=True)
        region_gdp = df.groupby('Region')['gdp_total_usd_billion_cleaned'].sum().reset_index()
        fig_donut = px.pie(
            region_gdp,
            values='gdp_total_usd_billion_cleaned',
            names='Region',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_donut.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
 
   
    # Bottom row
    col3, col4 = st.columns(2)
   
    with col3:
        st.markdown('<div class="section-header">Trade Balance by Region</div>', unsafe_allow_html=True)
        region_trade = df.groupby('Region')[['Exports_Cleaned_Billion', 'Imports_Cleaned_Billion']].sum().reset_index()
        region_trade['Trade Balance'] = region_trade['Exports_Cleaned_Billion'] - region_trade['Imports_Cleaned_Billion']
       
        fig_trade_balance = px.bar(
            region_trade,
            x='Region',
            y='Trade Balance',
            color='Trade Balance',
            color_continuous_scale='RdYlGn'
        )
        fig_trade_balance.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=0, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Trade Balance (Billion USD)"
        )
        fig_trade_balance.update_xaxes(tickangle=45)
        st.plotly_chart(fig_trade_balance, use_container_width=True)
   
    with col4:
        st.markdown('<div class="section-header">GDP Distribution by Region</div>', unsafe_allow_html=True)
        fig_box = px.box(
            df,
            x='Region',
            y='gdp_total_usd_billion_cleaned',
            color='Region',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_box.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=0, b=30),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="GDP (Billion USD)"
        )
        fig_box.update_xaxes(tickangle=45)
        st.plotly_chart(fig_box, use_container_width=True)
 
 
# Trade Analysis Dashboard
 
elif section == "Trade Analysis":
   
    # Trade metrics
    total_exports = df['Exports_Cleaned_Billion'].sum()
    total_imports = df['Imports_Cleaned_Billion'].sum()
    trade_surplus_countries = len(df[df['Trade Balance'] > 0])
    trade_deficit_countries = len(df[df['Trade Balance'] < 0])
    avg_trade_openness = df['Trade_Openness'].mean()
   
    col1, col2, col3, col4, col5 = st.columns(5)
   
    with col1:
        st.metric("Global Exports", f"${total_exports:,.0f}B")
    with col2:
        st.metric("Global Imports", f"${total_imports:,.0f}B")
    with col3:
        st.metric("Trade Surplus", f"{trade_surplus_countries} countries")
    with col4:
        st.metric("Trade Deficit", f"{trade_deficit_countries} countries")
    with col5:
        st.metric("Avg Trade Openness", f"{avg_trade_openness:.1f}%")
   
    # Main trade visualizations
    col1, col2 = st.columns([3, 2])
   
    with col1:
        st.markdown('<div class="section-header">Global Trade Balance</div>', unsafe_allow_html=True)
        top_traders = df.nlargest(15, 'gdp_total_usd_billion_cleaned')
       
        fig_trade_bal = go.Figure()
        fig_trade_bal.add_trace(go.Bar(
            name='Exports',
            x=top_traders['Country'],
            y=top_traders['Exports_Cleaned_Billion'],
            marker_color='#00d4aa'
        ))
        fig_trade_bal.add_trace(go.Bar(
            name='Imports',
            x=top_traders['Country'],
            y=-top_traders['Imports_Cleaned_Billion'],
            marker_color='#ff6b6b'
        ))
       
        fig_trade_bal.update_layout(
            barmode='relative',
            height=280,
            margin=dict(l=0, r=0, t=0, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Trade Value (Billion USD)",
            xaxis_title=""
        )
        fig_trade_bal.update_xaxes(tickangle=45)
        st.plotly_chart(fig_trade_bal, use_container_width=True)
   
    with col2:
        st.markdown('<div class="section-header">Top Trade Partners</div>', unsafe_allow_html=True)
        df['Total Trade'] = df['Exports_Cleaned_Billion'] + df['Imports_Cleaned_Billion']
        top_trade = df.nlargest(10, 'Total Trade')
       
        fig_top_trade = px.bar(
            top_trade,
            y='Country',
            x='Total Trade',
            orientation='h',
            color='Total Trade',
            color_continuous_scale='Blues'
        )
        fig_top_trade.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Total Trade (Billion USD)",
            yaxis_title=""
        )
        st.plotly_chart(fig_top_trade, use_container_width=True)
   
    # Bottom visualizations
    col3, col4 = st.columns(2)
   
    with col3:
        st.markdown('<div class="section-header">Trade Openness vs GDP</div>', unsafe_allow_html=True)
        fig_openness = px.scatter(
            df,
            x='GDP_per_capita_ppp_cleaned',
            y='Trade_Openness',
            size='gdp_total_usd_billion_cleaned',
            color='Region',
            hover_name='Country',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_openness.update_layout(
            height=220,
            margin=dict(l=0, r=0, t=0, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="GDP per Capita (PPP)",
            yaxis_title="Trade Openness (%)"
        )
        st.plotly_chart(fig_openness, use_container_width=True)
   
    with col4:
        st.markdown('<div class="section-header">Regional Trade Shares</div>', unsafe_allow_html=True)
        region_exports = df.groupby('Region')['Exports_Cleaned_Billion'].sum().reset_index()
        fig_regional_trade = px.pie(
            region_exports,
            values='Exports_Cleaned_Billion',
            names='Region',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_regional_trade.update_layout(
            height=220,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_regional_trade, use_container_width=True)
 
 
 
# Download Data
 
elif section == "Download Data":
        st.markdown("<div class='section-title'>Download Cleaned Dataset</div>", unsafe_allow_html=True)
       
        # Download button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇ Download CSV",
            data=csv_data,
            file_name="economic_intelligence_dataset.csv",
            mime="text/csv"
        )
       
        # Display data table
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.dataframe(
            df.head(100),
            use_container_width=True,
            height=400
        )
 
 
# Footer
 
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.8rem; margin-top: 1rem;'>"
    "Economic Intelligence Platform | Data Source: Economic Intelligence Dataset | "
    "Built with Streamlit & Plotly</div>",
    unsafe_allow_html=True
)

 
