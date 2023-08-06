from byteplus.core.metrics import latency, counter


def report_request_success(metrics_prefix: str, url: str, begin: float):
    url_tag = _build_url_tags(url)
    latency(_build_latency_key(metrics_prefix), begin, url_tag)
    counter(_build_counter_key(metrics_prefix), 1, url_tag)


def report_request_error(metrics_prefix: str, url: str, begin: float, code: int, message: str):
    url_tag = _build_url_tags(url)
    url_tag.extend(["code:" + str(code), "message:" + message])
    latency(_build_latency_key(metrics_prefix), begin, url_tag)
    counter(_build_counter_key(metrics_prefix), 1, url_tag)


def report_request_exception(metrics_prefix: str, url: str, begin: float, e: BaseException):
    url_tag = _build_url_tags(url)
    tag_kvs = _with_exception_tags(url_tag, e)
    latency(_build_latency_key(metrics_prefix), begin, tag_kvs)
    counter(_build_counter_key(metrics_prefix), 1, tag_kvs)


def _with_exception_tags(tag_kvs: list, e: BaseException):
    msg = str(e).lower()
    if "time" in msg and "out" in msg:
        if "connect" in msg:
            tag_kvs.append("message:connect-timeout")
            return tag_kvs
        if "read" in msg:
            tag_kvs.append("message:read-timeout")
            return tag_kvs
        tag_kvs.append("message:timeout")
        return tag_kvs
    tag_kvs.append("message:other")
    return tag_kvs


def _build_url_tags(url: str):
    return ["url:" + _adjust_url_tag(url), "req_type:" + _parse_req_type(url)]


def _adjust_url_tag(url: str):
    return url.replace("=", "_is_")


def _parse_req_type(url: str):
    if "ping" in url:
        return "ping"
    if "data/api" in url:
        return "data-api"
    if "predict/api" in url:
        return "predict-api"
    return "unknown"


def _build_counter_key(metrics_prefix: str):
    return metrics_prefix + "." + "count"


def _build_latency_key(metrics_prefix: str):
    return metrics_prefix + "." + "latency"
