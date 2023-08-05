# coding:utf-8
# -*- coding:utf-8 -*-
import logging
from tccm.internal.common.business import BusinessInfo
from tccm.api.client_option import ClientOption
from tccm.internal.work.worker import Worker
from tccm.internal.common.util import Util
from tccm.api.metric import CustomMetric, ModuleMetric
from tccm.internal.transport.transport import TranSport


class TccmClient(object):

    def __init__(self):
        super(TccmClient, self).__init__()
        self.worker = Worker()
        self.business_info = None

    # 初始化 tccm-client, 通过 tccm-agent 上报监控数据
    def init_client(self, business_app_id, business_name, report_region, option=ClientOption()):
        """
         初始化 client, 默认 [[推荐]]
         此方法初始化的 client，会将数据发到 tccm-agent
         @param business_app_id 腾讯云 app_id , 腾讯云官网获取
         @param business_name 业务名, 长度不超过 32，支持字母、数字、下划线
         @param report_region 上报地域
         @param option 控制 client 的选项
         @return 初始化是否成功
        """
        logging.basicConfig(filename='tccm-py.log', format="%(levelname)s:%(asctime)s:%(message)s", level=logging.DEBUG)
        logging.info('init_client successed')
        if business_app_id < 0:
            logging.error("business_app_id should not be 0.")
            raise NotImplementedError(u"business_app_id should not be 0.")
        if Util().check_business_name(business_name) != True:
            logging.error("check businessName failed")
            raise NotImplementedError(u"check businessName failed")
        business_info = BusinessInfo().set_business_info(business_app_id, business_name, report_region)
        opt = ClientOption().resolve_options(option)
        writer = self.init_transport_module(opt)
        client = self.init_internal_module(opt, business_info, writer)
        return client

    # 初始化传输协议 (UDP或HTTP)
    def init_transport_module(self, opt):
        addr = opt.tccm_agent_addr
        port = opt.tccm_agent_port
        writer = TranSport(opt.transport_mode, addr, port)
        return writer

    # 初始化sdk内部模块
    def init_internal_module(self, opt, business_info, transport):
        client = TccmClient()
        client.business_info = business_info
        client.worker = Worker().new_worker(transport, opt.transport_mode, business_info, opt.global_tags,
                                            opt.queue_length_with_worker, opt.max_bytes_per_payload,
                                            opt.tccm_agent_addr,
                                            opt.tccm_agent_port)
        return client

    def write(self, metrics):
        if metrics.type == "custom_metric":
            return self.worker.write_metric(metrics.custom_metric)
        elif metrics.type == "module_metric":
            return self.worker.write_metric(metrics.module_metric)
        else:
            logging.error("invalid metric data type.")
            raise NotImplementedError(u"invalid metric data type.")

    def close(self):
        """
         * 关闭 client
         * @param
         * @return 关闭 client 是否成功
        """
        logging.info('tccm_client closed')
        return self.worker.transport.close()


class Measurement(object):
    def __init__(self):
        super(Measurement, self).__init__()

    def new_measurement(self, type, measurement):
        if type == "custom_metric":
            measurement = CustomMetric().set_measurement(measurement)
        if type == "module_metric":
            measurement = ModuleMetric().set_measurement(measurement)
        return measurement
