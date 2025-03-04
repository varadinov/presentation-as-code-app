import streamlit as st
from views.bot import bot
from views.presentations import presentations

st.sidebar.write(f"Presentation AI")
pages = [
    st.Page(bot, url_path= "bot", title="Chat Bot"),
    st.Page(presentations, url_path= "presentations", title="Presentations"),
]
pg = st.navigation(pages)
st.logo('images/logo.png', size='large')
pg.run()

