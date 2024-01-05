from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from bball_analysis.http_service import TeamOverview


cwd = Path.cwd()

@pytest.fixture
def saved_page():
    file_name = "2023-24 Milwaukee Bucks Roster and Stats _ Basketball-Reference.com.html"
    with open(cwd / "tests" / "data" / file_name, 'r') as file:
        data = file.read()

    return data

def test_team_overview(saved_page):
    soup = BeautifulSoup(saved_page, 'html.parser')
    overview = TeamOverview.from_soup(soup)

    table_names = {'Roster Table', 'Injury Report Table', 'Team and Opponent Stats Table', 'Team Misc Table', 'Per Game Table', 'Totals Table', 'Per 36 Minutes Table', 'Per 100 Poss Table', 'Advanced Table', 'Adjusted Shooting Table', 'Shooting Table', 'Play-by-Play Table', 'Salaries Table', 'Draft Rights Table'}
    parsed_table_names = set(overview.tables.keys())
    table_name_diff = table_names.symmetric_difference(parsed_table_names)

    assert len(table_name_diff) == 0

    print(overview.links)
    assert len(overview.links.keys()) == 1
