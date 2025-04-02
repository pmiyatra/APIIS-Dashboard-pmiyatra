import pandas as pd
import streamlit as st

# Streamlit File Uploader (for Streamlit Cloud)
uploaded_file = st.file_uploader("Upload the dashboard file", type=["xlsx"])

if uploaded_file is not None:
    # Load dashboard from uploaded file
    df_dashboard = pd.read_excel(uploaded_file, sheet_name="WBR APIIS")

    # Rename columns to A, B, C, ...
    df_dashboard.columns = [chr(65 + i) for i in range(len(df_dashboard.columns))]

    # Remove column A
    if "A" in df_dashboard.columns:
        df_dashboard.drop(columns=["A"], inplace=True)

    # Replace 'None' values with blanks
    df_dashboard.replace(to_replace=[None, "None", pd.NA, "nan", "NaN"], value="", inplace=True)

    # Strip whitespace from all cells
    df_dashboard = df_dashboard.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Forward-fill values to simulate merged cells in Excel
    df_dashboard.ffill(inplace=True)

    # Drop rows where all values are empty after stripping
    df_dashboard = df_dashboard.replace("", pd.NA).dropna(how="all")

    # Apply text wrapping in Streamlit
    def style_dataframe(df):
        return df.style.set_properties(**{'white-space': 'pre-wrap'})

    # Streamlit app layout
    st.set_page_config(layout="wide")
    st.title("Dashboard Viewer")

    st.subheader("WBR APIIS Sheet Preview")
    st.table(df_dashboard)  # `st.table()` for better formatting

else:
    st.warning("Please upload an Excel file to view the dashboard.")

