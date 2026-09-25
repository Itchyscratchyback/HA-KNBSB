import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_AWAY_ARRIVAL_MINUTES,
    CONF_HOME_ARRIVAL_MINUTES,
    CONF_ORS_API_KEY,
    CONF_TEAM_URL,
    DOMAIN,
)


class KNBSBConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):

        if user_input is not None:

            await self.async_set_unique_id(
                user_input[
                    CONF_TEAM_URL
                ]
            )

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="KNBSB",
                data=user_input,
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