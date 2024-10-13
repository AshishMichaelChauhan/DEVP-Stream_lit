# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Import-Export Dashboard",
    page_icon="📦",
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
    st.title('📦 Import-Export Dashboard')

    # Filter by year
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
    return f"${val / 1e6:.1f}M" if val > 1e6 else f"${val / 1e3:.1f}K"

def calculate_transaction_difference(input_df, input_year):
    selected_year_data = input_df[input_df['Date'].dt.year == input_year].reset_index()
    previous_year_data = input_df[input_df['Date'].dt.year == input_year - 1].reset_index()
    selected_year_data['value_difference'] = selected_year_data.Value.sub(previous_year_data.Value, fill_value=0)
    return pd.concat([selected_year_data.Country, selected_year_data.Value, selected_year_data.value_difference], axis=1).sort_values(by="value_difference", ascending=False)

#######################
# Dashboard Main Panel
st.markdown("<h1 style='text-align: center; color: #004d40;'>📦 Import-Export Transactions Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #004d40;'>Comprehensive analysis of global trade flows by year and country</h4>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Display key metrics in card layout
df_transaction_diff_sorted = calculate_transaction_difference(df, selected_year)

first_country = df_transaction_diff_sorted.Country.iloc[0] if selected_year > df['Date'].dt.year.min() else '-'
first_country_value = format_value(df_transaction_diff_sorted.Value.iloc[0])
first_country_delta = format_value(df_transaction_diff_sorted.value_difference.iloc[0]) if selected_year > df['Date'].dt.year.min() else '-'

last_country = df_transaction_diff_sorted.Country.iloc[-1] if selected_year > df['Date'].dt.year.min() else '-'
last_country_value = format_value(df_transaction_diff_sorted.Value.iloc[-1])
last_country_delta = format_value(df_transaction_diff_sorted.value_difference.iloc[-1]) if selected_year > df['Date'].dt.year.min() else '-'

# Metrics in a card layout
st.markdown(f"""
<div class='metric-container'>
    <div class='metric-box'>
        <div class='metric-title'>Top Country by Value</div>
        <div class='metric-value'>{first_country}</div>
        <div class='metric-delta'>Difference: {first_country_delta}</div>
    </div>
    <div class='metric-box'>
        <div class='metric-title'>Lowest Country by Value</div>
        <div class='metric-value'>{last_country}</div>
        <div class='metric-delta'>Difference: {last_country_delta}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

#######################
# New Insights Section
st.markdown("### Key Insights:")
insight_1 = f"*Top Country*: {first_country} had the highest transaction value of {first_country_value}, reflecting its dominance in the selected trade data."
insight_2 = f"*Bottom Country*: {last_country} had the lowest transaction value of {last_country_value}, indicating it contributed less to the overall trade."
insight_3 = f"The selected countries combined have seen varied growth across trade categories, with noticeable peaks and troughs across specific time frames."
st.write(insight_1)
st.write(insight_2)
st.write(insight_3)

#######################
# Additional Graphs Section
col1, col2 = st.columns(2)

with col1:
    st.markdown('#### Top 10 Countries by Transaction Value')
    
    # Bar chart for top countries
    top_10_countries = df_selected_year.groupby('Country')['Value'].sum().reset_index().sort_values(by='Value', ascending=False).head(10)
    bar_chart = alt.Chart(top_10_countries).mark_bar().encode(
        x=alt.X('Value:Q', title='Transaction Value'),
        y=alt.Y('Country:N', sort='-x', title='Country'),
        color=alt.Color('Country:N', scale=alt.Scale(scheme=selected_color_theme))
    ).properties(width=600, height=400)
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.markdown('#### Transactions Over Time')
    
    # Line chart for transactions over time
    line_chart = alt.Chart(df_selected_year).mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(title='Date')),
        y=alt.Y('Value:Q', axis=alt.Axis(title='Transaction Value')),
        color=alt.Color('Category:N', legend=alt.Legend(title="Category"))
    ).properties(width=600, height=400)
    st.altair_chart(line_chart, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Pie chart for value distribution by category
st.markdown('#### Value Distribution by Category')

pie_chart = px.pie(df_selected_year, values='Value', names='Category', title="Value Distribution by Category",
                   color_discrete_sequence=px.colors.sequential.RdBu)
pie_chart.update_traces(textinfo='percent+label')
st.plotly_chart(pie_chart, use_container_width=True)

# Heatmap for transactions by category over time
st.markdown('#### Category-Wise Heatmap')

heatmap = alt.Chart(df_selected_year).mark_rect().encode(
    y=alt.Y('Category:O', axis=alt.Axis(title="Category")),
    x=alt.X('Date:T', axis=alt.Axis(title="Date")),
    color=alt.Color('Value:Q', scale=alt.Scale(scheme=selected_color_theme)),
).properties(width=900, height=300)
st.altair_chart(heatmap, use_container_width=True)

#######################
# New Charts Added
st.markdown('#### Stacked Area Chart: Cumulative Transaction Values Over Time')
# Stacked Area Chart
area_chart = alt.Chart(df_selected_year).mark_area().encode(
    x='Date:T',
    y='Value:Q',
    color='Category:N',
    tooltip=['Date', 'Value']
).properties(width=900, height=300)
st.altair_chart(area_chart, use_container_width=True)

st.markdown('#### Sunburst Chart: Category and Country Breakdown')
# Sunburst Chart
sunburst_chart = px.sunburst(df_selected_year, path=['Category', 'Country'], values='Value', title='Sunburst Chart: Category and Country Breakdown',
                             color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(sunburst_chart, use_container_width=True)

#######################
# Violin Plot
st.markdown('#### Violin Plot: Distribution of Transaction Values by Country')
# Violin Plot
violin_chart = px.violin(df_selected_year, y='Value', x='Country', color='Country',
                         box=True, points="all", title="Violin Plot: Transaction Value Distribution by Country")
st.plotly_chart(violin_chart, use_container_width=True)

#######################
# Box Plot
st.markdown('#### Box Plot: Transaction Value by Shipping Method')
# Box Plot
box_chart = px.box(df_selected_year, x='Shipping_Method', y='Value', color='Shipping_Method', 
                   title="Box Plot: Transaction Value by Shipping Method")
st.plotly_chart(box_chart, use_container_width=True)

#######################
# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("##### Created by Ashish Michael Chauhan | Import-Export Dashboard © 2024", unsafe_allow_html=True)
