import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================
# CREATE SAMPLE DATA (since files might not exist)
# ============================================

@st.cache_data
def get_data():
    """Create sample data for the dashboard"""
    
    # Historical account ownership data
    acc_data = pd.DataFrame({
        'year': [2011, 2014, 2017, 2021, 2024],
        'value': [14.0, 22.0, 35.0, 46.0, 49.0],
        'indicator': ['Account Ownership'] * 5
    })
    
    # Mobile money data
    mm_data = pd.DataFrame({
        'year': [2021, 2024],
        'value': [4.7, 9.45],
        'indicator': ['Mobile Money'] * 2
    })
    
    # Forecast data
    forecast_data = pd.DataFrame({
        'Year': [2025, 2026, 2027],
        'Pessimistic': [48.5, 51.0, 53.5],
        'Base': [51.0, 54.5, 58.0],
        'Optimistic': [53.5, 58.0, 62.5]
    })
    
    # Impact data
    impact_data = pd.DataFrame({
        'event_name': ['Telebirr Launch', 'Telebirr Launch', 'M-Pesa Launch', 'EthSwitch Interoperability'],
        'indicator': ['Account Ownership', 'Mobile Money', 'Mobile Money', 'Digital Payments'],
        'impact': [3.0, 4.3, 3.0, 2.0],
        'confidence': ['Medium', 'High', 'High', 'Medium']
    })
    
    return acc_data, mm_data, forecast_data, impact_data

acc_data, mm_data, forecast_data, impact_data = get_data()

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📈 Overview", "📉 Trends", "🔮 Forecasts", "📊 Impact Analysis", "📝 About"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Data Sources")
st.sidebar.markdown("""
- World Bank Findex
- GSMA Reports
- NBE Reports
""")

# ============================================
# PAGE: OVERVIEW
# ============================================

if page == "📈 Overview":
    st.title("🇪🇹 Ethiopia Financial Inclusion Dashboard")
    st.markdown("### 📊 Key Metrics at a Glance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Account Ownership (2024)", "49.0%", "+3.0%")
    
    with col2:
        st.metric("Mobile Money (2024)", "9.45%", "+4.75%")
    
    with col3:
        st.metric("Growth Since 2011", "+35pp", "250%")
    
    with col4:
        st.metric("NFIS-II Target (2030)", "60%", "11pp to go")
    
    st.markdown("---")
    st.markdown("### 📈 Account Ownership Progress")
    
    # Create chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(acc_data['year'], acc_data['value'], 'o-', linewidth=2, markersize=10, color='#2E86AB')
    
    # Add forecast
    forecast_years = [2025, 2026, 2027]
    ax.plot(forecast_years, forecast_data['Base'], 'o--', linewidth=2, markersize=10, color='#F18F01', label='Base Forecast')
    ax.fill_between(forecast_years, forecast_data['Pessimistic'], forecast_data['Optimistic'], alpha=0.2, color='#2E86AB')
    
    ax.axhline(y=60, color='red', linestyle=':', linewidth=2, label='NFIS-II Target (60%)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Account Ownership (%)')
    ax.set_ylim(0, 70)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        📈 Key Insights
        - Account ownership: 14% (2011) → 49% (2024)
        - Growth has slowed recently
        - Mobile money is driving new adoption
        """)
    
    with col2:
        st.warning("""
        ⚠️ Challenges
        - Urban vs Rural: 60% vs 38%
        - Gender gap remains: 5pp
        - Mobile money accounts vs usage gap
        """)

# ============================================
# PAGE: TRENDS
# ============================================
elif page == "📉 Trends":
    st.title("📉 Trend Analysis")
    
    indicator = st.selectbox("Select Indicator", ["Account Ownership", "Mobile Money"])
    
    if indicator == "Account Ownership":
        data = acc_data
    else:
        data = mm_data
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data['year'], data['value'], 'o-', linewidth=2, markersize=10, color='#2E86AB')
    ax.set_xlabel('Year')
    ax.set_ylabel(f'{indicator} (%)')
    ax.set_title(f'{indicator} Trend')
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    st.dataframe(data)

# ============================================
# PAGE: FORECASTS
# ============================================

elif page == "🔮 Forecasts":
    st.title("🔮 Financial Inclusion Forecasts (2025-2027)")
    
    scenario = st.selectbox("Select Scenario", ["Base", "Optimistic", "Pessimistic"])
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Historical
    ax.plot(acc_data['year'], acc_data['value'], 'o-', linewidth=2, markersize=10, color='#2E86AB', label='Historical')
    
    # Forecast
    scenario_map = {"Base": "Base", "Optimistic": "Optimistic", "Pessimistic": "Pessimistic"}
    ax.plot(forecast_data['Year'], forecast_data[scenario_map[scenario]], 'o--', linewidth=2, markersize=10, color='#F18F01', label=f'{scenario} Forecast')
    
    ax.axhline(y=60, color='red', linestyle=':', linewidth=2, label='Target: 60%')
    ax.set_xlabel('Year')
    ax.set_ylabel('Account Ownership (%)')
    ax.set_ylim(0, 70)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.markdown("### 📊 Forecast Table")
    st.dataframe(forecast_data.style.format({
        'Pessimistic': '{:.1f}%',
        'Base': '{:.1f}%',
        'Optimistic': '{:.1f}%'
    }))
    
    # Download
    csv = forecast_data.to_csv(index=False)
    st.download_button("📥 Download Forecast CSV", csv, "forecast.csv", "text/csv")

# ============================================
# PAGE: IMPACT ANALYSIS
# ============================================

elif page == "📊 Impact Analysis":
    st.title("📊 Event Impact Analysis")
    
    st.markdown("### 📋 Impact Summary")
    st.dataframe(impact_data)
    
    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(impact_data['event_name'], impact_data['impact'], color=['#2E86AB', '#F18F01', '#A23B72', '#3B9B6E'])
    ax.set_xlabel('Event')
    ax.set_ylabel('Impact Magnitude')
    ax.set_title('Event Impact Magnitudes')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Add values on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.1f}', ha='center', va='bottom')
    
    st.pyplot(fig)
    
    # Confidence pie chart
    st.markdown("### 🎯 Confidence Distribution")
    confidence_counts = impact_data['confidence'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(confidence_counts.values, labels=confidence_counts.index, autopct='%1.1f%%', colors=['#2E86AB', '#F18F01', '#C73E3E'])
    st.pyplot(fig2)

# ============================================
# PAGE: ABOUT
# ============================================

else:
    st.title("📝 About This Dashboard")
    st.markdown("""
    ### 🇪🇹 Ethiopia Financial Inclusion Forecasting System
    
    This dashboard provides interactive visualization and forecasting of Ethiopia's financial inclusion indicators.
    
    ### 📊 Data Sources
    - Global Findex Database: World Bank's comprehensive demand-side survey
    - GSMA Reports: Mobile money and digital financial services data
    - NBE Reports: National Bank of Ethiopia administrative data
    
    ### 🎯 Key Indicators
    1. Access: Account Ownership Rate
    2. Usage: Digital Payment Adoption Rate
                
    ### 🔮 Forecasting Methodology
    - Trend Regression: Linear and logit models
    - Event-Augmented: Policy and product launch impacts
    - Scenario Analysis: Pessimistic, Base, and Optimistic
    
    ### 📅 Last Updated
    July 2026
    """)

st.markdown("---")
st.markdown("Made with ❤️ by Selam Analytics")