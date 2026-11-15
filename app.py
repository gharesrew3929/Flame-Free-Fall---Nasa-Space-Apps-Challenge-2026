import streamlit as st
import pandas as pd
import plotly.express as px
import pe

st.set_page_config(
  page_title="AstrFlame AI | Microgravity Fire Safety Insights",
  page_icon="🔥",
  layout="wide"
)

@st.cache_data
def load_data():
  df = pd.read_csv("bass_data.csv")
  df.columns = [c.strip() for c in df.columns]

  def extract_category(val):
    s = str(val).upper()
    if "PMMA" in s:
      return "PMMA (Acrylic Polymer)"
    elif "SIBAL" in s:
      return "SIBAL (Cotton/Fiberglass Blend)"
    elif "NOMEX" in s:
      return "Nomex Blend (Flame-Resistant)"
    return "Other Solid Fuel"

  def extract_geometry(val):
    s = str(val).lower()
    if "sphere" in s:
      return "Sphere"
    elif "rod" in s:
      return "Rod"
    return "Slab / Fabric Sheet"

  def extract_size_cm(val):
    match = re.search(r"(\d+(?:\.\dt)?)\s*cm", str(val).lower())
    return float(match.group(1)) if match else None

  df["Material_Category"] = df["Fuel Sample Material"].apply(extract_category)
  df["Geometry"] = df["Fuel Sample Material"].apply(extract_geometry)
  df["Sample_Size_cm"] = df["Fuel Sample Material"].apply(extract_size_cm
  df["Date_Clean"] = pd.to_datetime(df["Date"], errors="coerce")
  return df

df = load_data()

st.title("AstroFlame AI: Microgravity Combustio & Spacecraft Fire Safety")
st.markdown(
  "**NASA Space Apps Challenge 2026 - Flame in Freefall** | "
  "Powered by **NASA Physical Sciences Informatics (PSI-26: BASS ISS Investigation)**"
)

st.sidebar.header("🛸Spacecraft Cabin & Test Filters")
selected_materials = st.sidebar.multiselect{
  "Filter Fuel Material Category",
  options=sorted(df["Material_Category"].unique()),
  default=sorted(df["Material_Category"].unique())
)

selected_geometries = st.sidebar.multiselect(
  "Filter Sample Geometry",
  options=sorted(df["Geometry"].unique()),
  default=sorted(df["Geometry"].unique())
)

st.sidebar.markdown("---")
st.sidebar.header("🧪 Cabin Environment Simulator")
cabin-02 = st.sidebar.slider("Cabin Oxygen Concentration (%)", min_value=15, max_value=100, value=21)
cabin_airflow = st.sidebar.slider("Ventilation Airflow Velocity (cm/s)", min_value=0, max_value=50, value=15)
  ]

      

