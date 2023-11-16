from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
import streamlit as st
import pandas as pd


st.title('Lets play basketball!')


team_name = st.selectbox(
    "What team would you like to research?",
    [t.value for t in Team]
)

team = Team(team_name)

standings_json = client.standings(season_end_year=2024)
standings = pd.DataFrame.from_dict(standings_json)
st.write(standings)

st.write(standings_json)


