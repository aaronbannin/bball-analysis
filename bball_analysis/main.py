from typing import Any

import streamlit as st
from basketball_reference_web_scraper.data import Team, TEAM_TO_TEAM_ABBREVIATION
from loguru import logger

from http_service import HTTPService
from llm import Agent
from prompts import Prompts


http = HTTPService()
if st.session_state.get("agent") is None:
    st.session_state["agent"] = Agent()


# utility functions
def set_chat_context():
    """
    Creates a clean context for chat.
    Mutates st.session_state and the agent as side effects.
    Probably should be a closure to make this a pure function?
    """

    team = st.session_state.get("team_picker")
    current_team = st.session_state.get("team")
    logger.info(f"team_picker {team} current_team {current_team}")
    if current_team is not None and current_team == team:
        # no change, do nothing
        return

    st.session_state["team"] = team
    _team = Team(team)
    logger.info(f"team: {team} {TEAM_TO_TEAM_ABBREVIATION[_team]}")

    overview = http.team_overview(team)
    seed_message = f"I am researching the NBA team {team}."
    seed_messages = [
        {"role": "user", "content": seed_message}
    ]

    # reset memory for streamlit and openai
    st.session_state["agent"].set_thread()
    st.session_state["messages"] = seed_messages
    seed_msg_response = st.session_state["agent"].chat(enrich_user_message(seed_message, overview.summary))
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
    key="team_picker",
    on_change=set_chat_context
)

if team_name is not None and "messages" in st.session_state:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = st.session_state["agent"].chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
