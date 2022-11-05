import logging

CONF_ID = "id"
CONF_CURRENCY_NAME = "currency_name"
CONF_MINER_ADDRESS = "miner_address"
CONF_UPDATE_FREQUENCY = "update_frequency"
CONF_NAME_OVERRIDE = "name_override"
CONF_TOKEN = "token"

SENSOR_PREFIX = "FlexpoolInfo "

ATTR_WORKERS_ONLINE = "workers_online"
ATTR_WORKERS_OFFLINE = "workers_offline"
ATTR_CURRENT_HASHRATE = "current_hashrate"
ATTR_AVERAGE_HASHRATE = "average_hashrate"
ATTR_REPORTED_HASHRATE = "reported_hashrate"
ATTR_VALID_SHARES = "valid_shares"
ATTR_STALE_SHARES = "stale_shares"
ATTR_INVALID_SHARES = "invalid_shares"
ATTR_UNPAID_BALANCE = "unpaid_balance"
ATTR_UNPAID_LOCAL_BALANCE = "unpaid_local_balance"
ATTR_LAST_UPDATE = "last_update"
ATTR_SINGLE_COIN_LOCAL_CURRENCY = "single_coin_in_local_currency"
ATTR_LAST_PAYOUT_VALUE = "last_payout_value"
ATTR_LAST_PAYOUT_FEE = "last_payout_fee"
ATTR_LAST_PAYOUT_TIMESTAMP = "last_payout_timestamp"
ATTR_LAST_PAYOUT_HASH = "last_payout_hash"

FLEXPOOL_API_ENDPOINT = "https://api.flexpool.io/v2/miner/"
COINGECKO_ETC_API_ENDPOINT = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum-classic&vs_currencies="
COINGECKO_ETH_API_ENDPOINT = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies="
COINGECKO_XCH_API_ENDPOINT = "https://api.coingecko.com/api/v3/simple/price?ids=chia&vs_currencies="
COINGECKO_ZIL_API_ENDPOINT = "https://api.coingecko.com/api/v3/simple/price?ids=zilliqa&vs_currencies="

_LOGGER = logging.getLogger(__name__)
