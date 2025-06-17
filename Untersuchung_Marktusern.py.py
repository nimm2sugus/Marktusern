import streamlit as st
import pandas as pd
import plotly.express as px

# Funktion zum Laden der Excel-Datei
@st.cache_data
def load_excel_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return None

# Streamlit-Seitenlayout
st.set_page_config(page_title="Untersuchung Marktusern", layout="wide")
st.title("Untersuchung Marktusern")

# Datei-Upload
uploaded_file = st.file_uploader("📁 Bereinigte Excel-Datei hochladen", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = load_excel_file(uploaded_file)

    if df is not None:
        st.subheader("Originaldaten nach Datenformatanpassung")

        df = df.copy()
        df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')
        df['Peak Power (kW)'] = pd.to_numeric(df['Peak Power (kW)'], errors='coerce')
        df['Average Power (kW)'] = pd.to_numeric(df['Average Power (kW)'], errors='coerce')
        df['Average Amp (A)'] = pd.to_numeric(df['Average Amp (A)'], errors='coerce')

        df['Jahr'] = df['End Time'].dt.year
        df['Monat_num'] = df['End Time'].dt.month
        df['Tag'] = df['End Time'].dt.day
        df['Stunde'] = df['End Time'].dt.hour

        st.write(df, use_container_width=True)

        # --- Farbzuordnungen ---
        colors_cars = px.colors.qualitative.Plotly

        # Car Verteilung Gesamt
        prov_counts = df['Car'].value_counts().reset_index()
        prov_counts.columns = ['Car', 'Anzahl']

        fig_cars = (px.pie(prov_counts, names='Provider', values='Anzahl',
                          title="🏢 Top 10 Provider + Rest (gesamt)",
                          color='Provider',
                          color_discrete_map=colors_cars))
        st.plotly_chart(fig_cars, use_container_width=True)
