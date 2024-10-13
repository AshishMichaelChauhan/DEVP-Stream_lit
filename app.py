# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Import-Export Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

# Set background color for the whole page
page_bg_color = """
  <style>
  body {
      background-color: #e8f5e9;
  }
  .metric-container {
      display: flex;
      justify-content: space-between;
  }
  .metric-box {
      padding: 15px;
      margin: 5px;
      border-radius: 10px;
      background-color: #ffffff;
      box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
      text-align: center;
  }
  .metric-title {
      font-size: 16px;
      font-weight: bold;
      color: #333333;
  }
  .metric-value {
      font-size: 20px;
      color: #007bff;
  }
  .metric-delta {
      color: #ff6b6b;
  }
  </style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

alt.themes.enable("dark")

#######################
# Load data
df_data = pd.read_csv('Imports_Exports_Dataset.csv')
df = df_data.sample(n=3001, random_state=55007)
#######################
# Sidebar
with st.sidebar:
    st.title(' Import-Export Dashboard')

    # Filter by years
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    year_list = sorted(df['Date'].dt.year.unique(), reverse=True)
    selected_year = st.selectbox('Select a year', year_list)

    # Filter data based on selected year
    df_selected_year = df[df['Date'].dt.year == selected_year]

    # Multi-select for country
    country_list = df['Country'].unique()
    selected_countries = st.multiselect('Select country(s)', country_list, default=country_list[:3])  # Default first 3

    if selected_countries:
        df_selected_year = df_selected_year[df_selected_year['Country'].isin(selected_countries)]

    # Select color theme
    color_theme_list = ['blues', 'reds', 'greens', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#######################
# Helper Functions
def format_value(val):
    return f"<span class="math-inline">\{val / 1e6\:\.1f\}M" if val \> 1e6 else f"</span>{val / 1e3:.1f}K"


def calculate_transaction_difference(input_df, input_year):
    selected_year_data = input_df[input_df['Date'].dt.year == input_year]

    # Check if there's data for the previous year
    if input_year > input_df['Date'].dt.year.min():
        previous_year_data = input_df[input_df['Date'].dt.year == input_year - 1]
        selected_year_data['value_difference'] = selected_year_data.Value.sub(previous_year_data.Value, fill_value=0)
    else:
        selected_year_data['value_difference'] = 0  # No previous year data, set difference to 0

    return pd.concat([selected_year_data.Country, selected_year_data.Value, selected_year
