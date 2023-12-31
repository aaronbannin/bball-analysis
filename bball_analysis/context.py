import random
from typing import Optional

from loguru import logger
from streamlit.runtime.state import SessionStateProxy

from bball_analysis.http_service import HTTPService
from bball_analysis.llm import Agent
from bball_analysis.mappings import Team, TEAM_NAMES, TEAM_TO_TEAM_ABBREVIATION


def enrich_user_message(message: str, content: list[str]):
    """
    Add retrieved information into message.
    """
    as_string = "\n".join(content)
    return f"{message}\n\n{as_string}"

class SessionStateManager:
    """
    Manages Streamlit's session_state.
    Provides a type-hintable interface.
    For each object you want in state, add as a property.

    You should not add any view methods; it will mess up rendering.
    """
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

    def seed_user_messages(self, messages: list[str]):
        self.state["messages"] = []
        for m in messages:
            self.add_user_message(m)

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

    def _add_message(self, role: str, message: str):
        if "messages" not in self.state:
            raise KeyError("No messages in state")

        self.messages.append({"role": role, "content": message})

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

        logger.info(f"team_picker {self.team_picker} current_team {self.team}")
        if self.team is not None and self.team_picker == self.team:
            # no change, do nothing
            return

        self.team = self.team_picker
        _team = Team(self.team)
        logger.info(f"team: {self.team} {TEAM_TO_TEAM_ABBREVIATION[_team]}")

        overview = self.http.team_overview(self.team)
        seed_message = f"I am researching the NBA team {self.team}."

        # reset memory for streamlit and openai
        self.agent.reset()
        self.agent.add_datasets(overview.tables)
        self.seed_user_messages([seed_message])
        enriched_content = [str(overview.summary), "you have the following data sets availiable", ",".join([t for t in overview.tables.keys()])]
        seed_msg_response = self.agent.chat(enrich_user_message(seed_message, enriched_content))
        self.add_assistant_message(seed_msg_response)
