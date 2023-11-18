from typing import Any

import streamlit as st
import pandas as pd
from basketball_reference_web_scraper import client as bbr_client
from basketball_reference_web_scraper.data import Team, TEAM_TO_TEAM_ABBREVIATION
from loguru import logger

from http_service import HTTPService
from llm import Agent
from prompts import Prompts


agent = Agent()
http = HTTPService()

# utility functions
def set_chat_context():
    ctx_team = st.session_state["team"]
    _team = Team(ctx_team)
    logger.info(f"team: {ctx_team} {TEAM_TO_TEAM_ABBREVIATION[_team]}")

    overview = http.team_overview(ctx_team)
    seed_message = f"I am researching the NBA team {ctx_team}."
    seed_messages = [
        {"role": "user", "content": seed_message}
    ]

    st.session_state["messages"] = seed_messages
    seed_msg_response = agent.chat(enrich_user_message(seed_message, overview.summary))
    st.session_state.messages.append({"role": "role", "content": seed_msg_response})


def enrich_user_message(message: str, content: Any):
    """
    Add retrieved information into message.
    """
    return f"{message}\n\n{content}"


# app
st.title("Talkin' Some Bball Outside of the School")
team_name = st.selectbox(
    Prompts.initial_user_prompt.render(),
    [t.value for t in Team],
    index=None,
    key="team",
    on_change=set_chat_context
)

if team_name is not None and "messages" in st.session_state:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = agent.chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
