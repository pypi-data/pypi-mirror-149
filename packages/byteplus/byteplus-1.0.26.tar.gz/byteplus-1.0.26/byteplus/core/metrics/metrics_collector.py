import threading

from .metrics_option import *
from .constant import *
from .helper import _build_collect_key, _parse_name_and_tags, _is_timeout_exception
from .sample import *
from .metrics_pb2 import *
import requests
import time
import logging
import sys
from byteplus.core.exception import NetException, BizException

log = logging.getLogger(__name__)

initialed = False  # init func should exec once
metrics_cfg = None
metrics_collector: map = {}
metrics_locks: map = {}
timer_stat_metrics = ["max", "min", "avg", "pct75", "pct90", "pct95", "pct99", "pct999"]

"""
Parameters:
  key - metrics name
  value - metrics value
  tag_kvs - tag_key and tag_value list, 
    should be formatted as ["tag_key_1:tag_value_1","tag_key_2:tag_value_2",...]
Example:
  store("goroutine.count", 400, ["ip:127.0.0.1"])
"""


def store(name: str, value: float, tag_kvs: list):
    if not _is_enable_metrics():
        return
    collect_key = _build_collect_key(name, tag_kvs)
    _update_metric(MetricsType.metrics_type_store, collect_key, value)


"""
Parameters:
  key - metrics name
  value - metrics value
  tag_kvs - tag_key and tag_value list, 
    should be formatted as ["tag_key_1:tag_value_1","tag_key_2:tag_value_2",...]
Example:
  counter("request.qp", 1, ["method:user", "type:upload"])
"""


def counter(name: str, value: float, tag_kvs: list):
    if not _is_enable_metrics():
        return
    collect_key = _build_collect_key(name, tag_kvs)
    _update_metric(MetricsType.metrics_type_counter, collect_key, value)


"""
Parameters:
  key - metrics name
  value - metrics value
  tag_kvs - tag_key and tag_value list, 
    should be formatted as ["tag_key_1:tag_value_1","tag_key_2:tag_value_2",...]
Example:
  timer("request.cost", 100, ["method:user", "type:upload"])
"""


def timer(name: str, value: float, tag_kvs: list):
    if not _is_enable_metrics():
        return
    collect_key = _build_collect_key(name, tag_kvs)
    _update_metric(MetricsType.metrics_type_timer, collect_key, value)


"""
Parameters:
  key - metrics name
  begin - the unit of `begin` is milliseconds
  tag_kvs - tag_key and tag_value list, 
    should be formatted as ["tag_key_1:tag_value_1","tag_key_2:tag_value_2",...]
Example:
  latency("request.latency", start_time_ms, ["method:user", "type:upload"])
"""


def latency(key: str, begin: float, tag_kvs: list):
    timer(key, time.time_ns() / 1e6 - begin, tag_kvs)


class MetricValue(object):
    def __init__(self, value: object, flushed_value=None):
        self.value = value
        self.flushed_value = flushed_value
        self.updated = False
        self.lock = threading.Lock()


# As long as the init function is called, the metrics are enabled
def init(metrics_opts: tuple):
    global metrics_cfg
    metrics_cfg = MetricsCfg()
    for opt in metrics_opts:
        opt.fill(metrics_cfg)

    metrics_collector[MetricsType.metrics_type_store] = {}
    metrics_collector[MetricsType.metrics_type_counter] = {}
    metrics_collector[MetricsType.metrics_type_timer] = {}

    metrics_locks[MetricsType.metrics_type_store] = threading.Lock()
    metrics_locks[MetricsType.metrics_type_counter] = threading.Lock()
    metrics_locks[MetricsType.metrics_type_timer] = threading.Lock()

    global initialed
    if not initialed:
        initialed = True
        threading.Thread(target=_report()).start()


def _report():
    if not _is_enable_metrics():
        return
    _flushTimer()
    _flushCounter()
    _flushStore()

    # a timer only execute once after spec duration
    threading.Timer(metrics_cfg.flush_interval_ms / 1000, _report).start()
    return


def _flushStore():
    metrics_requests = []
    with metrics_locks.get(MetricsType.metrics_type_store):
        for collect_key, metric in metrics_collector.get(MetricsType.metrics_type_store).items():
            if metric.updated:
                metric.updated = False
                name, tag_kvs, ok = _parse_name_and_tags(collect_key)
                if not ok:
                    continue
                metrics_request: Metric = Metric()
                metrics_request.metric = metrics_cfg.prefix + "." + name
                metrics_request.tags.update(tag_kvs)
                metrics_request.value = metric.value
                metrics_request.timestamp = int(time.time())
                metrics_requests.append(metrics_request)
    if len(metrics_requests) > 0:
        url = OTHER_URL_FORMAT.format(metrics_cfg.http_schema, metrics_cfg.domain)
        _send_metrics(metrics_requests, url)


