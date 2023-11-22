import random

import streamlit as st
from streamlit import chat_message
from streamlit.runtime.state import SessionStateProxy
from loguru import logger

from bball_analysis.context import SessionStateManager
from http_service import HTTPService
from llm import Agent
from mappings import Team, TEAM_TO_TEAM_ABBREVIATION, TEAM_NAMES
from prompts import Prompts


# class SessionStateManager:
#     def __init__(self, session_state: SessionStateProxy) -> None:
#         self.state = session_state

#         if "messages" not in self.state:
#             self.state.messages = []

#         if "agent" not in self.state:
#             self.state.agent = Agent()

#     @property
#     def agent(self) -> Agent:
#         return self.state.agent

#     @property
#     def messages(self) -> list[dict[str, str]]:
#         return self.state.messages

#     def populate_chat_messages(self):
#         for msg in self.messages:
#             chat_message(msg["role"]).write(msg["content"])


#     def _add_message(self, role: str, message: str):
#         if "messages" not in self.state:
#             raise KeyError("No messages in state")

#         self.messages.append({"role": role, "content": message})
#         chat_message(role).write(message)

#     def add_user_message(self, message: str):
#         return self._add_message("user", message)

#     def add_assistant_message(self, message: str):
#         return self._add_message("assistant", message)

http = HTTPService()
context = SessionStateManager(st.session_state)
# TEAMS = [t.value for t in Team]

# utility functions
def set_random_team():
    team = random.choice(TEAM_NAMES)
    logger.info(f"Picked {team} randommly")
    st.session_state["team"] = None
    st.session_state["team_picker"] = team
    return set_chat_context()

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
    st.session_state["agent"].add_datasets(overview.tables)
    st.session_state["messages"] = seed_messages
    enriched_content = [str(overview.summary), "you have the following data sets availiable", ",".join([t for t in overview.tables.keys()])]
    seed_msg_response = st.session_state["agent"].chat(enrich_user_message(seed_message, enriched_content))
    st.session_state.messages.append({"role": "assistant", "content": seed_msg_response})


def enrich_user_message(message: str, content: list[str]):
    """
    Add retrieved information into message.
    """
    as_string = "\n".join(content)
    return f"{message}\n\n{as_string}"


# app
st.title("Talkin' Some Bball Outside of the School")
team_name = st.selectbox(
    Prompts.initial_user_prompt.render(),
    TEAM_NAMES,
    index=None,
    key="team_picker",
    on_change=set_chat_context
)
st.button(
    "Random",
    on_click=set_random_team
)

if team_name is not None and "messages" in st.session_state:
    context.populate_chat_messages()

    if prompt := st.chat_input():
        context.add_user_message(prompt)

        response = context.agent.chat(prompt)
        context.add_assistant_message(response)
