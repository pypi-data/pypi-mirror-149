# coding:utf-8
# -*- coding:utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from tccm.internal.common.util import Util
from tccm.internal.common.business import BusinessInfo
from tccm.api.tccm_client import TccmClient
from tccm.api.client_option import ClientOption
from tccm.api.metric import CustomMetric

if __name__ == "__main__":
    tccm = TccmClient().init_client(251001011, "ziana_tccm_test", "test", "")
    tccm.close()
    option = ClientOption()
    global_tags = {"city": "guangzhou"}
    option.set_global_tags(global_tags)
    print("util-check-test:", option.get_global_tags())
    # 测试 tccm.internal.common.util
    # input1 = "my_measurement"
    # util1 = Util().check_business_name(input1)
    # util2 = Util().escape_measurement(input1)
    # util3 = Util().escape_metric_name_and_tag(input1)
    # print("util-check-test:", util1, util2, util3)

    # 测试 tccm.internal.common.business
    # business_app_id = 251001011
    # business_name = "business_name"
    # report_region = "gz2"
    # bu = BusinessInfo().set_business_info(business_app_id, business_name, report_region)
    # print("get_business_app_id:", bu.get_business_app_id())
    # print("get_business_name:", bu.get_business_name())
    # print("set_business_info:", bu.get_report_region())

    # 测试 tccm.internal.transport.http
    # conn = HTTP().new_http_writer("m.cyw.com")
    # params = {'cityId': '438'}

    # print(conn.set_writer_timeout(40))
    #
    # print(conn.write(params))
    # print(conn.close())

    # 测试 tccm.api.client_option
    # globalTag = {"key1": "value1", "key2": "value2"}
    # option = [{"global_tags": {"key1": "value1", "key2": "value2"}, "max_bytes_per_payload": 23,
    #            "thread_number_with_worker": 23, "channel_length_with_worker": 23, "regular_interval_ms_with_worker": 23,
    #            "telemetry_is_open": True, "telemetry_report_interval": 23, "max_message_per_payload": 23,
    #            "transport_mode": 23, "tccm_agent_addr": 23}]
    # option = []
    # out = ClientOption().resolve_options(option)
    # op = ClientOption()
    # op.set_max_bytes_per_payload(12)
    #
    #
    # print(op.max_bytes_per_payload)
    #
    # print(out.get_global_tags())

    # custom_metric = CustomMetric().set_measurement("ziana's measurement").add_max_field("name", 34)
    # measurement = custom_metric.get_measurement()
    # print("custom_metric:", custom_metric.custom_metric)
    #
    # # 测试 tccm.api.tccm_client
    # business_app_id = 251001011
    # business_name = "business_name"
    # report_region = "gz2"
    # client = TccmClient().init_client(business_app_id, business_name, report_region, option)
    # data = "test data"
    # values = {'wd': 'word'}
    # client.write(custom_metric)
    # print("client", client)

    # httpClient = HTTP().new_http_writer()
    # data = "test data"
    # values = {'wd': 'word'}
    # httpClient.write(values)
    # httpClient.close()
