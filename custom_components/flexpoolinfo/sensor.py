#!/usr/bin/env python3

import requests
import voluptuous as vol
from datetime import datetime, date, timedelta
import urllib.error

from .const import (
    _LOGGER,
    CONF_CURRENCY_NAME,
    CONF_TOKEN,
    CONF_ID,
    CONF_MINER_ADDRESS,
    CONF_UPDATE_FREQUENCY,
    CONF_NAME_OVERRIDE,
    SENSOR_PREFIX,
    FLEXPOOL_API_ENDPOINT,
    COINGECKO_ETH_API_ENDPOINT,
    COINGECKO_XCH_API_ENDPOINT,
    COINGECKO_ZIL_API_ENDPOINT,
    ATTR_WORKERS_ONLINE,
    ATTR_WORKERS_OFFLINE,
    ATTR_CURRENT_HASHRATE,
    ATTR_AVERAGE_HASHRATE,
    ATTR_REPORTED_HASHRATE,
    ATTR_VALID_SHARES,
    ATTR_STALE_SHARES,
    ATTR_INVALID_SHARES,
    ATTR_UNPAID_BALANCE,
    ATTR_UNPAID_LOCAL_BALANCE,
    ATTR_LAST_UPDATE,
    ATTR_SINGLE_COIN_LOCAL_CURRENCY,
    ATTR_LAST_PAYOUT_VALUE,
    ATTR_LAST_PAYOUT_FEE,
    ATTR_LAST_PAYOUT_TIMESTAMP,
    ATTR_LAST_PAYOUT_HASH
)

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MINER_ADDRESS): cv.string,
        vol.Required(CONF_UPDATE_FREQUENCY, default=1): cv.string,
        vol.Required(CONF_CURRENCY_NAME, default="usd"): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
        vol.Optional(CONF_ID, default=""): cv.string,
        vol.Optional(CONF_NAME_OVERRIDE, default=""): cv.string
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup FlexpoolInfo sensor")

    id_name = config.get(CONF_ID)
    miner_address = config.get(CONF_MINER_ADDRESS).strip()
    local_currency = config.get(CONF_CURRENCY_NAME).strip().lower()
    update_frequency = timedelta(minutes=(int(config.get(CONF_UPDATE_FREQUENCY))))
    name_override = config.get(CONF_NAME_OVERRIDE).strip()
    token = config.get(CONF_TOKEN).strip().lower()
    currency_name = config.get(CONF_CURRENCY_NAME).strip().lower()

    entities = []

    try:
        entities.append(
            FlexpoolInfoSensor(
                miner_address, currency_name, token, local_currency, update_frequency, id_name, name_override
            )
        )
    except urllib.error.HTTPError as error:
        _LOGGER.error(error.reason)
        return False

    add_entities(entities)


