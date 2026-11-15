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

filtered_df = df[
  (df["Matersial_Category"].isin(selected_materials)) &
  (df["Geometry"].isin(selected_geometries))
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total ISS Burn Tests", len(filtered_df))
col2.metric("Unique Fuel Configurations", filtered_df["Fuel Sample Material"].nunique())
col3.metric("Distinct Sample Batches", filtered_df["Sample #"].nunique())
avg_size = filtered_df["Sample_Size_cm"].mean()
col4.metric("Avg Characteristic Size", f"{avg_size:.2f} cm" if pd.notna(avg_size) else "N/A")

st.markdown("---")

tab1, tab2, tab3 = st.tabs([
  "📊ISS BASS Combustion Explorer",
  "🤖 AI Spacecraft Fire-Safety Advisor",
  "🔬 Scientific Methodology & NASA Citations"
])

with tab1: 
  c1, c2 = st.columns(2)

  with c1:
    st.subheader("Microgravity Tests by Fuel Configuration")
    mat_counts = filtered_df["Fuel Sample Material"].value_counts().reset_index()
    mat_counts.columns = ["Fuel Sample Material", "Test Count"]
    fig1 = px.bar(
      mat_counts,
      x="Test Count",
      y="Fuel Sample Material".
      orientation="h",
      color="Test Count",
      color_continuous_scale="Y1OrRd"
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
    st.plotly_chart(fig1, use_container_width=True)

  with c2:
    st.subheader("Material Class & Geometry Breakdown")
    sunburst_df = filtered_df.groupby(["Material_Category", "Geometry"]).size().reset_index(name="Count")
    fig2 = px.sunburst(
      sunburst_df,
      path=["Material_Category", "Geometry"],
      values="Count",
      color="Material_Category"
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

  st.subheader("ISS Experiment TImeline (Test Sequence vs. GMT Day)")
  timeline_df = filtered_df.dropna(subset=["GMT", "As Run Test #"])
  fig3 = px.scatter(
    timelinw_df,
    x="GMT",
    y="As Run Test #",
    color="Material_Category",
    symbol="Geometry",
    hover_data=["Date", "Test #", "Sample #", "Fuel Sample Material"],
    title="BASS Experimental Campaign Progression on the International Space Station"
  )
  st.plotly_chart(fig3, use_container_width=True)

  with st.expander("📄 View Raw Filtered NASA PSI-26 Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

with tab2:
  st.subheader("🤖 Automated Spacecraft Fire-Safety Risk Synthesis")
  st.write(
    "Combines **ISS BASS microgravity material testing patterns** with simulated spacecraft cabin parameters "
    "and historical NASA fire incident lessons (**Apollo 1** & **Space Station Mir 1997**)."
  )

  o2_factor = min(max((cabin_o2 - 16) * 1.4, 0), 65)

  if cabin_airflow == 0:
    flow_factor = 10
  elif 2 <= cabin_airflow <= 25:
    flow_factor = 25
  else:
    flow_factor = 12

  mat_risk = 10
  if "PMMA (Acrylic Polymer)" in selected_materials:
    mat_risk += 12
  id "SIBAL (Cotton/Fiberglass Blend)" in selected_materials:
    mat_risk += 8
  
  


    



      

