# coding:utf-8
# -*- coding:utf-8 -*-
from tccm.pb import sdk_metric_pb_pb2
from tccm.internal.common.util import Util
from tccm.internal.common.default import DefaultMeasurement, DefaultMeasurement, MetricFieldType, \
    DefaultConfModuleMetric


class CustomMetric(object):
    def __init__(self):
        custom_metric = sdk_metric_pb_pb2.Metric()
        custom_metric.time = 0
        self.type = "custom_metric"
        self.custom_metric = custom_metric

    # 清除自定义指标表
    def clear(self):
        custom_metric = sdk_metric_pb_pb2.Metric()
        custom_metric.time = 0
        self.custom_metric = custom_metric
        return self

    # 添加维度
    # 维度名如果出现特殊字符, 则统一替换成下划线
    # 维度名或者维度值不能超过一定长度, 超过就丢弃
    def add_tags(self, tags):

        for key in tags:
            tag = self.custom_metric.tags.add()
            if len(key) <= 0 | len(key) > DefaultMeasurement.DefaultTagNameLengthOfMeasurement | len(
                    tags[key]) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
                continue
            res_key = Util().escape_metric_name_and_tag(key)
            tag.key = res_key
            tag.value = tags[key]
        return self

    # 设置自定义指标表时间
    def set_time(self, time):
        self.custom_metric.time = time
        return self

    # 获取自定义指标表内部结构
    def get_raw_metric(self):
        return self.custom_metric

    # 设置自定义指标表表名
    def set_measurement(self, measurement):
        self.custom_metric.measurement = measurement
        return self

    # 设置自定义指标表表名
    def set_app_id(self, app_id):
        self.custom_metric.appId = app_id
        return self

    # 设置自定义指标表表名
    def set_namespace(self, namespace):
        self.custom_metric.namespace = namespace
        return self

    # 获取自定义指标表表名
    def get_measurement(self):
        return self.custom_metric.measurement

    # 给自定义指标表添加 sum 类型指标
    def add_sum_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.SUM)
        return self

    # 给自定义指标表添加 min 类型指标
    def add_min_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.MIN)
        return self

    # 给自定义指标表添加 max 类型指标
    def add_max_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.MAX)
        return self

    # 给自定义指标表添加 first 类型指标
    def add_first_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.FIRST)
        return self

    # 给自定义指标表添加 last 类型指标
    def add_last_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.LAST)
        return self

    # 给自定义指标表添加 counter 类型指标
    def add_counter_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.COUNTER)
        return self

    # 给自定义指标表添加 gauge 类型指标
    def add_gauge_field(self, name, value):
        self.add_basic_field(name, value, sdk_metric_pb_pb2.GAUGE)
        return self

    # 给自定义指标表添加 histogram 类型指标
    def add_histogram_field(self, name, value, buckets):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_histogram_field = self.custom_metric.histogramField.add()
        tmp_histogram_field.name = res_name
        tmp_histogram_field.value = value
        if len(buckets) <= 0:
            for default_bucket in DefaultMeasurement.DefaultHistogramBuckets:
                tmp_histogram_field.bucket.append(default_bucket)
        else:
            for bucket in buckets:
                tmp_histogram_field.bucket.append(bucket)
        return self

    # 给自定义指标表添加 summary 类型指标
    def add_summary_field(self, name, value, quantiles):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        self.tag = Util().escape_metric_name_and_tag(name)
        res_name = self.tag
        tmp_summary_field = self.custom_metric.summaryField.add()
        tmp_summary_field.name = res_name
        tmp_summary_field.value = value
        if len(quantiles) <= 0:
            for default_quantile in DefaultMeasurement.DefaultSummaryQuantiles:
                tmp_summary_field.quantile.append(default_quantile)

        else:
            for quantile in quantiles:
                tmp_summary_field.quantile.append(quantile)
        return self

    # 给自定义指标表添加 set(去重统计) 类型指标,使用默认精度
    def add_set_field(self, name, value):
        self.add_set_field_with_precision(name, value, DefaultMeasurement.DefaultSetFieldPrecision)
        return self

    # 给自定义指标表添加 set(去重统计) 类型指标,可设置精度. precision 为精度，取值范围[6-18],值越大精度越高
    def add_set_field_with_precision(self, name, value, precision):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_hll_field = sdk_metric_pb_pb2.HllField()
        tmp_hll_field.name = res_name
        tmp_hll_field.value = value
        if precision < DefaultMeasurement.DefaultSetFieldMinPrecision | \
                precision > DefaultMeasurement.DefaultSetFieldMaxPrecision:
            precision = DefaultMeasurement.DefaultSetFieldPrecision
        tmp_hll_field.precision = precision
        return self

    # 给自定义指标表添加任意类型指标
    def add_field(self, name, value, field_type):
        convert_value = self.convert(value)
        if field_type == MetricFieldType.MetricSumField:
            self.add_sum_field(name, convert_value)
        elif field_type == MetricFieldType.MetricMinField:
            self.add_min_field(name, convert_value)
        elif field_type == MetricFieldType.MetricMaxField:
            self.add_max_field(name, convert_value)
        elif field_type == MetricFieldType.MetricFirstField:
            self.add_first_field(name, convert_value)
        elif field_type == MetricFieldType.MetricLastField:
            self.add_last_field(name, convert_value)
        elif field_type == MetricFieldType.MetricCounterField:
            self.add_counter_field(name, convert_value)
        elif field_type == MetricFieldType.MetricGaugeField:
            self.add_gauge_field(name, convert_value)
        elif field_type == MetricFieldType.MetricHistogramField:
            self.add_histogram_field(name, convert_value, DefaultMeasurement.DefaultHistogramBuckets)
        elif field_type == MetricFieldType.MetricSummaryField:
            self.add_summary_field(name, convert_value, DefaultMeasurement.DefaultSummaryQuantiles)
        return self

    # 内部添加基础指标的子函数
    def add_basic_field(self, name, value, field_type):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_basic_field = self.custom_metric.fields.add()
        tmp_basic_field.name = res_name
        tmp_basic_field.value = value
        tmp_basic_field.fieldType = field_type
        tmp_basic_field.SerializeToString()

    # todo：转换成 float64
    def convert(self, value):
        return value


