# coding:utf-8
# -*- coding:utf-8 -*-

from enum import Enum, unique
from tccm.internal.transport.transport import TranSport





@unique
class MetricFieldType(Enum):
    MetricSumField = 0
    MetricMinField = 1
    MetricMaxField = 2
    MetricFirstField = 3
    MetricLastField = 4
    MetricCounterField = 5
    MetricGaugeField = 6
    MetricSummaryField = 7
    MetricHistogramField = 8


class DefaultConfClientOption(object):
    # 单个要发送的包中最多的表的数量
    DefaultMaxMessagePerPayload = 100
    # 单个要发送的包最大的字节数, UDP
    # 单次最多发送65535字节，减去udp报头(8)、IP报头(60)的结果
    # HTTP 发送也遵循这个限制, 因为包太大，解包也会消耗性能
    DefaultMaxBytePerPayload = 65467
    # worker模块中worker协程的个数
    DefaultThreadNumberWithWorker = 1
    # worker模块中管道默认的长度
    DefaultChannelLengthWithWorker = 200000
    # worker模块中定时写数据的时间, 单位毫秒
    # DefaultRegularIntervalMsWithWorker = 10
    # 是否开启SDK自监控
    DefaultTelemetryIsOpen = True
    # 自监控上报时间间隔
    DefaultTelemetryReportInterval = 60
    # 传输数据使用的默认协议
    DefaultTransportMode = TranSport.HTTPTransportMode
    # 默认的tccm - agent地址
    DefaultTccmAgentAddr = "127.0.0.1"
    DefaultTccmAgentPort = 8126


class DefaultConfModuleMetric(object):
    DefaultModuleMeasurement = "module_call"
    DefaultActiveTimeCost = "active_time_cost"
    DefaultActiveSuccessCount = "active_success_count"
    DefaultActiveRequestCount = "active_request_count"
    DefaultPassiveTimeCost = "passive_time_cost"
    DefaultPassiveSuccessCount = "passive_success_count"
    DefaultPassiveRequestCount = "passive_request_count"

    DefaultDimensionActiveModule = "AModule"
    DefaultDimensionActiveInterface = "AInterface"
    DefaultDimensionActiveIp = "AIp"
    DefaultDimensionPassiveModule = "PModule"
    DefaultDimensionPassiveInterface = "PInterface"
    DefaultDimensionPassiveIp = "PIp"
    DefaultDimensionEnv = "Namespace"
    DefaultDimensionRetCode = "RetCode"
    DefaultDimensionStatus = "Status"


class DefaultMeasurement(object):
    # measurement 默认的表名
    DefaultMeasurementName = "default_measurement"

    # 统计方式为 set 时的精度
    DefaultSetFieldPrecision = 14
    # 统计方式为 set 时最小精度
    DefaultSetFieldMinPrecision = 6
    # 统计方式为 set 时最大精度
    DefaultSetFieldMaxPrecision = 18

    # measurement 最大的长度
    DefaultMeasurementMaxLength = 128

    # 业务标识 BusinessName 最大的长度
    DefaultBusinessNameMaxLength = 32

    # 一张表中tag和field的字段不能超过500
    DefaultTagAndFieldNumberOfMeasurement = 500

    # 一张表中指标名的最大长度, 默认128个字符
    DefaultFieldLengthOfMeasurement = 128

    # 一张表中维度名的最大长度, 默认128个字符
    DefaultTagNameLengthOfMeasurement = 128

    # 一张表中维度值的最大长度, 默认128个字符
    DefaultTagValueLengthOfMeasurement = 128

    # 当上报方式为http时，http的URL的参数, 注：版本使用http路由v2版本
    DefaultTccmAgentHttpUrlParam = "/api/v2"
    DefaultHistogramBuckets = [10, 50, 100]
    DefaultSummaryQuantiles = [0.5, 0.95, 0.99]
