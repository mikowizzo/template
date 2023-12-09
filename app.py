from openai import OpenAI
import streamlit as st
from streamlit import session_state as ss

client = OpenAI()

if "model" not in ss:
    ss.sys_msg = "Role: python coder,Instructions: respond with code examples where possible with as few characters as possible."
    ss.model = "gpt-3.5-turbo"
    ss.messages = [{'role':'system','content':ss.sys_msg}]

with st.sidebar:
    ss.sys_msg = st.text_area('System message')
    ss.model = st.radio('Model',['gpt-3.5-turbo-1106', 'gpt-4-1106-preview'], horizontal=True)
    if st.button("New Chat"):
        ss.messages = [{'role':'system','content':ss.sys_msg}]
    ss.max_history = st.slider('Max history', 0, 20, 0)

for m in ss.messages: st.chat_message(m["role"]).markdown(m["content"])

if prompt := st.chat_input("What is up?"):
    ss.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=ss.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in ss.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    ss.messages.append({"role": "assistant", "content": full_response})

#Number of messages to keep
if ss.max_history == 0:
    ss.messages = [ss.messages[0]]
elif len(ss.messages) > ss.max_history:
    ss.messages = [ss.messages[0]] + ss.messages[-ss.max_history:]


with st.sidebar, st.expander('Session state', expanded = False): ss