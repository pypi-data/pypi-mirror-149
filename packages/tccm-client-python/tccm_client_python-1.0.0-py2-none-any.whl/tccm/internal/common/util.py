# coding:utf-8
# -*- coding:utf-8 -*-
import logging
from tccm.internal.common.default import DefaultMeasurement


class Util(object):
    def __init__(self):
        return

    # 检测初始化 tccm-client 时传入的 business_name
    def check_business_name(self, business_name):
        if len(business_name) > DefaultMeasurement.DefaultBusinessNameMaxLength:
            logging.error("The max length of businessName is ", DefaultMeasurement.DefaultBusinessNameMaxLength)
            raise NotImplementedError(u"The max length of businessName is.")
        # 业务 BusinessName 不允许有的字符 {",", "*", "?", "\"", "<", ">", "|", " ", "#", ":", "\\", "/", ";", "]"}
        invalid_business_name_set = set((",", "*", "?", "\"", "<", ">", "|", " ", "#", ":", "\\", "/", ";", "]"))
        for name in business_name:
            if name in invalid_business_name_set:
                logging.error("Business Name only supports numbers, letters, and underscores,inValid businessName:",
                              business_name)
                raise NotImplementedError(
                    u"Business Name only supports numbers, letters, and underscores,inValid businessName:")
        return True

    # 检验表名是否有非法字符，如果出现一律替换为下划线，且不修改原始的业务传入的字符串
    def escape_measurement(self, input_measurement):
        if len(input_measurement) <= 0:
            return DefaultMeasurement.DefaultMeasurementName
        if len(input_measurement) > DefaultMeasurement.DefaultBusinessNameMaxLength:
            return input_measurement[0:DefaultMeasurement.DefaultBusinessNameMaxLength]
        output_measurement = list(input_measurement)
        # 表名中不可出现的非法字符 {"|", ",", "*", "?", "<", ">", "#", ":", "\\", "/", ";", "]", "\"", " "}
        invalid_measurement_set = set(("|", ",", "*", "?", "<", ">", "#", ":", "\\", "/", ";", "]", "\"", " "))
        for measurement in output_measurement:
            if measurement in invalid_measurement_set:
                output_measurement[output_measurement.index(measurement)] = '_'

        return "".join(output_measurement)

    # 检验指标名和维度名，指标名和维度名只允许出现【字母、数字、点、下划线、中划线】，如果出现其他字符一律替换为下划线
    def escape_metric_name_and_tag(self, input_name):
        output_name = list(input_name)
        for name in output_name:
            if (not ((name >= '0') and (name <= '9'))) and (not ((name >= 'A') and (name <= 'Z'))) and (
                    not ((name >= 'a') and (name <= 'z'))) and (name != '.') and (name != '-') and (name != '_'):
                output_name[output_name.index(name)] = '_'
        return "".join(output_name)
