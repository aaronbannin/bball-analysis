from enum import Enum


class Location(Enum):
    HOME = "HOME"
    AWAY = "AWAY"


class Outcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"


class Team(Enum):
    ATLANTA_HAWKS = "ATLANTA HAWKS"
    BOSTON_CELTICS = "BOSTON CELTICS"
    BROOKLYN_NETS = "BROOKLYN NETS"
    CHARLOTTE_HORNETS = "CHARLOTTE HORNETS"
    CHICAGO_BULLS = "CHICAGO BULLS"
    CLEVELAND_CAVALIERS = "CLEVELAND CAVALIERS"
    DALLAS_MAVERICKS = "DALLAS MAVERICKS"
    DENVER_NUGGETS = "DENVER NUGGETS"
    DETROIT_PISTONS = "DETROIT PISTONS"
    GOLDEN_STATE_WARRIORS = "GOLDEN STATE WARRIORS"
    HOUSTON_ROCKETS = "HOUSTON ROCKETS"
    INDIANA_PACERS = "INDIANA PACERS"
    LOS_ANGELES_CLIPPERS = "LOS ANGELES CLIPPERS"
    LOS_ANGELES_LAKERS = "LOS ANGELES LAKERS"
    MEMPHIS_GRIZZLIES = "MEMPHIS GRIZZLIES"
    MIAMI_HEAT = "MIAMI HEAT"
    MILWAUKEE_BUCKS = "MILWAUKEE BUCKS"
    MINNESOTA_TIMBERWOLVES = "MINNESOTA TIMBERWOLVES"
    NEW_ORLEANS_PELICANS = "NEW ORLEANS PELICANS"
    NEW_YORK_KNICKS = "NEW YORK KNICKS"
    OKLAHOMA_CITY_THUNDER = "OKLAHOMA CITY THUNDER"
    ORLANDO_MAGIC = "ORLANDO MAGIC"
    PHILADELPHIA_76ERS = "PHILADELPHIA 76ERS"
    PHOENIX_SUNS = "PHOENIX SUNS"
    PORTLAND_TRAIL_BLAZERS = "PORTLAND TRAIL BLAZERS"
    SACRAMENTO_KINGS = "SACRAMENTO KINGS"
    SAN_ANTONIO_SPURS = "SAN ANTONIO SPURS"
    TORONTO_RAPTORS = "TORONTO RAPTORS"
    UTAH_JAZZ = "UTAH JAZZ"
    WASHINGTON_WIZARDS = "WASHINGTON WIZARDS"


class OutputType(Enum):
    JSON = "JSON"
    CSV = "CSV"


class OutputWriteOption(Enum):
    WRITE = "w"
    CREATE_AND_WRITE = "w+"
    APPEND = "a"
    APPEND_AND_WRITE = "a+"


class Position(Enum):
    POINT_GUARD = "POINT GUARD"
    SHOOTING_GUARD = "SHOOTING GUARD"
    SMALL_FORWARD = "SMALL FORWARD"
    POWER_FORWARD = "POWER FORWARD"
    CENTER = "CENTER"
    FORWARD = "FORWARD"
    GUARD = "GUARD"


class PeriodType(Enum):
    QUARTER = "QUARTER"
    OVERTIME = "OVERTIME"


class League(Enum):
    NATIONAL_BASKETBALL_ASSOCIATION = "NATIONAL_BASKETBALL_ASSOCIATION"
    AMERICAN_BASKETBALL_ASSOCIATION = "AMERICAN_BASKETBALL_ASSOCIATION"
    BASKETBALL_ASSOCIATION_OF_AMERICA = "BASKETBALL_ASSOCIATION_OF_AMERICA"


class Conference(Enum):
    EASTERN = "EASTERN"
    WESTERN = "WESTERN"


class Division(Enum):
    ATLANTIC = "ATLANTIC"
    CENTRAL = "CENTRAL"
    MIDWEST = "MIDWEST"
    NORTHWEST = "NORTHWEST"
    PACIFIC = "PACIFIC"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"


DIVISIONS_TO_CONFERENCES = {
    Division.ATLANTIC: Conference.EASTERN,
    Division.CENTRAL: Conference.EASTERN,
    Division.SOUTHEAST: Conference.EASTERN,
    Division.MIDWEST: Conference.WESTERN,
    Division.PACIFIC: Conference.WESTERN,
    Division.SOUTHWEST: Conference.WESTERN,
    Division.NORTHWEST : Conference.WESTERN
}


