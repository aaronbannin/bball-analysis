import random
from typing import Optional, TypedDict

import streamlit as st
from loguru import logger
from pydantic import BaseModel as PydanticBaseModel

from http_service import HTTPService
from llm import Agent
from mappings import Team, TEAM_TO_TEAM_ABBREVIATION
from prompts import Prompts


import asyncio
# import streamlit as st

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Context(BaseModel):
    messages: list[str]
    agent: Agent
    # team_picker: Optional[str]
    team: Optional[str] = None


# class SessionState:
#     def __init__(self, messages: list[str], agent: Agent):
#         pass

#     @property
#     def messages(self) -> list[str]:

async def periodic():
    while True:
        logger.info("Hello world")
        r = await asyncio.sleep(1)
        logger.info(f"asyncio sleep ? {r}")


# asyncio.run(periodic())

http = HTTPService()

if "ctx" not in st.session_state:
    # agent =
    logger.info("setting up context")
    st.session_state["ctx"] = Context(messages=[], agent=Agent())

context: Context = st.session_state["ctx"]
# if st.session_state.get("agent") is None:
#     st.session_state["agent"] = Agent()
TEAMS = [t.value for t in Team]

# utility functions
def set_random_team(ctx: Context):
    team = random.choice(TEAMS)
    logger.info(f"Picked {team} randommly")
    # st.session_state["team"] = None
    ctx.team = None
    st.session_state["team_picker"] = team
    return set_chat_context(ctx)

def set_chat_context(ctx: Context):
    """
    Creates a clean context for chat.
    Mutates st.session_state and the agent as side effects.
    Probably should be a closure to make this a pure function?
    """

    team = st.session_state.get("team_picker")
    current_team = ctx.team
    logger.info(f"team_picker {team} current_team {current_team}")
    if current_team is not None and current_team == team:
        # no change, do nothing
        return

    # st.session_state["team"] = team
    ctx.team = team
    _team = Team(team)
    logger.info(f"team: {team} {TEAM_TO_TEAM_ABBREVIATION[_team]}")

    overview = http.team_overview(team)
    seed_message = f"I am researching the NBA team {team}."
    seed_messages = [
        {"role": "user", "content": seed_message}
    ]

    # reset memory for streamlit and openai
    ctx.agent.set_thread()
    # st.session_state["agent"].set_thread()
    ctx.agent.add_datasets(overview.tables)
    # st.session_state["agent"].add_datasets(overview.tables)
    ctx.messages = seed_messages
    # st.session_state["messages"] = seed_messages
    enriched_content = [str(overview.summary), "you have the following data sets availiable", ",".join([t for t in overview.tables.keys()])]
    seed_msg_response = ctx.agent.chat(enrich_user_message(seed_message, enriched_content))
    ctx.messages.append({"role": "role", "content": seed_msg_response})
    # st.session_state.messages.append({"role": "role", "content": seed_msg_response})


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
    TEAMS,
    index=None,
    key="team_picker",
    on_change=set_chat_context,
    # kwargs=dict(ctx=context)
    args=(context,)
)
st.button(
    "Random",
    on_click=set_random_team,
    args=(context,)
    # kwargs=dict(ctx=context)
)

if team_name is not None and "messages" in context:
    for msg in context.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        context.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = context.agent.chat(prompt)
        # asyncio.run(agent.oai_chat(prompt))
        # response = await agent.oai_chat(prompt)

        # context.messages.append({"role": "assistant", "content": response})
        context.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
