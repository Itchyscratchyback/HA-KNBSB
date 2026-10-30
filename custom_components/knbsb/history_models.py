from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchRecord:
    match_key: str
    status: str

    notes: List[str] = field(
        default_factory=list
    )


@dataclass
class TeamHistory:
    team_key: str

    club_name: str

    team_code: str

    current_team_guid: str

    known_team_guids: List[str] = field(
        default_factory=list
    )

    matches: List[MatchRecord] = field(
        default_factory=list
    )