import streamlit as st
import re
import os
from utils.file import load_file
from openai import OpenAI
from config import config
from utils.presentation import generate_presentation


def bot():
    st.title("Presentation as Code Bot")
    
    instructions = load_file(os.path.join("resources", "instructions.txt"))
    client = OpenAI(
        # base_url=config['OPENAI_API_ENDPOINT'],
        api_key=config['OPENAI_API_KEY']
    )

    st.session_state.setdefault('messages', [{"role": "system", "content": instructions}])
    st.session_state.setdefault('builded', False)
    st.session_state.setdefault('presentation_id', None)

    for message in st.session_state.messages:
        if message["role"] != 'system':
            with st.chat_message(message["role"]):
                st.text(message["content"])

    if prompt := st.chat_input("Give me a topic about presentation?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=config['OPENAI_API_MODEL'],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            text_container = st.empty()
            full_text = "" 

            for chunk in stream:
                 if chunk.choices and chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content 
                    text_container.text(full_text.replace("<<START_SLIDEV>>", "").replace("<<END_SLIDEV>>", ""))

        st.session_state.messages.append({"role": "assistant", "content": full_text})
        st.session_state.builded = False

    col1, col2, col3, _ = st.columns([2,2,2,5])
    last_assistant_response = next(iter(reversed([m for m in st.session_state.messages if m['role'] == 'assistant'])), None)
    if last_assistant_response:
        with col1:
            build_button = st.button("Build", key="build", disabled=st.session_state.builded, use_container_width=True)
            if build_button:
                with st.spinner('Generating...'):
                    if match := re.search(r"<<START_SLIDEV>>(.*?)<<END_SLIDEV>>", last_assistant_response['content'], re.DOTALL):
                        presentation_id = generate_presentation(match.group(1).strip())
                        st.session_state.presentation_id = presentation_id
                        st.session_state.builded = True
                    else:
                        st.error('LLM model returned wrong data.')

    if st.session_state.builded:
        with col2:
            st.link_button("View", f"{config['STATIC_CONTENT_ENDPOINT']}/{st.session_state.presentation_id}/dist/", use_container_width=True)
        with col3:
            clean_button = st.button('Clean', use_container_width=True  )
            if clean_button:
                st.session_state.presentation_id = None
                st.session_state.builded = False
                st.session_state.messages = [{"role": "system", "content": instructions}]
                st.rerun()
