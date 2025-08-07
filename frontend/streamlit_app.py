# streamlit connects to flask blah blah

import streamlit as st
import requests
import uuid

st.title("RC Chatbot Test")

if "chat_id" not in st.session_state:
    try:
        start_resp = requests.post("http://localhost:5050/create_chat")
        start_resp.raise_for_status()
        st.session_state.chat_id = start_resp.json().get("chat_id")
        st.success(f"Connected! Chat ID: {st.session_state.chat_id}")
    except Exception as e:
        st.error(f"Failed to start session: {type(e).__name__}: {e}")

question = st.text_input("Ask me something")

# Step 3: Send to Flask backend when input is given
if question:
    try:
        payload = {
            "chat_id": st.session_state.chat_id,
            "query": question
        }

        response = requests.post(
            "http://localhost:5050/query",
            json=payload
        )
        response.raise_for_status() # throws error if not status 200


        data = response.json()
        st.markdown("**Answer:** " + data.get("response", "No answer returned."))

        sources = data.get("sources",[])
        if sources: 
            st.markdown("**Sources:**")
            for i, src in enumerate(sources,1):
                st.markdown(f"{i}. [{src}]({src})")

        st.markdown("**Raw Response:**")
        st.json(data)
    except Exception as e:
        st.error(f"Error: {type(e).__name__}: {e}")