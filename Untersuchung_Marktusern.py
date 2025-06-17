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
        color_palette = px.colors.qualitative.Set3

        # Car Verteilung Gesamt
        car_counts = df['Car'].value_counts().reset_index()
        car_counts.columns = ['Car', 'Anzahl']

        # Farbdictionary erstellen (alle Fahrzeugtypen)
        unique_cars = car_counts['Car'].unique()
        colors_cars_dict = {
            car: color_palette[i % len(color_palette)] for i, car in enumerate(unique_cars)
        }

        # Pie-Chart erstellen
        fig_cars = px.pie(
            car_counts,
            names='Car',
            values='Anzahl',
            title="🚘 Verteilung der EVs nach Fahrzeugtyp",
            color='Car',
            color_discrete_map=colors_cars_dict
        )

        # Darstellung verbessern
        fig_cars.update_traces(
            textinfo='percent+label',
            textposition='inside',
            insidetextorientation='radial'
        )

        fig_cars.update_layout(
            title_font_size=24,
            legend_title_text='Fahrzeugtyp',
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor='center'),
            margin=dict(t=50, b=50, l=0, r=0)
        )

        st.plotly_chart(fig_cars, use_container_width=True)
