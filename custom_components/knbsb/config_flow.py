import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_AWAY_ARRIVAL_MINUTES,
    CONF_HOME_ARRIVAL_MINUTES,
    CONF_ORS_API_KEY,
    CONF_TEAM_SLOT,
    CONF_TEAM_URL,
    DOMAIN,
)


class KNBSBConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    def _get_next_team_slot(self) -> int:
        """Return the first available KNBSB team slot."""

        used_slots = {
            entry.data.get(CONF_TEAM_SLOT)
            for entry in self.hass.config_entries.async_entries(
                DOMAIN
            )
            if entry.data.get(CONF_TEAM_SLOT) is not None
        }

        team_slot = 1

        while team_slot in used_slots:
            team_slot += 1

        return team_slot

    async def async_step_user(
        self,
        user_input=None,
    ):
        """Handle the initial KNBSB configuration step."""

        if user_input is not None:

            await self.async_set_unique_id(
                user_input[
                    CONF_TEAM_URL
                ]
            )

            self._abort_if_unique_id_configured()

            team_slot = (
                self._get_next_team_slot()
            )

            entry_data = {
                **user_input,
                CONF_TEAM_SLOT:
                    team_slot,
            }

            return self.async_create_entry(
                title="KNBSB",
                data=entry_data,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_TEAM_URL
                    ): str,

                    vol.Required(
                        CONF_ORS_API_KEY
                    ): str,

                    vol.Required(
                        CONF_AWAY_ARRIVAL_MINUTES,
                        default=30,
                    ): int,

                    vol.Required(
                        CONF_HOME_ARRIVAL_MINUTES,
                        default=90,
                    ): int,
                }
            ),
        )