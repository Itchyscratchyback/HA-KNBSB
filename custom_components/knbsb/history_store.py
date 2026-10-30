from __future__ import annotations

import json
import logging

from pathlib import Path

from homeassistant.core import HomeAssistant

from .history_models import TeamHistory


_LOGGER = logging.getLogger(__name__)

#CODE STARTS HERE

class HistoryStore:

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:

        self._hass = hass

        self._base_path = (
            Path(hass.config.path())
            / ".storage"
            / "knbsb"
            / "history"
        )

        self._base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Team Key Generatie

    @staticmethod
    def build_team_key(
        club_name: str,
        team_code: str,
    ) -> str:

        safe_club = (
            club_name
            .strip()
            .replace(" ", "_")
        )

        safe_team = (
            team_code
            .strip()
            .replace(" ", "_")
        )

        return (
            f"{safe_club}_{safe_team}"
        )

    # Bestandslocatie bepalen

        def get_team_file(
        self,
        team_key: str,
    ) -> Path:

        return (
            self._base_path
            / f"{team_key}.json"
        )

    # Teamhistory aanmaken

        def create_team_history(
        self,
        club_name: str,
        team_code: str,
        team_guid: str,
    ) -> TeamHistory:

        team_key = self.build_team_key(
            club_name,
            team_code,
        )

        return TeamHistory(
            team_key=team_key,

            club_name=club_name,

            team_code=team_code,

            current_team_guid=team_guid,

            known_team_guids=[
                team_guid
            ],
        )
# Opslaan
    async def save_team(
        self,
        team: TeamHistory,
    ) -> None:

        path = self.get_team_file(
            team.team_key
        )

        data = {
            "schema": 1,

            "team_key":
                team.team_key,

            "club_name":
                team.club_name,

            "team_code":
                team.team_code,

            "current_team_guid":
                team.current_team_guid,

            "known_team_guids":
                team.known_team_guids,

            "matches": [
                {
                    "match_key":
                        match.match_key,

                    "status":
                        match.status,

                    "notes":
                        match.notes,
                }
                for match
                in team.matches
            ],
        }

        path.write_text(
            json.dumps(
                data,
                indent=2,
            ),
            encoding="utf-8",
        )

# Laden

    async def load_team(
        self,
        team_key: str,
    ) -> TeamHistory | None:

        path = self.get_team_file(
            team_key
        )

        if not path.exists():
            return None

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return TeamHistory(
            team_key=
                data["team_key"],

            club_name=
                data["club_name"],

            team_code=
                data["team_code"],

            current_team_guid=
                data["current_team_guid"],

            known_team_guids=
                data.get(
                    "known_team_guids",
                    []
                ),
        )

# GUID migratie

    async def get_or_create_team(
        self,
        club_name: str,
        team_code: str,
        team_guid: str,
    ) -> TeamHistory:

        team_key = (
            self.build_team_key(
                club_name,
                team_code,
            )
        )

        team = await self.load_team(
            team_key
        )

        if team is None:

            team = (
                self.create_team_history(
                    club_name=
                        club_name,

                    team_code=
                        team_code,

                    team_guid=
                        team_guid,
                )
            )

            await self.save_team(
                team
            )

            return team


        if (
            team_guid
            not in
            team.known_team_guids
        ):

            _LOGGER.info(
                (
                    "KNBSB team GUID gewijzigd "
                    "%s -> %s"
                ),
                team.team_key,
                team_guid,
            )

            team.known_team_guids.append(
                team_guid
            )


        team.current_team_guid = (
            team_guid
        )

        await self.save_team(
            team
        )

        return team