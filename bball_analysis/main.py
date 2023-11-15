from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType, Team
import streamlit as st
import pandas as pd

# print(client.team_box_scores(day=1, month=1, year=2023))

st.title('Lets play basketball!')


team_name = st.selectbox(
    "What team would you like to research?",
    [t.value for t in Team]
    # placeholder="Can you give me a short summary?",
    # disabled=not uploaded_file,
)

team = Team(team_name)

standings_json = client.standings(season_end_year=2024)
standings = pd.DataFrame.from_dict(standings_json)
# st.write(standings[standings['team'] == team])
st.write(standings)

st.write(standings_json)


