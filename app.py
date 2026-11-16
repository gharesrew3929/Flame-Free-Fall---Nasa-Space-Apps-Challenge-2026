import streamlit as st
import pandas as pd
import plotly.express as px
import re
st.set_page_config(
  page_title="AstrFlame AI | Microgravity Fire Safety Insights",
  page_icon="🔥",
  layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("bass_data.csv")
    df.columns = [c.strip() for c in df.columns]

    planned_df = pd.read_csv("planned_test_matrix.csv", skiprows=2)
    planned_df.columns = [c.strip() for c in planned_df.columns]

    return df, planned_df
  
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
    elif "slab" in s:
        return "Slab"
    elif "fabric" in s or "sheet" in s:
        return "Fabric / Sheet"
    else:
        return "Unspecified / Other"

  def extract_size_cm(val):
    match = re.search(r"(\d+(?:\.\d+)?)\s*cm", str(val).lower())
    return float(match.group(1)) if match else None

  df["Material_Category"] = df["Fuel Sample Material"].apply(extract_category)
  df["Geometry"] = df["Fuel Sample Material"].apply(extract_geometry)
  df["Sample_Size_cm"] = df["Fuel Sample Material"].apply(extract_size_cm)
  df["Date_Clean"] = pd.to_datetime(df["Date"], errors="coerce")
  return df, planned_df
df, planned_df = load_data()

st.title("AstroFlame AI: Microgravity Combustio & Spacecraft Fire Safety")
st.markdown(
  "**NASA Space Apps Challenge 2026 - Flame in Freefall** | "
  "Powered by **NASA Physical Sciences Informatics (PSI-26: BASS ISS Investigation)**"
)

st.sidebar.header("🛸Spacecraft Cabin & Test Filters")
selected_materials = st.sidebar.multiselect(
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
cabin_o2 = st.sidebar.slider("Cabin Oxygen Concentration (%)", min_value=15, max_value=100, value=21)
cabin_airflow = st.sidebar.slider("Ventilation Airflow Velocity (cm/s)", min_value=0, max_value=50, value=15)

filtered_df = df[
  (df["Material_Category"].isin(selected_materials)) &
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
      y="Fuel Sample Material",
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
    timeline_df,
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
    st.subheader("🔬 BASS Configuration Explorer")

    st.write(
        "Explore planned NASA BASS experimental configurations, "
        "including fuel materials, sample geometry, ignition settings, "
        "and experimental setup parameters."
    )

    st.info(
        "This dataset describes planned experimental configurations. "
        "It does not report measured flame behavior or fire-safety outcomes."
    )

    # Identify relevant columns
    fuel_col = next(
        c for c in planned_df.columns
        if c.lower().startswith("fuel descript")
    )

    test_col = "Test Point"
    sample_col = "Sample Number"

    # Remove empty rows and preserve grouped material descriptions
    config_df = planned_df.copy()

    config_df = config_df[
        config_df[test_col].notna()
    ].copy()

    config_df[fuel_col] = (
        config_df[fuel_col]
        .replace("", pd.NA)
        .ffill()
    )

    config_df[sample_col] = (
        config_df[sample_col]
        .replace("", pd.NA)
        .ffill()
    )

    # Material selection
    materials = sorted(
        config_df[fuel_col].dropna().unique()
    )

    selected_fuel = st.selectbox(
        "Select a fuel material",
        materials
    )

    material_data = config_df[
        config_df[fuel_col] == selected_fuel
    ]

    # Summary metrics
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Planned test points",
        len(material_data)
    )

    c2.metric(
        "Sample identifiers",
        material_data[sample_col].nunique()
    )

    c3.metric(
        "Fuel material",
        selected_fuel
    )

    st.markdown("### Planned Configuration Records")

    st.dataframe(
        material_data,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Material Configuration Overview")

    material_counts = (
        config_df.groupby(fuel_col)[test_col]
        .count()
        .sort_values(ascending=False)
    )

    st.bar_chart(material_counts)

    st.caption(
        "Counts represent listed test points in the planned matrix, "
        "not completed experiments or successful combustion tests."
    )

with tab3:
  st.subheader("🔬 Scientific Methodology & NASA Data Attribution")
  st.markdown("""
  ### 1. Primary NASA Open Dataset
  * **Source:** NASA Physical Sciences Informatics (PSI) Data Repository
  * **Investigation:** **PSI-26 -- Burning and Suppression of Solids (BASS)** conducted aboard the International Space Station (ISS).
  * **Dataset File:** 'PSI-26_Experimental table_BASS.csv` (Microgravity solid-fuel combustion test matrix across PMMA spheres/slabs, SIBAL cotton-fiberglass blends, and Nomex fabrics).
  
  ### 2. Why Microgravity Combustion Differs from Earth (1g)
  * On Eath, hot combustion gases rise due to **buoyancy**, drawing fresh oxygen into the base of a flame.
  * In microgravity (**0g**), buoyancy disappears. Flames become spherical, cooler, and governed entirely by **molecular diffusion** and **forced spacecraft ventilation**
  * Surprisingly, NASA's BASS experiments demonstrated that certain solid materials burn at **lower oxygen concentrations in microgravity** under gentle airflow than the they do on Earth.

  ### 3. Additional NASA Reference Sources
  * *A Researcher's Guide to International Space Station Combustion Science* (NASA ISS Program Science Office)
  * *Apollo 1 & Apollo 13 Historical Investigation Archives* (NASA)
  * *25 Years Ago: Fire Aboard Space Station Mir* (NASA History)
  """)


    



      

