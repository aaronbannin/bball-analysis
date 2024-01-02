import streamlit as st
from streamlit import chat_message

from bball_analysis.context import SessionStateManager
from mappings import TEAM_NAMES
from prompts import Prompts


context = SessionStateManager(st.session_state)

import logging
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig()
# logging.getLogger("llama_index.agent.openai_agent").setLevel(logging.DEBUG)
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# print(loggers)

# app
st.title("Talkin' Some Bball Outside of the School")
team_name = st.selectbox(
    Prompts.initial_user_prompt.render(),
    TEAM_NAMES,
    index=None,
    key="team_picker",
    on_change=context.set_chat_context
)

st.button(
    "Random",
    on_click=context.set_random_team
)

if team_name is not None and len(context.messages) > 0:
    for msg in context.messages:
        chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        context.add_user_message(prompt)
        chat_message("user").write(prompt)

        response = context.agent.chat(prompt)
        context.add_assistant_message(response)
        chat_message("assistant").write(response)
