# coding:utf-8
# -*- coding:utf-8 -*-
import Queue
import logging
from tccm.pb import sdk_metric_pb_pb2
from tccm.internal.common.business import BusinessInfo


class Worker(object):
    def __init__(self):
        self.transport = None
        self.transport_mode = None
        self.business_info = BusinessInfo()
        self.global_tags = None
        # self.queueMetrics = Manager().Queue()
        self.queue_metrics = Queue.Queue()
        self.tccm_agent_addr = None
        self.tccm_agent_port = None
        self.max_byte_per_payload = None

    def new_worker(self, transport, transport_mode, business_info, global_tags,
                   queue_length_with_worker, max_byte_per_payload, tccm_agent_addr,
                   tccm_agent_port):
        """
         * 创建worker模块
         * @param
         * @return
        """
        self.transport = transport
        self.transport_mode = transport_mode
        self.business_info = business_info
        self.global_tags = global_tags
        # self.queueMetrics = Manager().Queue(queue_length_with_worker)
        self.queue_metrics = Queue.Queue(queue_length_with_worker)
        self.tccm_agent_addr = tccm_agent_addr
        self.tccm_agent_port = tccm_agent_port
        self.max_byte_per_payload = max_byte_per_payload
        return self

    def write_metric(self, metric):
        """
         * 将业务数据写入worker模块的管道
         * @param
         * @return
        """
        # 创建进程池, Pool(3) 表示创建容量为3个进程的进程池

        # po = Pool(5)
        # po.apply_async(self.write_data, args=(metric,))
        # po.apply_async(self.send_data)
        # po.close()
        # po.join()
        self.queue_metrics.put(item=metric)
        self.send_data()

    def write_data(self, metric):
        self.queue_metrics.put(item=metric)

    def send_data(self):
        """
         * 将获取到的数据处理之后发送
         * @param
         * @return
        """
        if not self.queue_metrics.empty():
            metric_list = sdk_metric_pb_pb2.MetricList()
            metric_list.appId = self.business_info.get_business_app_id()
            metric_list.namespace = self.business_info.get_business_name()
            if (self.business_info.get_report_region()) > 0:
                metric_list.reportRegionWithAgent = self.business_info.get_report_region()
            metric = metric_list.metrics.add()
            serialize_to_string = self.queue_metrics.get().SerializeToString()
            metric1 = sdk_metric_pb_pb2.Metric()
            metric1.ParseFromString(serialize_to_string)
            metric.appId = metric1.appId
            metric.namespace = metric1.namespace
            metric.time = metric1.time
            metric.measurement = metric1.measurement
            for tmp_tag in metric1.tags:
                tag = metric.tags.add()
                tag.value = tmp_tag.value
                tag.key = tmp_tag.key
            for tmp_field in metric1.fields:
                fields = metric.fields.add()
                fields.fieldType = tmp_field.fieldType
                fields.name = tmp_field.name
                fields.value = tmp_field.value
            for tmp_histogram_field in metric1.histogramField:
                histogram_field = metric.histogramField.add()
                histogram_field.name = tmp_histogram_field.name
                histogram_field.value = tmp_histogram_field.value
                for bucket in tmp_histogram_field.bucket:
                    histogram_field.bucket.append(bucket)
            for tmp_summary_field in metric1.summaryField:
                summary_field = metric.summaryField.add()
                summary_field.name = tmp_summary_field.name
                summary_field.value = tmp_summary_field.value
                for quantile in tmp_summary_field.quantile:
                    summary_field.quantile.append(quantile)
            for tmp_hll_field in metric1.hllField:
                hll_field = metric.hllField.add()
                hll_field.name = tmp_hll_field.name
                hll_field.value = tmp_hll_field.value
                hll_field.precision = tmp_hll_field.precision

            metric_list_string = metric_list.SerializeToString()
            if len(metric_list_string) > self.max_byte_per_payload:
                logging.error("metric list of one measurement more than 64K, dropped data, cur body len:",
                              len(metric_list_string))
                raise NotImplementedError(u"metric list of one measurement more than 64K, dropped data, cur body len:",
                                          len(metric_list_string))
            return self.transport.write(metric_list_string)
