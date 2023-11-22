import random
from typing import Any, Optional

from loguru import logger
from streamlit import chat_message
from streamlit.runtime.state import SessionStateProxy

from bball_analysis.http_service import HTTPService
from bball_analysis.llm import Agent
from bball_analysis.mappings import Team, TEAM_NAMES, TEAM_TO_TEAM_ABBREVIATION


# TEAMS = [t.value for t in Team]

def enrich_user_message(message: str, content: list[str]):
    """
    Add retrieved information into message.
    """
    as_string = "\n".join(content)
    return f"{message}\n\n{as_string}"

class SessionStateManager:
    def __init__(self, session_state: SessionStateProxy) -> None:
        self.state = session_state

        if "messages" not in self.state:
            self.state.messages = []

        if "agent" not in self.state:
            self.state.agent = Agent()

        self.http = HTTPService()

    @property
    def agent(self) -> Agent:
        return self.state.agent

    @property
    def messages(self) -> list[dict[str, str]]:
        return self.state.messages

    @property
    def team_picker(self) -> Optional[str]:
        return self.state.get("team_picker")

    @team_picker.setter
    def team_picker(self, team: str):
        self.state["team_picker"] = team

    @property
    def team(self) -> Optional[str]:
        return self.state.get("team")

    @team.setter
    def team(self, name: str):
        self.state["team"] = name

    # def _setter(self, key: str, value: Any):
    #     self.state[key] = value

    def populate_chat_messages(self):
        for msg in self.messages:
            chat_message(msg["role"]).write(msg["content"])


    def _add_message(self, role: str, message: str):
        if "messages" not in self.state:
            raise KeyError("No messages in state")

        self.messages.append({"role": role, "content": message})
        chat_message(role).write(message)

    def add_user_message(self, message: str):
        return self._add_message("user", message)

    def add_assistant_message(self, message: str):
        return self._add_message("assistant", message)

    def set_random_team(self):
        team = random.choice(TEAM_NAMES)
        logger.info(f"Picked {team} randommly")
        self.team = None
        self.team_picker = team
        return self.set_chat_context()

    def set_chat_context(self):
        """
        Creates a clean context for chat.
        Mutates st.session_state and the agent as side effects.
        Probably should be a closure to make this a pure function?
        """

        # team = st.session_state.get("team_picker")
        # current_team = st.session_state.get("team")
        logger.info(f"team_picker {self.team_picker} current_team {self.team}")
        if self.team is not None and self.team_picker == self.team:
            # no change, do nothing
            return

        # st.session_state["team"] = team
        self.team = self.team_picker
        _team = Team(self.team)
        logger.info(f"team: {self.team} {TEAM_TO_TEAM_ABBREVIATION[_team]}")

        overview = self.http.team_overview(self.team)
        seed_message = f"I am researching the NBA team {self.team}."
        seed_messages = [
            {"role": "user", "content": seed_message}
        ]

        # reset memory for streamlit and openai
        # st.session_state["agent"].set_thread()
        self.agent.set_thread()
        # st.session_state["agent"].add_datasets(overview.tables)
        self.agent.add_datasets(overview.tables)
        self.add_user_message(seed_message)
        # st.session_state["messages"] = seed_messages
        enriched_content = [str(overview.summary), "you have the following data sets availiable", ",".join([t for t in overview.tables.keys()])]
        seed_msg_response = self.agent.chat(enrich_user_message(seed_message, enriched_content))
        self.add_assistant_message(seed_msg_response)
        # st.session_state.messages.append({"role": "assistant", "content": seed_msg_response})
