import pandas as pd
import streamlit as st

# File path
dashboard_path = "APIIS_Deck_PRIYA MIYATRA.xlsx"

# Load dashboard
df_dashboard = pd.read_excel(dashboard_path, sheet_name="WBR APIIS")

# Rename columns to A, B, C, ...
df_dashboard.columns = [chr(65 + i) for i in range(len(df_dashboard.columns))]

# Remove column A
df_dashboard.drop(columns=["A"], inplace=True)

# Replace 'None' values with blanks
df_dashboard.replace(to_replace=[None, "None", pd.NA, "nan", "NaN"], value="", inplace=True)

# Strip whitespace from all cells
df_dashboard = df_dashboard.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Forward-fill values to simulate merged cells in Excel
df_dashboard.ffill(inplace=True)

# Drop rows where all values are empty after stripping
df_dashboard = df_dashboard.replace("", pd.NA).dropna(how="all")

def style_dataframe(df):
    """Apply styling to wrap text in cells."""
    return df.style.set_properties(**{'white-space': 'pre-wrap'})

# Streamlit app
st.set_page_config(layout="wide")
st.title("Dashboard Viewer")

st.subheader("WBR APIIS Sheet Preview")
st.dataframe(style_dataframe(df_dashboard))
