from __future__ import annotations

import json
from datetime import UTC
from datetime import datetime
from pathlib import Path

from homeassistant.core import HomeAssistant

from .history_store import HistoryStore


class HistoryRegistry:

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:

        self._hass = hass

        self._store = HistoryStore(
            hass
        )

        self._metadata_file = (
            Path(hass.config.path())
            / ".storage"
            / "knbsb"
            / "metadata.json"
        )

        self._metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


    async def load_metadata(
        self,
    ) -> dict:

        if not self._metadata_file.exists():

            return {
                "schema": 1,
                "teams": [],
            }

        return json.loads(
            self._metadata_file.read_text(
                encoding="utf-8"
            )
        )


    async def save_metadata(
        self,
        metadata: dict,
    ) -> None:

        self._metadata_file.write_text(
            json.dumps(
                metadata,
                indent=2,
            ),
            encoding="utf-8",
        )


    async def get_known_teams(
        self,
    ) -> listmetadata = await self.load_metadata()

        return metadata.get(
            "teams",
            [],
        )


    async def get_active_teams(
        self,
    ) -> listteams = await self.get_known_teams()

        return [
            team
            for team in teams
            if team.get(
                "active",
                False
            )
        ]


    async def register_team(
        self,
        club_name: str,
        team_code: str,
        team_guid: str,
    ) -> dict:

        team = await (
            self._store.get_or_create_team(
                club_name=club_name,
                team_code=team_code,
                team_guid=team_guid,
            )
        )

        metadata = await self.load_metadata()

        teams = metadata.setdefault(
            "teams",
            [],
        )

        team_entry = next(
            (
                item
                for item in teams
                if item["team_key"]
                == team.team_key
            ),
            None,
        )

        now = (
            datetime.now(
                UTC
            )
            .isoformat()
        )

        if team_entry is None:

            team_entry = {
                "team_key":
                    team.team_key,

                "club_name":
                    club_name,

                "team_code":
                    team_code,

                "active":
                    True,

                "last_seen":
                    now,
            }

            teams.append(
                team_entry
            )

        else:

            team_entry["active"] = True

            team_entry["last_seen"] = now

        await self.save_metadata(
            metadata
        )

        return team_entry


    async def mark_missing_teams(
        self,
        active_team_keys: set[str],
    ) -> None:

        metadata = await self.load_metadata()

        changed = False

        teams = metadata.get(
            "teams",
            [],
        )

        for team in teams:

            if (
                team["team_key"]
                not in active_team_keys
            ):

                if (
                    team.get(
                        "active",
                        True
                    )
                ):

                    team["active"] = False

                    changed = True

        if changed:

            await self.save_metadata(
                metadata
            )


    async def sync_active_teams(
        self,
        discovered_teams: list[dict],
    ) -> None:

        active_team_keys: set[str] = set()

        for team in discovered_teams:

            club_name = team[
                "club_name"
            ]

            team_code = team[
                "team_code"
            ]

            team_guid = team[
                "team_guid"
            ]

            registry_entry = (
                await self.register_team(
                    club_name=
                        club_name,

                    team_code=
                        team_code,

                    team_guid=
                        team_guid,
                )
            )

            active_team_keys.add(
                registry_entry[
                    "team_key"
                ]
            )

        await self.mark_missing_teams(
            active_team_keys
        )


    async def get_team(
        self,
        team_key: str,
    ) -> dict | None:

        metadata = await self.load_metadata()

        return next(
            (
                team
                for team in metadata.get(
                    "teams",
                    []
                )
                if team["team_key"]
                == team_key
            ),
            None,
        )