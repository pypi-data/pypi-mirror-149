# coding:utf-8
# -*- coding:utf-8 -*-

class BusinessInfo(object):
    def __init__(self, business_app_id=None, business_name=None, report_region=None):
        self.business_app_id = business_app_id
        self.business_name = business_name
        self.report_region = report_region

    # 设置业务信息
    def set_business_info(self, business_app_id, business_name, report_region):
        self.business_app_id = business_app_id
        self.business_name = business_name
        self.report_region = report_region
        return self

    # 获取业务信息 - -app_id
    def get_business_app_id(self):
        return self.business_app_id

    # 获取业务信息 - -namespace
    def get_business_name(self):
        return self.business_name

    # 获取业务信息 - -上报地域
    def get_report_region(self):
        return self.report_region
