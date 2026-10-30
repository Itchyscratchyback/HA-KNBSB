from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    websocket_api.async_register_command(hass, ws_get_history)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "knbsb/history",
        vol.Optional("pool_ids"): [int],
    }
)
@callback
def ws_get_history(hass, connection, msg) -> None:
    """Return stored teams and pool matches for the dashboard card."""

    manager = hass.data.get(DOMAIN, {}).get("history")

    if manager is None:
        connection.send_result(
            msg["id"], {"teams": {}, "pools": {}}
        )
        return

    data = manager.store.as_dict()
    pools = data["pools"]
    wanted = msg.get("pool_ids")

    if wanted is not None:
        keys = {str(pool_id) for pool_id in wanted}
        pools = {k: v for k, v in pools.items() if k in keys}

    connection.send_result(
        msg["id"],
        {"teams": data["teams"], "pools": pools},
    )
