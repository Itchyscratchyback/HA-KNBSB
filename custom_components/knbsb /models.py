from dataclasses import dataclass


@dataclass
class Match:
    date: str
    time: str
    opponent: str
    location: str
    competition: str
    home_away: str
    home_logo: str
    away_logo: str
    address: dict
    latitude: float
    longitude: float
    team_name: str
    team_logo: str
    opponent_name: str
    opponent_logo: str
    home_team_name: str
    home_team_logo: str
    away_team_name: str
    away_team_logo: str
    match_id: int
