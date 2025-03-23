"""Integrate with Dynamic DNS service."""
import asyncio
from datetime import timedelta
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.const import (
    CONF_HOST,
    CONF_DOMAIN,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_SCAN_INTERVAL
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "dyndns"

DEFAULT_INTERVAL = timedelta(minutes=15)

TIMEOUT = 30
ENDPOINT = "/nic/update"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_DOMAIN): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_INTERVAL): vol.All(
                    cv.time_period, cv.positive_timedelta
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the DynHost/DynDNS."""
    conf = config[DOMAIN]
    server = conf.get(CONF_HOST).strip()
    domain = conf.get(CONF_DOMAIN).strip()
    user = conf.get(CONF_USERNAME).strip()
    password = conf.get(CONF_PASSWORD).strip()
    interval = conf.get(CONF_SCAN_INTERVAL)

    session = async_get_clientsession(hass)

    result = await _update_dyndns(server, session, domain, user, password)

    if not result:
        return False

    async def update_domain_interval(_):
        await _update_dyndns(server, session, domain, user, password)

    async_track_time_interval(hass, update_domain_interval, interval)

    return True


async def _update_dyndns(server, session, domain, user, password):
    """Update DynHost/DynDNS."""
    try:
        url = f"https://{user}:{password}@{server}{ENDPOINT}?&hostname={domain}"
        async with async_timeout.timeout(TIMEOUT):
            resp = await session.get(url)
            body = await resp.text()

            if body.startswith("good"):
                _LOGGER.info("Updating for domain: %s", domain)
                return True

            if body.startswith("nochg"):
                _LOGGER.info("No Change for domain: %s", domain)
                return True

            _LOGGER.warning("Updating failed: %s => %s", domain, body.strip())

    except aiohttp.ClientError:
        _LOGGER.error("Can't connect to API")

    except asyncio.TimeoutError:
        _LOGGER.error("Timeout from API for domain: %s", domain)

    return False
