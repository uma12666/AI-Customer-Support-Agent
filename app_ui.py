import streamlit as st
from agent import process_message

st.title("🤖 AI Customer Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    if message["role"] == "user":
        st.write(f"👤 You: {message['content']}")

    else:
        st.write(f"🤖 Agent: {message['content']}")

user_input = st.text_input("Enter your message")

if st.button("Send"):

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = process_message(user_input)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()