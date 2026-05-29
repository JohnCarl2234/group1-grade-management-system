from pathlib import Path
import sys
import time
 
import pandas as pd
import streamlit as st
 

st.set_page_config(
    page_title="Student Dashboard - Grade Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))