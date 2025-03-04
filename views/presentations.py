import streamlit as st
from utils.presentation import find_presentations
import pandas as pd
from config import config

def presentations():
    st.title("Presentations")

    with st.spinner("Loading"):
        presentations = list(find_presentations())
        if not presentations:
            st.info("No presentations found.")

        else:
            df = pd.DataFrame([
                {
                    "Title": p["title"],
                    "Created On": p["created_on"],
                    "Link": f"[View]({config['STATIC_CONTENT_ENDPOINT']}/{p['directory']}/dist/)"
                }
                for p in presentations
            ])

            st.table(df)  