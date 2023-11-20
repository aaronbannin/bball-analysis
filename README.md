# Your Personal NBA Analyst
[Streamlit App](https://bball-analysis.streamlit.app/)

# Local Setup
- Install [Poetry](https://python-poetry.org/docs/).
- Create `.env` file and add `OPEN_AI_API_KEY`.
- Install dependancies: `poetry install`.
- Create agent: using the virtual environment `poetry shell` and then `python cli.py deploy-agent`.
- Launch the page: `streamlit run bball_analysis/main.py`.
