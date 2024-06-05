""" MediaTracker JSON to HASS sensor attributes """
import asyncio
from datetime import datetime, timedelta
import json
import logging

import aiohttp
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_NAME, CONF_SSL, CONF_HOST, CONF_PORT, CONF_TOKEN, CONF_DAYS, CONF_JSON_ONLY

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    conf = hass.data[DOMAIN]
    async_add_entities([Media_TrackerSensor(conf)])

class Media_TrackerSensor(Entity):
    """Representation of a custom sensor."""

    def __init__(self, config: dict):
        """Initialize the sensor."""
        self._ssl = 's' if config.get(CONF_SSL) else ''
        self._name = config.get(CONF_NAME)
        self._host = config.get(CONF_HOST)
        self._port = config.get(CONF_PORT)
        self._token = config.get(CONF_TOKEN)
        self._days = config.get(CONF_DAYS)
        self._json_only = config.get(CONF_JSON_ONLY)
        self._baseurl = f"http{self._ssl}://{self._host}:{self._port}/api"
        self._state = None
        self._data = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {'data': self._data}

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            calendar_data = await self._get_calendar_data()
            if calendar_data:
                processed_data = await self._process_calendar_data(calendar_data)
                self._data = json.dumps(processed_data, indent=4)
                self._state = str(len(processed_data)) + ' upcoming.'
        except Exception as e:
            _LOGGER.error(f"Error updating sensor: {e}")
            self._state = 'Update failed'
            self._data = None

    async def _get_calendar_data(self) -> list:
        today = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=self._days)).strftime("%Y-%m-%d")
        calendar_url = f"{self._baseurl}/calendar?start={today}&end={end_date}&token={self._token}"
        try:
            return await self._fetch_json(calendar_url)
        except Exception as e:
            _LOGGER.error(f"Fetch calendar error: {e}")
            return []

    async def _get_series_details(self, series_id: int) -> dict:
        details_url = f"{self._baseurl}/details/{series_id}?token={self._token}"
        try:
            return await self._fetch_json(details_url)
        except Exception as e:
            _LOGGER.error(f"Fetch details error: {e}")
            return {}

    @staticmethod
    async def _fetch_json(url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    @staticmethod
    def _initialize_default() -> dict:
        return {
            'title_default': '$title',
            'line1_default': '$episode',
            'line2_default': '$day - $release',
            'line3_default': '$number',
            'line4_default': '$empty',
            'icon': 'mdi:multimedia'
        }

    async def _process_calendar_data(self, calendar_data: list) -> list:
        if self._json_only:
            result_list = []
        else:
            result_list = [self._initialize_default()]

        tasks = [self._process_item(item) for item in calendar_data]
        processed_items = await asyncio.gather(*tasks)
        result_list.extend(processed_items)
        return result_list

    async def _process_item(self, item: dict) -> dict:
        detailed_json = await self._get_series_details(item['mediaItem']['id'])
        season_number = str(item['episode']['seasonNumber']).zfill(2)
        episode_number = str(item['episode']['episodeNumber']).zfill(2)

        add_item = {
            'series_id': item['mediaItem']['id'],
            'airdate': item['releaseDate'],
            'title': item['mediaItem']['title'],
            'release': item['episode']['releaseDate'],
            'episode': item['episode']['title'],
            'number': f"S{season_number}E{episode_number}",
            'season_num': season_number,
            'episode_num': episode_number,
            'genres': detailed_json['genres'],
            'rating': detailed_json['tmdbRating'],
            'runtime': detailed_json['runtime'],
            'poster': detailed_json.get('externalPosterUrl', '').replace('original', 'w342>
            'fanart': detailed_json.get('externalBackdropUrl', '').replace('original','w30>
            'flag': item['episode']['seen'],
        }
        return add_item
