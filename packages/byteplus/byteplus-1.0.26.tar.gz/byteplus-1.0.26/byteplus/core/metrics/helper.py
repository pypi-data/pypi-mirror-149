from .constant import DELIMITER
import time


def _build_collect_key(name: str, tags: list):
    return name + DELIMITER + _tags_to_string(tags)


def _tags_to_string(tags: list):
    tags.sort()
    return '|'.join(tags)


def _parse_name_and_tags(src: str):
    index = src.find(DELIMITER)
    if index == -1:
        return None, None, False
    return src[:index], _recover_tags(src[index + len(DELIMITER):]), True


def _recover_tags(tag_string: str) -> dict:
    tags = {}
    for tag in tag_string.split('|'):
        kv = tag.split(':', 1)  # only split once, the first part is key, the rest is value
        if len(kv) < 2:
            continue
        tags[kv[0]] = kv[1]
    return tags


def _is_timeout_exception(e):
    lower_err_msg = str(e).lower()
    if "time" in lower_err_msg and "out" in lower_err_msg:
        return True
    return False
