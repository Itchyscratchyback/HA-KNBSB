from dataclasses import dataclass


@dataclass
class Match:

    match_id: int
    date: str
    time: str
    opponent: str
    location: str
    competition: str
    home_away: str

    address: dict
    latitude: float
    longitude: float

    team_name: str
    team_logo: str

    home_team_logo: str
    home_logo: str
    home_club_name: str
    home_team_name: str


    away_team_logo: str
    away_logo: str
    away_club_name: str
    away_team_name: str


    team_club_name: str

    opponent_club_name: str
    opponent_name: str
    opponent_logo: str

    # Later checken of de logo's van de teams hetzelfde zijn als de logo's van de KNBSB, zo ja dan kan je die gebruiken in plaats van de logo's van de KNBSB.
    # En zien of de logo namen niet dubbel en door elkaar worden gebruikt