TEAM_ABBREVIATIONS_TO_TEAM = {
    'ATL': Team.ATLANTA_HAWKS,
    'BOS': Team.BOSTON_CELTICS,
    'BRK': Team.BROOKLYN_NETS,
    'CHI': Team.CHICAGO_BULLS,
    'CHO': Team.CHARLOTTE_HORNETS,
    'CLE': Team.CLEVELAND_CAVALIERS,
    'DAL': Team.DALLAS_MAVERICKS,
    'DEN': Team.DENVER_NUGGETS,
    'DET': Team.DETROIT_PISTONS,
    'GSW': Team.GOLDEN_STATE_WARRIORS,
    'HOU': Team.HOUSTON_ROCKETS,
    'IND': Team.INDIANA_PACERS,
    'LAC': Team.LOS_ANGELES_CLIPPERS,
    'LAL': Team.LOS_ANGELES_LAKERS,
    'MEM': Team.MEMPHIS_GRIZZLIES,
    'MIA': Team.MIAMI_HEAT,
    'MIL': Team.MILWAUKEE_BUCKS,
    'MIN': Team.MINNESOTA_TIMBERWOLVES,
    'NOP': Team.NEW_ORLEANS_PELICANS,
    'NYK': Team.NEW_YORK_KNICKS,
    'OKC': Team.OKLAHOMA_CITY_THUNDER,
    'ORL': Team.ORLANDO_MAGIC,
    'PHI': Team.PHILADELPHIA_76ERS,
    'PHO': Team.PHOENIX_SUNS,
    'POR': Team.PORTLAND_TRAIL_BLAZERS,
    'SAC': Team.SACRAMENTO_KINGS,
    'SAS': Team.SAN_ANTONIO_SPURS,
    'TOR': Team.TORONTO_RAPTORS,
    'UTA': Team.UTAH_JAZZ,
    'WAS': Team.WASHINGTON_WIZARDS
}

TEAM_NAMES = [t.value for t in Team]
TEAM_TO_TEAM_ABBREVIATION = {v: k for k, v in TEAM_ABBREVIATIONS_TO_TEAM.items()}
TEAM_TO_TEAM_ABBREVIATION[Team.CHARLOTTE_HORNETS] = "CHO"

TEAM_NAME_TO_TEAM = {
    "ATLANTA HAWKS": Team.ATLANTA_HAWKS,
    "BOSTON CELTICS": Team.BOSTON_CELTICS,
    "BROOKLYN NETS": Team.BROOKLYN_NETS,
    "CHARLOTTE HORNETS": Team.CHARLOTTE_HORNETS,
    "CHICAGO BULLS": Team.CHICAGO_BULLS,
    "CLEVELAND CAVALIERS": Team.CLEVELAND_CAVALIERS,
    "DALLAS MAVERICKS": Team.DALLAS_MAVERICKS,
    "DENVER NUGGETS": Team.DENVER_NUGGETS,
    "DETROIT PISTONS": Team.DETROIT_PISTONS,
    "GOLDEN STATE WARRIORS": Team.GOLDEN_STATE_WARRIORS,
    "HOUSTON ROCKETS": Team.HOUSTON_ROCKETS,
    "INDIANA PACERS": Team.INDIANA_PACERS,
    "LOS ANGELES CLIPPERS": Team.LOS_ANGELES_CLIPPERS,
    "LOS ANGELES LAKERS": Team.LOS_ANGELES_LAKERS,
    "MEMPHIS GRIZZLIES": Team.MEMPHIS_GRIZZLIES,
    "MIAMI HEAT": Team.MIAMI_HEAT,
    "MILWAUKEE BUCKS": Team.MILWAUKEE_BUCKS,
    "MINNESOTA TIMBERWOLVES": Team.MINNESOTA_TIMBERWOLVES,
    "NEW ORLEANS PELICANS": Team.NEW_ORLEANS_PELICANS,
    "NEW YORK KNICKS": Team.NEW_YORK_KNICKS,
    "OKLAHOMA CITY THUNDER": Team.OKLAHOMA_CITY_THUNDER,
    "ORLANDO MAGIC": Team.ORLANDO_MAGIC,
    "PHILADELPHIA 76ERS": Team.PHILADELPHIA_76ERS,
    "PHOENIX SUNS": Team.PHOENIX_SUNS,
    "PORTLAND TRAIL BLAZERS": Team.PORTLAND_TRAIL_BLAZERS,
    "SACRAMENTO KINGS": Team.SACRAMENTO_KINGS,
    "SAN ANTONIO SPURS": Team.SAN_ANTONIO_SPURS,
    "TORONTO RAPTORS": Team.TORONTO_RAPTORS,
    "UTAH JAZZ": Team.UTAH_JAZZ,
    "WASHINGTON WIZARDS": Team.WASHINGTON_WIZARDS
}

POSITION_ABBREVIATIONS_TO_POSITION = {
    "PG": Position.POINT_GUARD,
    "SG": Position.SHOOTING_GUARD,
    "SF": Position.SMALL_FORWARD,
    "PF": Position.POWER_FORWARD,
    "C": Position.CENTER,
    "F": Position.FORWARD,
    "G": Position.GUARD,
}


LOCATION_ABBREVIATIONS_TO_POSITION = {
    "": Location.HOME,
    "@": Location.AWAY,
}


OUTCOME_ABBREVIATIONS_TO_OUTCOME = {
    "W": Outcome.WIN,
    "L": Outcome.LOSS,
}

LEAGUE_ABBREVIATIONS_TO_LEAGUE = {
    "NBA": League.NATIONAL_BASKETBALL_ASSOCIATION,
    "ABA": League.AMERICAN_BASKETBALL_ASSOCIATION,
    "BAA": League.BASKETBALL_ASSOCIATION_OF_AMERICA,
}

