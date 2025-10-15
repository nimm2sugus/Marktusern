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

        # Zeilen entfernen, bei denen 'End Time' ungültig ist, da sie für die Analyse entscheidend sind
        df.dropna(subset=['End Time'], inplace=True)

        df['Jahr'] = df['End Time'].dt.year
        df['Monat'] = df['End Time'].dt.to_period('M').astype(str)

        st.write(df)

        # --- Farbpalette ---
        color_palette = px.colors.qualitative.Set3

        # Fahrzeugverteilung berechnen
        car_counts = df['Car'].value_counts().reset_index()
        car_counts.columns = ['Car', 'Anzahl']

        unique_cars = car_counts['Car'].unique()
        colors_cars_dict = {
            car: color_palette[i % len(color_palette)] for i, car in enumerate(unique_cars)
        }

        # === 🚘 Pie-Chart ===
        st.subheader("🚘 Verteilung der EVs nach Fahrzeugtyp")
        fig_cars = px.pie(
            car_counts,
            names='Car',
            values='Anzahl',
            title="Fahrzeugverteilung (gesamt)",
            color='Car',
            color_discrete_map=colors_cars_dict,
            hole=0.3  # Donut-Stil
        )

        fig_cars.update_traces(
            textinfo='percent+label',
            textposition='inside',
            insidetextorientation='radial'
        )

        fig_cars.update_layout(
            title_font_size=24,
            height=600,
            legend_title_text='Fahrzeugtyp',
            legend=dict(orientation="v", y=0.5, x=1.05),
            margin=dict(t=80, b=50, l=50, r=150)
        )

        st.plotly_chart(fig_cars, use_container_width=True)

        # === 📊 Zeitlicher Verlauf als gestapeltes Bar-Chart (Absolute Zahlen) ===
        st.subheader("📊 Zeitlicher Verlauf: Fahrzeugverteilung pro Monat (Absolute Zahlen)")

        car_month = df.groupby(['Monat', 'Car']).size().reset_index(name='Anzahl')
        car_month = car_month.sort_values('Monat') # Sortieren der Monate für korrekte Darstellung

        fig_bar = px.bar(
            car_month,
            x='Monat',
            y='Anzahl',
            color='Car',
            color_discrete_map=colors_cars_dict,
            title='Monatliche Verteilung der Fahrzeuge (gestapelt)'
        )

        fig_bar.update_layout(
            xaxis_title='Monat',
            yaxis_title='Anzahl Ladevorgänge',
            title_font_size=24,
            legend_title_text='Fahrzeugtyp',
            barmode='stack',
            height=600,
            margin=dict(t=80, b=50, l=50, r=50),
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # === NEU: 📈 Zeitlicher Verlauf der prozentualen Anteile ===
        st.subheader("📈 Monatliche Entwicklung der Fahrzeug-Anteile")

        fig_bar_percent = px.bar(
            car_month,
            x='Monat',
            y='Anzahl',
            color='Car',
            color_discrete_map=colors_cars_dict,
            title='Monatliche Anteile der Fahrzeuge (Normalisiert auf 100%)',
            barnorm='percent'  # Dieser Parameter normalisiert die Balken auf 100%
        )

        fig_bar_percent.update_layout(
            xaxis_title='Monat',
            yaxis_title='Anteil der Ladevorgänge (%)',
            title_font_size=24,
            legend_title_text='Fahrzeugtyp',
            barmode='stack',
            height=600,
            margin=dict(t=80, b=50, l=50, r=50),
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_bar_percent, use_container_width=True)
