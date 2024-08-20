from openai import OpenAI
import streamlit as st
import streamlit_authenticator as stauth

from utils import make_intro, reset_conversation, get_authenticator

make_intro()
authenticator = get_authenticator()
authenticator.login()


if st.session_state["authentication_status"]:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Clear Chat")
        with col2:
            st.button("🔄", on_click=reset_conversation)
        st.title("Configuration")

        st.session_state["openai_model"] = st.selectbox(
            "Select a model",
            [
                "gpt-4o",
                "gpt-4-turbo-preview",
                "gpt-3.5-turbo",
                "gpt-4",
            ],
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🙂"):
            st.markdown(prompt)

        with st.chat_message(
            "assistant",
            avatar="https://static-00.iconduck.com/assets.00/openai-icon-2021x2048-4rpe5x7n.png",
        ):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
