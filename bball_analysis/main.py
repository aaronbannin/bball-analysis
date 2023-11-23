import asyncio

import streamlit as st
from loguru import logger
from streamlit import chat_message

from bball_analysis.context import SessionStateManager
from bball_analysis.mappings import TEAM_NAMES
from bball_analysis.prompts import Prompts


context = SessionStateManager(st.session_state)
message_queue = asyncio.Queue()

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def periodic():
    msg = message_queue.get()
    chat_message(msg["role"]).write(msg["content"])
    # while True:
    #     idx = 0
    #     for msg in message_queue:
    #         chat_message(msg["role"]).write(msg["content"])
    #         idx += 1

    #     message_queue = message_queue[idx:]


asyncio.run(periodic())

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
        logger.info(f"Rendering message: {msg}")
        chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        context.add_user_message(prompt)
        # chat_message("user").write(prompt)
        message_queue.put_nowait({"role": "user", "content": prompt})

        response = context.agent.chat(prompt)
        context.add_assistant_message(response)
        # chat_message("assistant").write(response)
        message_queue.put_nowait({"role": "assistant", "content": response})