class FlexpoolInfoSensor(Entity):
    def __init__(
            self, miner_address, currency_name, token, local_currency, update_frequency, id_name, name_override
    ):
        self.data = None
        self.miner_address = miner_address
        self.local_currency = local_currency
        self.update = Throttle(update_frequency)(self._update)
        self.token = token
        if name_override:
            self._name = SENSOR_PREFIX + name_override
        else:
            self._name = SENSOR_PREFIX + (id_name + " " if len(id_name) > 0 else "") + miner_address
        self._icon = "mdi:apple-icloud"
        self._state = None
        self._workers_online = None
        self._workers_offline = None
        self._current_hashrate = None
        self._average_hashrate = None
        self._reported_hashrate = None
        self._valid_shares = None
        self._stale_shares = None
        self._invalid_shares = None
        self._last_update = None
        self._unpaid_balance = None
        self._unpaid_local_balance = None
        self._unit_of_measurement = "\u200b"
        self._single_coin_in_local_currency = None
        self._last_payout_value = None
        self._last_payout_fee = None
        self._last_payout_timestamp = None
        self._last_payout_hash = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def extra_state_attributes(self):
        return {ATTR_WORKERS_ONLINE: self._workers_online, ATTR_WORKERS_OFFLINE: self._workers_offline,
                ATTR_CURRENT_HASHRATE: self._current_hashrate, ATTR_AVERAGE_HASHRATE: self._average_hashrate,
                ATTR_REPORTED_HASHRATE: self._reported_hashrate, ATTR_VALID_SHARES: self._valid_shares,
                ATTR_STALE_SHARES: self._stale_shares, ATTR_INVALID_SHARES: self._invalid_shares,
                ATTR_LAST_UPDATE: self._last_update, ATTR_UNPAID_BALANCE: self._unpaid_balance,
                ATTR_UNPAID_LOCAL_BALANCE: self._unpaid_local_balance,
                ATTR_SINGLE_COIN_LOCAL_CURRENCY: self._single_coin_in_local_currency,
                ATTR_LAST_PAYOUT_VALUE: self._last_payout_value,
                ATTR_LAST_PAYOUT_FEE: self._last_payout_fee,
                ATTR_LAST_PAYOUT_TIMESTAMP: self._last_payout_timestamp,
                ATTR_LAST_PAYOUT_HASH: self._last_payout_hash
                }

    def _update(self):
        statsurl = (
                FLEXPOOL_API_ENDPOINT
                + "stats?coin="
                + self.token
                + "&address="
                + self.miner_address
        )

        balanceurl = (
                FLEXPOOL_API_ENDPOINT
                + "balance?coin="
                + self.token
                + "&address="
                + self.miner_address
        )

        workerurl = (
                FLEXPOOL_API_ENDPOINT
                + "workerCount?coin="
                + self.token
                + "&address="
                + self.miner_address
        )

        paymenturl = (
                FLEXPOOL_API_ENDPOINT
                + "paymentsStats?coin="
                + self.token
                + "&address="
                + self.miner_address
        )

        coingeckoxchurl = (
                COINGECKO_XCH_API_ENDPOINT
                + self.local_currency
        )

        coingeckoethurl = (
                COINGECKO_ETH_API_ENDPOINT
                + self.local_currency
        )

        coingeckozilurl = (
                COINGECKO_ZIL_API_ENDPOINT
                + self.local_currency
        )

        # sending get request to Flexpool dashboard endpoint
        r = requests.get(url=statsurl)
        # extracting response json
        self.data = r.json()
        statsurldata = self.data

        # sending get request to Flexpool balance endpoint
        r2 = requests.get(url=balanceurl)
        # extracting response json
        self.data2 = r2.json()
        balanceurldata = self.data2

        # sending get request to Flexpool currentStats endpoint
        r3 = requests.get(url=workerurl)
        # extracting response json
        self.data3 = r3.json()
        workerurldata = self.data3

        # sending get request to Flexpool paymentsStats endpoint
        r4 = requests.get(url=paymenturl)
        # extracting response json
        self.data4 = r4.json()
        paymenturldata = self.data4

        # sending get request to Congecko API endpoint
        if self.token.lower() == "xch":
            r5 = requests.get(url=coingeckoxchurl)
            self.data5 = r5.json()
            coingeckodata = self.data5
        if self.token.lower() == "eth":
            r5 = requests.get(url=coingeckoethurl)
            self.data5 = r5.json()
            coingeckodata = self.data5
        if self.token.lower() == "zil":
            r5 = requests.get(url=coingeckozilurl)
            self.data5 = r5.json()
            coingeckodata = self.data5

        try:
            if statsurldata:
                # Set the values of the sensor
                self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
                self._state = r3.json()['result']['workersOnline']
                # set the attributes of the sensor
                self._current_hashrate = r.json()['result']['currentEffectiveHashrate']
                self._average_hashrate = r.json()['result']['averageEffectiveHashrate']
                self._reported_hashrate = r.json()['result']['reportedHashrate']
                self._valid_shares = r.json()['result']['validShares']
                self._stale_shares = r.json()['result']['staleShares']
                self._invalid_shares = r.json()['result']['invalidShares']
                self._unpaid_balance = r2.json()['result']['balance']
                self._workers_online = r3.json()['result']['workersOnline']
                self._workers_offline = r3.json()['result']['workersOffline']
                if len(r4.json()['result']['lastPayment']):
                    self._last_payout_value = r4.json()['result']['lastPayment']['value']
                    self._last_payout_fee = r4.json()['result']['lastPayment']['fee']
                    self._last_payout_timestamp = datetime.fromtimestamp(int(r4.json()['result']['lastPayment']['timestamp'])).strftime('%d-%m-%Y %H:%M')
                    self._last_payout_hash = r4.json()['result']['lastPayment']['hash']
                if self.token.lower() == "xch":
                    if len(r5.json()['chia']):
                        self._single_coin_in_local_currency = r5.json()['chia'][self.local_currency]
                        calculate_unpaid = self._unpaid_balance / 1000000000000000000 * self._single_coin_in_local_currency
                        self._unpaid_local_balance = round(calculate_unpaid, 2)
                if self.token.lower() == "eth":
                    if len(r5.json()['ethereum']):
                        self._single_coin_in_local_currency = r5.json()['ethereum'][self.local_currency]
                        calculate_unpaid = self._unpaid_balance / 1000000000000000000 * self._single_coin_in_local_currency
                        self._unpaid_local_balance = round(calculate_unpaid, 2)
                if self.token.lower() == "zil":
                    if len(r5.json()['zilliqa']):
                        self._single_coin_in_local_currency = r5.json()['zilliqa'][self.local_currency]
                        calculate_unpaid = self._unpaid_balance / 1000000000000000000 * self._single_coin_in_local_currency
                        self._unpaid_local_balance = round(calculate_unpaid, 2)
            else:
                raise ValueError()

        except ValueError:
            self._state = None
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
