import metrics_collector as mc
from metrics_option import MetricsOption as mo
import time
import logging
import threading

send_times = 1000000


def metrics_init():
    # default log level is warning
    logging.basicConfig(level=logging.DEBUG)
    mc.init(
        (mo.with_metrics_log(),
         mo.with_flush_interval(10000))
    )


def store_report():
    for i in range(send_times):
        mc.store("request.store", 200, ["type:test_metrics1", "other_tag:xxx"])
        mc.store("request.store", 100, ["type:test_metrics2", "other_tag:xxx"])
        time.sleep(0.1)
    print("stop store reporting")


def count_report():
    for i in range(send_times):
        mc.counter("request.counter", 200, ["type:test_metrics1", "other_tag:xxx"])
        mc.counter("request.counter", 100, ["type:test_metrics2", "other_tag:xxx"])
        time.sleep(0.2)
    print("stop counter reporting")


def timer_report():
    for i in range(send_times):
        begin = time.time_ns() / 1e6
        time.sleep(0.1)
        mc.latency("request.timer", begin, ["type:test_metrics1", "other_tag:xxx"])
        begin = time.time_ns() / 1e6
        time.sleep(0.2)
        mc.latency("request.timer", begin, ["type:test_metrics2", "other_tag:xxx"])

    print("stop timer reporting")


if __name__ == '__main__':
    metrics_init()
    # store_report()
    # count_report()
    # timer_report()

    t1 = threading.Thread(target=store_report)
    t2 = threading.Thread(target=count_report)
    t3 = threading.Thread(target=timer_report)
    t1.start()
    t2.start()
    t3.start()

    print('start report')
    t1.join()
    t2.join()
    t3.join()
    print('end report')
