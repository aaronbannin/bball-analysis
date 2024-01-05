import streamlit as st
from streamlit import chat_message

from bball_analysis.context import enrich_user_message, SessionStateManager
from bball_analysis.mappings import TEAM_NAMES
from bball_analysis.prompts import Prompts


context = SessionStateManager(st.session_state)

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

        enriched = Prompts.user_question_prompt.render(
            user_input=prompt,
            # this is ugly, no concept of state within the graph
            # should probably use the `http` class?
            datasets=",".join([t for t in context.agent.datasets.keys()]),
        )
        response = context.agent.chat(enriched)

        context.add_assistant_message(response)
        chat_message("assistant").write(response)
