from __future__ import annotations

from datetime import datetime, timezone

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    websocket_api.async_register_command(hass, ws_get_history)
    websocket_api.async_register_command(hass, ws_set_note)
    websocket_api.async_register_command(hass, ws_set_hits)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "knbsb/hits_set",
        vol.Required("match_id"): vol.Coerce(str),
        vol.Required("hits"): vol.All(
            [
                {
                    vol.Required("x"): vol.All(
                        vol.Coerce(float), vol.Range(min=0, max=1)
                    ),
                    vol.Required("y"): vol.All(
                        vol.Coerce(float), vol.Range(min=0, max=1)
                    ),
                    vol.Required("t"): vol.In(["g", "f", "h"]),
                }
            ],
            vol.Length(max=500),
        ),
    }
)
@websocket_api.async_response
async def ws_set_hits(hass, connection, msg) -> None:
    """Replace the heatmap points of a match."""

    manager = hass.data.get(DOMAIN, {}).get("history")

    if manager is None:
        connection.send_error(
            msg["id"], "not_ready", "History not available"
        )
        return

    manager.store.set_hits(msg["match_id"], msg["hits"])
    await manager.store.async_save()

    connection.send_result(
        msg["id"],
        manager.store.as_dict()["notes"].get(msg["match_id"], {}),
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "knbsb/note_set",
        vol.Required("match_id"): vol.Coerce(str),
        vol.Required("text"): vol.All(str, vol.Length(max=5000)),
    }
)
@websocket_api.async_response
async def ws_set_note(hass, connection, msg) -> None:
    """Save (or clear with empty text) the note of a match."""

    manager = hass.data.get(DOMAIN, {}).get("history")

    if manager is None:
        connection.send_error(
            msg["id"], "not_ready", "History not available"
        )
        return

    manager.store.set_note(
        msg["match_id"],
        msg["text"],
        datetime.now(timezone.utc).isoformat(),
    )
    await manager.store.async_save()

    connection.send_result(
        msg["id"],
        manager.store.as_dict()["notes"].get(msg["match_id"], {}),
    )


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
            msg["id"], {"teams": {}, "pools": {}, "notes": {}}
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
        {
            "teams": data["teams"],
            "pools": pools,
            "notes": data["notes"],
        },
    )
