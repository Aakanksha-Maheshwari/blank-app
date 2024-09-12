import streamlit as st
import numpy as np
from openai import OpenAI

# Show title and description.
st.title("📄 My Lab 3 question answering Chatbox")
openai_model = st.sidebar.selectbox("Which Model?", ("mini", "regular"))
buffer_size = st.sidebar.slider("Buffer Size", min_value=1, max_value=10, value=2, step=1)
if openai_model =="mini":
    model_to_use ="gpt-4o-mini"
else:
    model_to_use ="gpt-4o"

if 'client' not in st.session_state:
    api_key =st.secrets["openai_key"]
    st.session_state.client = OpenAI(api_key=api_key)
if "messages" not in st.session_state:
    st.session_state["messages"] =\
        [{"role":"assistant","content":"How can I help you"}]
for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

if prompt:= st.chat_input("what is up"):
    st.session_state.messages.append({"role":"user","content":prompt})
    # Limit the buffer to the specified size
    if len(st.session_state.messages) > buffer_size * 2:
        st.session_state.messages = st.session_state.messages[-buffer_size * 2:]
    with st.chat_message("user"):
        st.markdown(prompt)
    client =st.session_state.client
    stream = client.chat.completions.create(
        model =model_to_use,
        messages =st.session_state.messages,
        stream = True,
        max_tokens=300)
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant","content":response})
    
    more_info_prompt = "Do you want more information?"
    with st.chat_message("assistant"):
        st.write(more_info_prompt)
    st.session_state.messages.append({"role": "assistant", "content": more_info_prompt})

    # Get user input for more information.
    if follow_up := st.chat_input("Please type 'yes' or 'no':"):
        st.session_state.messages.append({"role": "user", "content": follow_up})

        if follow_up.lower() == "yes":
            # If user says 'yes', provide more info.
            with st.chat_message("assistant"):
                more_info_response = f"Here's some additional info: {response}"  # Adjust based on logic.
                st.write(more_info_response)
            st.session_state.messages.append({"role": "assistant", "content": more_info_response})
            
            # Ask again after providing more info.
            with st.chat_message("assistant"):
                st.write("Do you want help with other questions?")
            st.session_state.messages.append({"role": "assistant", "content": "Do you want help with other questions?"})
        
        elif follow_up.lower() == "no":
            # If user says 'no', ask if they need help with other questions.
            next_question_prompt = "Do you want help with other questions?"
            with st.chat_message("assistant"):
                st.write(next_question_prompt)
            st.session_state.messages.append({"role": "assistant", "content": next_question_prompt})


    # Limit messages to buffer size after completing the flow.
    if len(st.session_state.messages) > buffer_size * 2:
        st.session_state.messages = st.session_state.messages[-buffer_size * 2:]