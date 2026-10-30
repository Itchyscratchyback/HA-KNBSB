from __future__ import annotations

from homeassistant.core import HomeAssistant

from .history_store import (
    HistoryStore,
)

# CODE STARTS HERE


class HistoryManager:

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:

        self._store = (
            HistoryStore(
                hass
            )
        )


    async def register_team(
        self,
        club_name: str,
        team_code: str,
        team_guid: str,
    ):

        return await (
            self._store
            .get_or_create_team(
                club_name=
                    club_name,

                team_code=
                    team_code,

                team_guid=
                    team_guid,
            )
        )

