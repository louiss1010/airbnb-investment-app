# The home page of the app

import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st

st.set_page_config(page_title="Airbnb Investment App", layout="wide")

CITIES = ["London"]
PERSONAS = ["First-time investor", "Portfolio landlord", "Risk-averse buyer"]

# Selections saved in session_state so every page can read them
city = st.sidebar.selectbox("City", CITIES, index=CITIES.index(st.session_state.get("city", "London")))
persona = st.sidebar.selectbox("Persona", PERSONAS, index=PERSONAS.index(st.session_state.get("persona", PERSONAS[0])))
st.session_state["city"], st.session_state["persona"] = city, persona

st.title("Airbnb Investment App")
st.write("Find where and what to buy for short-term letting. Pick a city and persona, then use the pages in the sidebar.")
st.caption("Data: Inside Airbnb snapshot (date TBC). Estimates only, not financial advice.")