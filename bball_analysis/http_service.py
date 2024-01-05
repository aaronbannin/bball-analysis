import re
from dataclasses import dataclass
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup
from pandas import read_html, DataFrame

from bball_analysis.mappings import Team, TEAM_TO_TEAM_ABBREVIATION


BASE_URL = 'https://www.basketball-reference.com'

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
    links: dict[str, str]

    @classmethod
    def from_soup(cls, soup: BeautifulSoup):
        # team_code = TEAM_TO_TEAM_ABBREVIATION[Team(team_name)]
        # url = f"{http.BASE_URL}/teams/{team_code}/{http.season_end_year}.html"

        # page = self._get(url)
        summary_soup = soup.find('div', attrs={'data-template': 'Partials/Teams/Summary'})
        for script in summary_soup(["script"]):
            script.extract()  # Remove script tags and their contents

        # team links
        link_dict = {}
        div = soup.find('div', attrs={'id': 'inner_nav'})
        links = div.find_all('li')
        # need to find link elements
        for link in links:
            # Get the href attribute (the URL)
            # href = link.find('href')
            a = link.find('a')
            href = a["href"]
            txt = a.get_text(strip=True)

            # Get the visible text associated with the link
            # Using .get_text() to get the visible text and stripping to remove leading/trailing whitespaces
            # text = link.get_text(strip=True)
            print(f"text={txt} href={href} link={link}")

            # Add to dictionary if not already present (to deduplicate)
            if href not in link_dict:
                link_dict[txt] = href

        summary = "".join(summary_soup.find_all(string=True))
        summary = re.sub(r'\n+', '\n', summary)

        all_tables = [BBallTable.from_soup(t) for t in soup.find_all('table')]

        return cls(
            tables={t.caption: t for t in all_tables if t.id is not None},
            summary=summary,
            links=link_dict
        )

    def _get_links():
        pass


class HTTPService:
    # delete?
    BASE_URL = BASE_URL

    def __init__(self):
        self.season_end_year = 2024

    def _get(self, url: str) -> BeautifulSoup:
        response = requests.get(url=url, allow_redirects=False)
        response.raise_for_status()

        # some content may be commented out
        clean_html = re.sub(r'<!--|-->', '', response.text, flags=re.DOTALL)
        return BeautifulSoup(clean_html, 'html.parser')

    def team_overview(self, team_name: str):
        # return TeamOverview.from_soup(http=self, soup)
        team_code = TEAM_TO_TEAM_ABBREVIATION[Team(team_name)]
        url = f"{self.BASE_URL}/teams/{team_code}/{self.season_end_year}.html"

        page = self._get(url)
        return TeamOverview.from_soup(page)
        # summary_soup = page.find('div', attrs={'data-template': 'Partials/Teams/Summary'})
        # for script in summary_soup(["script"]):
        #     script.extract()  # Remove script tags and their contents

        # # team links
        # link_dict = {}
        # links = page.find('div', attrs={'id': 'inner_nav'})
        # # need to find link elements
        # for elem in links:
        #     # Get the href attribute (the URL)
        #     href = elem.find('href')

        #     # Get the visible text associated with the link
        #     # Using .get_text() to get the visible text and stripping to remove leading/trailing whitespaces
        #     text = elem.get_text(strip=True)
        #     print(f"text={text}")

        #     # Add to dictionary if not already present (to deduplicate)
        #     if href not in link_dict:
        #         link_dict[href] = text

        # summary = "".join(summary_soup.find_all(text=True))
        # summary = re.sub(r'\n+', '\n', summary)

        # all_tables = [BBallTable.from_soup(t) for t in page.find_all('table')]

        # return TeamOverview(
        #     tables={t.caption: t for t in all_tables if t.id is not None},
        #     summary=summary
        # )

