# coding:utf-8
# -*- coding:utf-8 -*-
from tccm.internal.common.default import DefaultConfClientOption
from tccm.internal.transport.transport import TranSport


class ClientOption(object):
    """
     * 用于控制 TccmClient 行为的类
     * @author zianazhao
     * @date 2021/7/23
    """

    def __init__(self):
        """
        * 设置默认的参数
        * 默认的参数为使用最优的参数
        """
        self.global_tags = {}
        self.max_bytes_per_payload = DefaultConfClientOption.DefaultMaxBytePerPayload
        self.transport_mode = DefaultConfClientOption.DefaultTransportMode
        self.tccm_agent_addr = DefaultConfClientOption.DefaultTccmAgentAddr
        self.tccm_agent_port = DefaultConfClientOption.DefaultTccmAgentPort
        self.queue_length_with_worker = DefaultConfClientOption.DefaultChannelLengthWithWorker

    def resolve_options(self, options):
        if options == "":
            return self
        self.global_tags = options.global_tags
        self.max_bytes_per_payload = options.max_bytes_per_payload
        self.transport_mode = options.transport_mode
        self.tccm_agent_addr = options.tccm_agent_addr
        self.tccm_agent_port = options.tccm_agent_port
        self.queue_length_with_worker = options.queue_length_with_worker
        return self

    def set_global_tags(self, global_tags):
        """
         * 设置公共维度,会给所有指标添加此维度
         * @param globalTags 公共维度
        """
        if global_tags:
            self.global_tags = global_tags
        return self

    def set_max_bytes_per_payload(self, max_bytes_per_payload):
        """
         * 设置单个buffer的最大大小
         * 默认为4M，且不能超过4M(下游规定)
         * 所有业务的监控数据 metric 会存在 buffer 中，然后一并发送
         * @param maxBytesPerPayload 单个 buffer 大小
        """
        self.max_bytes_per_payload = max_bytes_per_payload
        return self

    def set_tccm_agent_addr(self, tccm_agent_addr):
        """
         * 设置tccm-agent地址
         * @param tccm_agent_addr tccm-agent地址
        """
        self.tccm_agent_addr = tccm_agent_addr
        return self

    def set_tccm_agent_port(self, tccm_agent_port):
        """
         * 设置tccm-agent端口
         * @param tccm_agent_port tccm-agent端口
        """
        self.tccm_agent_port = tccm_agent_port
        return self

    def set_transport_mode_use_http(self):
        """
         * 设置使用HTTP协议进程发送数据
         * @param
        """
        self.transport_mode = TranSport.HTTPTransportMode
        return self

    def set_transport_mode_use_udp(self):
        """
         * 设置使用UDP协议进程发送数据
         * @param
        """
        self.transport_mode = TranSport.UDPTransportMode
        return self

    def set_queue_length_with_worker(self, queue_length_with_worker):
        """
         * 设置worker模块中队列长度
         * @param queue_length_with_worker worker 模块中队列长度
        """
        self.queue_length_with_worker = queue_length_with_worker
        return self

    def get_global_tags(self):
        return self.global_tags

    def get_max_bytes_per_payload(self):
        return self.max_bytes_per_payload

    def get_transport_mode_use_http(self):
        return self.transport_mode

    def get_tccm_agent_addr(self):
        return self.tccm_agent_addr

    def get_tccm_agent_port(self):
        return self.tccm_agent_port

    def get_queue_length_with_worker(self):
        return self.queue_length_with_worker
