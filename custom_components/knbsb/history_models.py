from __future__ import annotations

from typing import Any


def build_team_key(club_name: str, team_code: str) -> str:
    """Stable storage identity, e.g. Houten_Dragons_MSL-1."""

    return (
        f"{club_name.strip().replace(' ', '_')}"
        f"_{team_code.strip().replace(' ', '_')}"
    )


def normalize_match(item: dict[str, Any]) -> dict[str, Any]:
    """Reduce a FOYS match item to the fields we persist.

    The status is stored exactly as FOYS returns it.
    """

    address = item.get("address") or {}
    competition = item.get("competition") or {}
    home_org = item.get("homeOrganisation") or {}
    away_org = item.get("awayOrganisation") or {}

    return {
        "match_id": item["id"],
        "date": (item.get("date") or "").split("T")[0],
        "time": (item.get("startTime") or "")[:5],
        "status": item.get("status"),
        "home_score": item.get("homeScore"),
        "away_score": item.get("awayScore"),
        "home_team_guid": item.get("homeTeamGuid"),
        "away_team_guid": item.get("awayTeamGuid"),
        "home_team_code": item.get("homeTeamName"),
        "away_team_code": item.get("awayTeamName"),
        "home_club_name": home_org.get("name"),
        "away_club_name": away_org.get("name"),
        "home_logo": item.get("homeLogoUrl"),
        "away_logo": item.get("awayLogoUrl"),
        "competition_id": competition.get("id"),
        "competition_name": competition.get("name"),
        "location": item.get("accommodationName"),
        "city": address.get("city"),
        "is_friendly": item.get("isFriendly"),
    }
