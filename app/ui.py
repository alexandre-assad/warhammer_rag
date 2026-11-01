import streamlit as st
from app.graph import app, config

def launch_app():
    st.title("Warhammer Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your question..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Looking in the rules and in the database..."):
                try:
                    inputs = {
                        "query": prompt,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    result = app.invoke(inputs, config=config)
                    answer = result["answer"]

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Erreur d'exécution : {str(e)}")