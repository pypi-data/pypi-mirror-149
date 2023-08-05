# coding:utf-8
# -*- coding:utf-8 -*-
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from tccm.api.tccm_client import TccmClient, Measurement
from tccm.api.client_option import ClientOption


if __name__ == "__main__":
    option = ClientOption()
    option.set_transport_mode_use_http()
    # option.set_global_tags()
    option.set_max_bytes_per_payload(111111)
    tccm = TccmClient().init_client(251001011, "ziana_tccm_test", "test", option)
    measurement = Measurement().new_measurement("module_metric", "ziana_test_measurement")
    measurement.with_a_module("AApp.AServer.serviceA")
    measurement.with_a_interface("AInterface")
    measurement.with_p_module("PApp.PServer.serviceB")
    measurement.with_p_interface("PInterface")
    measurement.with_p_ip("localhost")
    measurement.with_env("Pre-release")
    measurement.with_ret_code("999")
    measurement.with_status("exception")
    measurement.with_active_time_cost(1.23)
    measurement.with_active_success_count(1)
    measurement.with_active_request_count(1)
    measurement.add_custom_sum_field(name="my_sum_metric", value=random.randint(0, 100))
    measurement.add_custom_max_field(name="my_max_metric", value=random.randint(0, 100))
    measurement.add_custom_min_field(name="my_min_metric", value=random.randint(0, 100))
    measurement.add_custom_first_field(name="my_first_metric", value=random.randint(0, 100))
    measurement.add_custom_last_field(name="my_last_metric", value=random.randint(0, 100))
    measurement.add_custom_counter_field(name="my_counter_metric", value=random.randint(0, 100))
    measurement.add_custom_gauge_field(name="my_gauge_metric", value=random.randint(0, 100))
    measurement.add_custom_histogram_field(name="my_histogram_metric", value=random.randint(0, 100), buckets=[])
    measurement.add_custom_summary_field(name="my_summary_metric", value=random.randint(0, 100), quantiles=[])
    measurement.add_set_field(name="my_set_metric", value="set_value")

    tccm.write(measurement)
    tccm.close()