def _flushCounter():
    metrics_requests = []
    with metrics_locks.get(MetricsType.metrics_type_counter):
        for collect_key, metric in metrics_collector.get(MetricsType.metrics_type_counter).items():
            if metric.updated:
                metric.updated = False
                name, tag_kvs, ok = _parse_name_and_tags(collect_key)
                if not ok:
                    continue
                # metric.value may not be the latest, the case is acceptable
                value_copy = metric.value
                metrics_request: Metric = Metric()
                metrics_request.metric = metrics_cfg.prefix + "." + name
                metrics_request.tags.update(tag_kvs)
                metrics_request.value = value_copy - metric.flushed_value
                metrics_request.timestamp = int(time.time())
                metrics_requests.append(metrics_request)
                metric.flushed_value = value_copy
                # if the value is too large, reset it, it rarely happen, no lock is acceptable
                if value_copy >= sys.float_info.max / 2:
                    metric.value = 0.0
                    metric.flushed_value = 0.0

    if len(metrics_requests) > 0:
        url = COUNTER_URL_FORMAT.format(metrics_cfg.http_schema, metrics_cfg.domain)
        _send_metrics(metrics_requests, url)


def _flushTimer():
    metrics_requests = []
    with metrics_locks.get(MetricsType.metrics_type_timer):
        for collect_key, metric in metrics_collector.get(MetricsType.metrics_type_timer).items():
            if metric.updated:
                metric.updated = False
                name, tag_kvs, ok = _parse_name_and_tags(collect_key)
                if not ok:
                    continue
                snapshot = metric.value.snapshot()
                metric.value.clear()
                metrics_requests.extend(_build_stat_metrics(snapshot, name, tag_kvs))

    if len(metrics_requests) > 0:
        url = OTHER_URL_FORMAT.format(metrics_cfg.http_schema, metrics_cfg.domain)
        _send_metrics(metrics_requests, url)


def _send_metrics(metrics_requests: list, url: str):
    metric_message: MetricMessage = MetricMessage()
    metric_message.metrics.extend(metrics_requests)
    try:
        _send(metric_message, url)
        if _enable_print_log():
            log.debug("[BytePlusSDK][Metrics] send metrics success, url:{}, metrics_requests:{}".format(url,
                                                                                                        metrics_requests))
    except BaseException as e:
        log.error(
            "[BytePlusSDK][Metrics] send metrics exception, msg:{}, url:{}, metricsRequests:{}".format(str(e), url,
                                                                                                       metrics_requests))


def _build_stat_metrics(sample: SampleSnapshot, name: str, tag_kvs: map):
    timestamp = int(time.time())
    metrics_requests = []
    for stat_name in timer_stat_metrics:
        stat_func = sample.get_func_from_name(stat_name)
        if stat_func is None:
            continue
        metrics_request: Metric = Metric()
        metrics_request.metric = metrics_cfg.prefix + "." + name + "." + stat_name
        metrics_request.tags.update(tag_kvs)
        metrics_request.value = stat_func()
        metrics_request.timestamp = timestamp
        metrics_requests.append(metrics_request)
    return metrics_requests


def _is_enable_metrics() -> bool:
    if metrics_cfg is None:
        return False
    return metrics_cfg.enable_metrics


def _enable_print_log() -> bool:
    if metrics_cfg is None:
        return False
    return metrics_cfg.print_log


def _update_metric(metrics_type: MetricsType, collect_key: str, value: float):
    metric: MetricValue = _get_or_create_metric(metrics_type, collect_key)
    if metrics_type == MetricsType.metrics_type_store:
        metric.value = value
    if metrics_type == MetricsType.metrics_type_counter:
        with metric.lock:
            metric.value = metric.value + value
    if metrics_type == MetricsType.metrics_type_timer:
        metric.value.update(value)
    metric.updated = True


def _get_or_create_metric(metrics_type: MetricsType, collect_key: str):
    if metrics_collector.get(metrics_type).get(collect_key) is not None:
        return metrics_collector.get(metrics_type).get(collect_key)
    with metrics_locks.get(metrics_type):
        if metrics_collector.get(metrics_type).get(collect_key) is None:
            metrics_collector.get(metrics_type)[collect_key] = _build_default_metric(metrics_type)
            return metrics_collector.get(metrics_type).get(collect_key)


def _build_default_metric(metrics_type: MetricsType):
    if metrics_type == MetricsType.metrics_type_timer:
        return MetricValue(Sample(RESERVOIR_SIZE))
    if metrics_type == MetricsType.metrics_type_counter:
        return MetricValue(0.0, 0.0)
    return MetricValue(0.0)


# send httpRequest to metrics server
def _send(metric_requests: MetricMessage, url: str):
    headers = {"Content-Type": "application/protobuf", "Accept": "application/json"}
    req_bytes: bytes = metric_requests.SerializeToString()
    for i in range(MAX_TRY_TIMES):
        try:
            response = requests.post(url=url, headers=headers, data=req_bytes,
                                     timeout=metrics_cfg.http_timeout_ms / 1000)
            if response.status_code == SUCCESS_HTTP_CODE:
                return
            if response.content is None:
                raise BizException("rsp body is null")
            raise BizException("do http request fail, url:{}， rsp:{}".format(url, response.content))

        except BaseException as e:
            if _is_timeout_exception(e) and i < MAX_TRY_TIMES - 1:
                continue
            raise BizException(str(e))
