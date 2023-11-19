import re
from dataclasses import dataclass
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup
from pandas import read_html, DataFrame

from mappings import Team, TEAM_TO_TEAM_ABBREVIATION

@dataclass
class BBallTable:
    id: str
    class_name: str
    caption: Optional[str]
    thead: str
    table: DataFrame

    @classmethod
    def from_soup(cls, soup: BeautifulSoup):
        caption = soup.find('caption')
        thead = soup.find('thead')

        # should only be one table, but bs4 returns array
        df = read_html(str(soup))[0]

        return cls(
            id=soup.get('id'),
            class_name=soup.get('class'),
            caption=caption.get_text() if caption is not None else None,
            thead=thead.get_text() if thead is not None else None,
            table=df
        )


@dataclass
class TeamOverview:
    tables: dict[str, BBallTable]
    summary: Any

class HTTPService:
    BASE_URL = 'https://www.basketball-reference.com'


    def __init__(self):
        self.season_end_year = 2024

    def _get(self, url: str) -> BeautifulSoup:
        response = requests.get(url=url, allow_redirects=False)
        response.raise_for_status()

        # some content may be commented out
        clean_html = re.sub(r'<!--|-->', '', response.text, flags=re.DOTALL)
        return BeautifulSoup(clean_html, 'html.parser')

    def team_overview(self, team_name: str):
        team_code = TEAM_TO_TEAM_ABBREVIATION[Team(team_name)]
        url = f"{self.BASE_URL}/teams/{team_code}/{self.season_end_year}.html"

        page = self._get(url)
        summary_soup = page.find('div', attrs={'data-template': 'Partials/Teams/Summary'})
        for script in summary_soup(["script"]):
            script.extract()  # Remove script tags and their contents

        summary = "".join(summary_soup.find_all(text=True))
        summary = re.sub(r'\n+', '\n', summary)

        all_tables = [BBallTable.from_soup(t) for t in page.find_all('table')]

        return TeamOverview(
            tables={t.caption: t for t in all_tables if t.id is not None},
            summary=summary
        )
