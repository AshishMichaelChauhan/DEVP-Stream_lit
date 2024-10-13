# 📦 Import-Export Dashboard

Welcome to the **Import-Export Transactions Dashboard**! This dashboard provides an in-depth analysis of global trade flows by year, country, and category, offering visual insights into the patterns of imports and exports across different timeframes.

The following is the link to my streamlit dashboard:
https://devp-app-2uwghzwzzhr5yckc2app2wh.streamlit.app/

## 🛠 Features

- **Data Visualization**: Interactive visualizations including:
  - Bar Chart for top 10 countries by transaction value.
  - Line Chart showing the trend of transaction values over time.
  - Pie Chart representing value distribution by category.
  - Heatmap for category-wise transactions over time.
  - **Violin Plot** to visualize distribution of transaction values by country.
  - **Box Plot** to compare transaction values by shipping method.
  - Stacked Area Chart for cumulative transaction values.
  - Sunburst Chart for breakdown by category and country.

- **Interactive Filters**:
  - Filter data by **year**.
  - Select specific **countries** for deeper analysis.
  - Choose from various **color themes** for visual customizations.

- **Metrics**:
  - Highlights the **top and bottom countries** by transaction value.
  - Shows **year-over-year** transaction differences for selected countries.

## 🖥 Demo

Explore the dashboard features and interact with the visualizations using the available filters to get the most out of the dataset.

![Dashboard Screenshot](dashboard-screenshot.png)

## 📊 Dataset

The dashboard is powered by the **Imports_Exports_Dataset.csv** file, which includes transaction records of various countries over different years. Each record contains the following fields:
- `Date`: Date of the transaction.
- `Country`: Country involved in the transaction.
- `Value`: Value of the import/export transaction.
- `Category`: Category of the goods involved.
- `Shipping_Method`: Method used for shipping the goods.

## 🏗️ Installation and Setup

Follow these steps to set up and run the project on your local machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/import-export-dashboard.git
   cd import-export-dashboard
