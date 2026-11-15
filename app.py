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
