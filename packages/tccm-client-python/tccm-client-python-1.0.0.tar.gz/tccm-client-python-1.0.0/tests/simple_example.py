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
    option.set_tccm_agent_addr("10.247.44.116")
    # option.set_transport_mode_use_http()
    # option.set_max_bytes_per_payload(111111)
    tccm = TccmClient().init_client(1258344699, "Coding-trpc-nodejs", "gz2", option)
    measurement = Measurement().new_measurement("custom_metric", "ziana_test_measurement")
    measurement.set_app_id(1258344699)
    measurement.set_namespace("Coding-trpc-nodejs")
    measurement.add_tags({"env": "dev", "region": "bj"})
    measurement.add_sum_field(name="my_sum_metric", value=random.randint(0, 100))
    measurement.add_max_field(name="my_max_metric", value=random.randint(0, 100))
    measurement.add_min_field(name="my_min_metric", value=random.randint(0, 100))
    measurement.add_first_field(name="my_first_metric", value=random.randint(0, 100))
    measurement.add_last_field(name="my_last_metric", value=random.randint(0, 100))
    measurement.add_counter_field(name="my_counter_metric", value=random.randint(0, 100))
    measurement.add_gauge_field(name="my_gauge_metric", value=random.randint(0, 100))
    measurement.add_histogram_field(name="my_histogram_metric", value=random.randint(0, 100), buckets=[])
    measurement.add_summary_field(name="my_summary_metric", value=random.randint(0, 100), quantiles=[])
    measurement.add_set_field(name="my_set_metric", value="set_value")

    tccm.write(measurement)
    tccm.close()
