import streamlit as st
from views.bot import bot
from views.presentations import presentations

st.sidebar.write(f"Presentation AI")
st.logo('images/logo.png', size='large')
pages = [
    st.Page(bot, url_path= "bot", title="Chat Bot"),
    st.Page(presentations, url_path= "presentations", title="Presentations"),
]
pg = st.navigation(pages)
pg.run()

