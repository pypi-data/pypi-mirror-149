# coding:utf-8
# -*- coding:utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
import random
import time
from tccm.api.tccm_client import TccmClient, Measurement
from tccm.api.client_option import ClientOption

STR_Len = 10  # 随机字符串的长度
STRS_Count = 10000  # 随机字符串数组的数量

"""
 * 生成随机字符串
 * @param length
"""


def get_rand_str(length):
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(str)

    return salt


"""
 * 上报自定义指标
 * @param tag_num
 * @param field_num
"""


def report_custom_metric(client, tag_num, field_num):
    time_start = time.time()
    custom_metric = Measurement().new_measurement("custom_metric", "ziana_test_measurement")
    for i in range(tag_num):
        custom_metric.add_tags({"env": get_rand_str(3), "region": get_rand_str(2)})
    for j in range(field_num):
        custom_metric.add_sum_field(name="my_sum_metric", value=random.randint(0, 100))
        custom_metric.add_max_field(name="my_max_metric", value=random.randint(0, 100))
        custom_metric.add_min_field(name="my_min_metric", value=random.randint(0, 100))
        custom_metric.add_first_field(name="my_first_metric", value=random.randint(0, 100))
        custom_metric.add_last_field(name="my_last_metric", value=random.randint(0, 100))
        custom_metric.add_counter_field(name="my_counter_metric", value=random.randint(0, 100))
        custom_metric.add_gauge_field(name="my_gauge_metric", value=random.randint(0, 100))
        custom_metric.add_histogram_field(name="my_histogram_metric", value=random.randint(0, 100), buckets=[])
        custom_metric.add_summary_field(name="my_summary_metric", value=random.randint(0, 100), quantiles=[])
        custom_metric.add_set_field(name="my_set_metric", value="set-value")
    client.write(custom_metric)
    one_report_cost_time = (time.time() - time_start) * 1000
    return one_report_cost_time


if __name__ == "__main__":
    option = ClientOption()
    option.set_transport_mode_use_udp()
    tccm = TccmClient().init_client(1258344699, "Coding-trpc-nodejs", "gz2", option)
    tag_num = 5
    field_num = 2
    total_report_time = 5000
    timeStart = time.time()
    total_time_costs = []
    for i in range(total_report_time):
        one_report_cost_time = report_custom_metric(tccm, tag_num, field_num)
        total_time_costs.append(one_report_cost_time)
    totalTimeCost = (time.time() - timeStart)
    max_one_report_cost_time = max(total_time_costs)
    print ("total cost time: %d s:", totalTimeCost)
    print("one report cost time: %d ms:", max_one_report_cost_time)
    print("QPS: %d:count/sec", field_num * total_report_time / totalTimeCost)
    tccm.close()
