from enum import Enum, unique

DEFAULT_METRICS_DOMAIN = "bot.snssdk.com"
DEFAULT_METRICS_PREFIX = "byteplus.rec.sdk"
DEFAULT_HTTP_SCHEMA = "https"
COUNTER_URL_FORMAT = "{}://{}/api/counter"
OTHER_URL_FORMAT = "{}://{}/api/put"
DEFAULT_FLUSH_INTERVAL_MS: int = 15 * 1000
DELIMITER = "+"
RESERVOIR_SIZE: int = 65536
DEFAULT_HTTP_TIMEOUT_MS: int = 800
MAX_TRY_TIMES: int = 2
SUCCESS_HTTP_CODE: int = 200


@unique
class MetricsType(Enum):
    metrics_type_counter = 0
    metrics_type_timer = 1
    metrics_type_store = 2