class ModuleMetric(object):
    def __init__(self):
        module_metric = sdk_metric_pb_pb2.Metric()
        module_metric.time = 0
        self.type = "module_metric"
        self.module_metric = module_metric

    # 清除模调指标表
    def clear(self):
        module_metric = sdk_metric_pb_pb2.Metric()
        module_metric.time = 0
        self.module_metric = module_metric
        return self

    # 设置自定义指标表表名
    def set_measurement(self, measurement):
        self.module_metric.measurement = measurement
        return self

    # 获取表名
    def get_measurement(self):
        return self.module_metric.measurement

    # 获取内存pb结构体
    def get_raw_metric(self):
        return self.module_metric

    # 设置时间
    def set_time(self, time):
        self.module_metric.time = time
        return self

    # 添加主调模块维度
    def with_a_module(self, a_module):
        if len(a_module) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionActiveModule
        tag.value = a_module
        return self

    # 添加主调接口维度
    def with_a_interface(self, a_interface):
        if len(a_interface) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionActiveInterface
        tag.value = a_interface
        return self

    # 添加主调IP维度
    def with_a_ip(self, a_ip):
        if len(a_ip) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionActiveIp
        tag.value = a_ip
        return self

    # 添加被调模块维度
    def with_p_module(self, p_module):
        if len(p_module) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionPassiveModule
        tag.value = p_module
        return self

    # 添加被调接口维度
    def with_p_interface(self, p_interface):
        if len(p_interface) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionPassiveInterface
        tag.value = p_interface
        return self

    # 添加被调IP维度
    def with_p_ip(self, p_ip):
        if len(p_ip) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionPassiveIp
        tag.value = p_ip
        return self

    # 添加当前环境维度
    def with_env(self, env):
        if len(env) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionEnv
        tag.value = env
        return self

    # 添加返回码维度
    def with_ret_code(self, res_code):
        if len(res_code) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionRetCode
        tag.value = res_code
        return self

    # 添加状态码维度
    def with_status(self, status):
        if len(status) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
            return
        tag = self.module_metric.tags.add()
        tag.key = DefaultConfModuleMetric.DefaultDimensionStatus
        tag.value = status
        return self

    # 添加主调耗时指标
    def with_active_time_cost(self, time_cost):
        tmp_histogram_field = self.module_metric.histogramField.add()
        tmp_histogram_field.name = DefaultConfModuleMetric.DefaultActiveTimeCost
        tmp_histogram_field.value = time_cost
        for default_bucket in DefaultMeasurement.DefaultHistogramBuckets:
            tmp_histogram_field.bucket.append(default_bucket)
        return self

    # 添加主调成功数指标
    def with_active_success_count(self, success_count):
        tmp_basic_field = self.module_metric.fields.add()
        tmp_basic_field.name = DefaultConfModuleMetric.DefaultActiveSuccessCount
        tmp_basic_field.value = success_count
        tmp_basic_field.fieldType = sdk_metric_pb_pb2.SUM
        return self

    # 添加主调请求数指标
    def with_active_request_count(self, req_count):
        tmp_basic_field = self.module_metric.fields.add()
        tmp_basic_field.name = DefaultConfModuleMetric.DefaultActiveRequestCount
        tmp_basic_field.value = req_count
        tmp_basic_field.fieldType = sdk_metric_pb_pb2.SUM
        return self

    # 添加被调耗时指标
    def with_passive_time_cost(self, time_cost):
        tmp_histogram_field = self.module_metric.histogramField.add()
        tmp_histogram_field.name = DefaultConfModuleMetric.DefaultActiveTimeCost
        tmp_histogram_field.value = time_cost
        for default_bucket in DefaultMeasurement.DefaultHistogramBuckets:
            tmp_histogram_field.bucket.append(default_bucket)
        return self

    # 添加被调成功数指标
    def with_passive_success_count(self, success_count):
        tmp_basic_field = self.module_metric.fields.add()
        tmp_basic_field.name = DefaultConfModuleMetric.DefaultPassiveSuccessCount
        tmp_basic_field.value = success_count
        tmp_basic_field.fieldType = sdk_metric_pb_pb2.SUM
        return self

    # 添加被调请求数指标
    def with_passive_request_count(self, req_count):
        tmp_basic_field = self.module_metric.fields.add()
        tmp_basic_field.name = DefaultConfModuleMetric.DefaultPassiveRequestCount
        tmp_basic_field.value = req_count
        tmp_basic_field.fieldType = sdk_metric_pb_pb2.SUM
        return self

    # 添加自定义维度
    def add_custom_dimension(self, dimensions):
        dimension = self.module_metric.tags.add()
        for key in dimensions:
            if len(key) <= 0 | len(key) > DefaultMeasurement.DefaultTagNameLengthOfMeasurement | len(
                    dimensions[key]) > DefaultMeasurement.DefaultTagValueLengthOfMeasurement:
                continue
            res_key = Util().escape_metric_name_and_tag(key)
            dimension.key = res_key
            dimension.value = dimensions[key]
        return self

    # 添加自定义指标内部子函数
    def add_custom_field_sub(self, name, value, field_type):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_custom_field = self.module_metric.fields.add()
        tmp_custom_field.name = res_name
        tmp_custom_field.value = value
        tmp_custom_field.fieldType = field_type

    # 添加自定义 sum 类指标
    def add_custom_sum_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.SUM)
        return self

    # 添加自定义 min 类指标
    def add_custom_min_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.MIN)
        return self

    # 添加自定义 max 类指标
    def add_custom_max_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.MAX)
        return self

    # 添加自定义 first 类指标
    def add_custom_first_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.FIRST)
        return self

        # 添加自定义 last 类指标

    def add_custom_last_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.LAST)
        return self

    # 添加自定义 counter 类指标
    def add_custom_counter_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.COUNTER)
        return self

    # 添加自定义 gauge 类指标
    def add_custom_gauge_field(self, name, value):
        self.add_custom_field_sub(name, value, sdk_metric_pb_pb2.GAUGE)
        return self

    # 添加自定义 histogram 类指标
    def add_custom_histogram_field(self, name, value, buckets):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_histogram_field = self.module_metric.histogramField.add()
        tmp_histogram_field.name = res_name
        tmp_histogram_field.value = value
        if len(buckets) <= 0:
            for default_bucket in DefaultMeasurement.DefaultHistogramBuckets:
                tmp_histogram_field.bucket.append(default_bucket)
        else:
            for bucket in buckets:
                tmp_histogram_field.bucket.append(bucket)

        return self

    # 添加自定义 summary 类指标
    def add_custom_summary_field(self, name, value, quantiles):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_summary_field = self.module_metric.summaryField.add()
        tmp_summary_field.name = res_name
        tmp_summary_field.value = value
        if len(quantiles) <= 0:
            for default_quantile in DefaultMeasurement.DefaultSummaryQuantiles:
                tmp_summary_field.quantile.append(default_quantile)
        else:
            for quantile in quantiles:
                tmp_summary_field.quantile.append(quantile)
        return self

    # 给自定义指标表添加 set(去重统计) 类型指标，使用默认精度
    def add_set_field(self, name, value):
        self.add_set_field_with_precision(name, value, DefaultMeasurement.DefaultSetFieldPrecision)
        return self

    # 给自定义指标表添加 set(去重统计) 类型指标，可设置精度，precision 为精度，取值范围[6-18]，值越大精度越高
    def add_set_field_with_precision(self, name, value, precision):
        if len(name) <= 0 | len(name) > DefaultMeasurement.DefaultFieldLengthOfMeasurement:
            return self
        res_name = Util().escape_metric_name_and_tag(name)
        tmp_hll_field = sdk_metric_pb_pb2.HllField()
        tmp_hll_field.name = res_name
        tmp_hll_field.value = value
        if precision < DefaultMeasurement.DefaultSetFieldMinPrecision | \
                precision > DefaultMeasurement.DefaultSetFieldMaxPrecision:
            precision = DefaultMeasurement.DefaultSetFieldPrecision
        tmp_hll_field.precision = precision
        return self

    # 添加任意类型自定义指标
    def add_custom_field(self, name, value, field_type):
        convert_value = self.convert(value)
        if field_type == MetricFieldType.MetricSumField:
            self.add_custom_sum_field(name, convert_value)
        elif field_type == MetricFieldType.MetricMinField:
            self.add_custom_min_field(name, convert_value)
        elif field_type == MetricFieldType.MetricMaxField:
            self.add_custom_max_field(name, convert_value)
        elif field_type == MetricFieldType.MetricFirstField:
            self.add_custom_first_field(name, convert_value)
        elif field_type == MetricFieldType.MetricLastField:
            self.add_custom_last_field(name, convert_value)
        elif field_type == MetricFieldType.MetricCounterField:
            self.add_custom_counter_field(name, convert_value)
        elif field_type == MetricFieldType.MetricGaugeField:
            self.add_custom_gauge_field(name, convert_value)
        elif field_type == MetricFieldType.MetricHistogramField:
            self.add_custom_histogram_field(name, convert_value, DefaultMeasurement.DefaultHistogramBuckets)
        elif field_type == MetricFieldType.MetricSummaryField:
            self.add_custom_summary_field(name, convert_value, DefaultMeasurement.DefaultSummaryQuantiles)
        return self

    # todo：转换成 float64
    def convert(self, value):
        return value
