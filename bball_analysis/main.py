import streamlit as st
import pandas as pd
from basketball_reference_web_scraper import client as bbr_client
from basketball_reference_web_scraper.data import Team
from loguru import logger

# from openai import OpenAI
from llm import client as openai, Agent

INITIAL_PROMPT = "I am your AI driven analyst. What team would you like to research?"
st.title('Lets play basketball!')


agent = Agent()

# team = Team(team_name)

# standings_json = bbr_client.standings(season_end_year=2024)
# standings = pd.DataFrame.from_dict(standings_json)
# st.write(standings)

# st.write(standings_json)

def set_chat_context():
    seed_messages = [
        {"role": "user", "content": f"I am researching the NBA team {team_name}."}
    ]

    if "messages" not in st.session_state:
        st.session_state["messages"] = seed_messages


team_name = st.selectbox(
    INITIAL_PROMPT,
    [t.value for t in Team],
    index=None
    # placeholder="Choose an option"
)

if team_name is not None:
    if "messages" not in st.session_state:
        seed_messages = [
            # {"role": "user", "content": f"I am researching the NBA team {team_name}."}
        ]
        # seed_messages = [{
        #     "role": "assistant", "content": INITIAL_PROMPT
        # }]
        st.session_state["messages"] = seed_messages

    # st.session_state.messages.append({"role": "user", "content": f"I am researching the NBA team {team_name}."})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        response = agent.chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

