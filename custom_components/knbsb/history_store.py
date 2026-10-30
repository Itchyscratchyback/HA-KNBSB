from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .history_models import build_team_key

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "knbsb.history"


class HistoryStore:
    """Central history file (.storage/knbsb.history).

    Layout:
        teams: team_key -> club/team code/GUIDs/pool ids
        pools: pool_id  -> competition name + matches keyed by match_id
        sync:  team_guid -> last sync (ISO, UTC)
    """

    def __init__(self, hass: HomeAssistant) -> None:
        self._store: Store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: dict[str, Any] = {"teams": {}, "pools": {}, "sync": {}}
        self._loaded = False

    async def async_load(self) -> None:
        if self._loaded:
            return

        stored = await self._store.async_load()

        if stored:
            self._data = {
                "teams": stored.get("teams", {}),
                "pools": stored.get("pools", {}),
                "sync": stored.get("sync", {}),
            }

        self._loaded = True

    async def async_save(self) -> None:
        await self._store.async_save(self._data)

    def register_team(
        self,
        club_name: str,
        team_code: str,
        team_guid: str,
        pool_id: int,
    ) -> str:
        """Create the team or migrate a changed GUID; keeps history."""

        team_key = build_team_key(club_name, team_code)
        team = self._data["teams"].setdefault(
            team_key,
            {
                "club_name": club_name,
                "team_code": team_code,
                "current_team_guid": team_guid,
                "known_team_guids": [],
                "pool_ids": [],
            },
        )

        if team_guid not in team["known_team_guids"]:
            if team["known_team_guids"]:
                _LOGGER.info(
                    "KNBSB team GUID changed %s -> %s",
                    team_key,
                    team_guid,
                )
            team["known_team_guids"].append(team_guid)

        team["current_team_guid"] = team_guid

        if pool_id not in team["pool_ids"]:
            team["pool_ids"].append(pool_id)

        return team_key

    def update_pool(
        self,
        pool_id: int,
        matches: list[dict[str, Any]],
        last_sync: str,
    ) -> None:
        pool = self._data["pools"].setdefault(
            str(pool_id),
            {"pool_id": pool_id, "matches": {}},
        )

        for match in matches:
            pool["matches"][str(match["match_id"])] = match

        if matches:
            pool["competition_name"] = matches[0].get("competition_name")

        pool["last_sync"] = last_sync

    def update_standings(
        self,
        pool_id: int,
        standings: list[dict[str, Any]],
    ) -> None:
        pool = self._data["pools"].setdefault(
            str(pool_id),
            {"pool_id": pool_id, "matches": {}},
        )

        old_rows = {
            row["team_guid"]: row
            for row in pool.get("standings", [])
        }

        new_rows = [
            {
                "position": row.get("position"),
                "team_guid": row.get("teamGuid"),
                "club_name": row.get("clubName"),
                "team_code": row.get("teamName"),
                "logo": row.get("clubLogoUrl"),
                "pool_name": row.get("poolName"),
                "games_played": row.get("gamesPlayed"),
                "won": row.get("wonCount"),
                "draw": row.get("drawCount"),
                "lost": row.get("lostCount"),
                "points": row.get("points"),
                "score_diff": row.get("scoreDifference"),
                "score_for": row.get("scorePositive"),
                "score_against": row.get("scoreNegative"),
                "loss_of_rights": row.get("isLossOfRights"),
            }
            for row in sorted(
                standings, key=lambda r: r.get("position") or 999
            )
        ]

        for row in new_rows:
            old = old_rows.get(row["team_guid"])
            trend = dict(old.get("trend", {})) if old else {}

            if old:
                diff_old, diff_new = old.get("score_diff"), row["score_diff"]
                if None not in (diff_old, diff_new) and diff_new != diff_old:
                    trend["score_diff"] = (
                        "up" if diff_new > diff_old else "down"
                    )

                # A rise in wins clears the loss trend and vice versa.
                if (row["won"] or 0) > (old.get("won") or 0):
                    trend["won"] = "up"
                    trend.pop("lost", None)
                if (row["lost"] or 0) > (old.get("lost") or 0):
                    trend["lost"] = "up"
                    trend.pop("won", None)

            row["trend"] = trend

        pool["standings"] = new_rows

    def get_pool(self, pool_id: int) -> dict[str, Any] | None:
        return self._data["pools"].get(str(pool_id))

    def get_team(self, team_key: str) -> dict[str, Any] | None:
        return self._data["teams"].get(team_key)

    def get_last_sync(self, team_guid: str) -> str | None:
        return self._data["sync"].get(team_guid)

    def set_last_sync(self, team_guid: str, value: str) -> None:
        self._data["sync"][team_guid] = value

    def as_dict(self) -> dict[str, Any]:
        return self._data
