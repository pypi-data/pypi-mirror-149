from dg_sdk.request_tools import request_post
from dg_sdk.merchant.huabei_api_urls import *
from dg_sdk.dg_client import DGClient
from typing import List
from dg_sdk.merchant.module.file_info import FileInfo
import json


class Huabei(object):

    @classmethod
    def add_ali_cert_info(cls, app_id, file_list: List[FileInfo], **kwargs):
        """
        支付宝间连证书上传

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_hbjlzssc
        :param app_id: 支付宝：开发者应用ID，微信：服务商的APPID
        :param file_list: 证书文件列表
        :param kwargs: 非必填额外参数
        :return:
        """

        file_info_list = []
        if file_list:
            for file in file_list:
                file_info_list.append(file.obj_to_dict())

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "file_list": json.dumps(file_info_list)
        }

        required_params.update(kwargs)
        return request_post(add_cert_url, required_params)

    @classmethod
    def create_pcredit_solution(cls, activity_name, start_time, end_time, min_money_limit, max_money_limit,
                                amount_budget, install_num_str_list, budget_warning_money, budget_warning_mail_list,
                                budget_warning_mobile_no_list, **kwargs):
        """
        创建花呗分期商家贴息方案

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_cjhbfa
        :param activity_name: 花呗分期商家贴息活动名称
        :param start_time: 活动开始时间示例值:2019-07-08 00:00:00
        :param end_time: 活动结束时间，必须大于start_time，且结束时间必须晚于当前时间示例值: 2029-07-10 00:00:00
        :param min_money_limit: 免息金额下限
        :param max_money_limit: 免息金额上限
        :param amount_budget: 花呗分期贴息预算金额
        :param install_num_str_list: 花呗分期数集合，不同期数之间用逗号分开示例值:[“3”,”6”,”12”,”24”]
        :param budget_warning_money: 预算提醒金额
        :param budget_warning_mail_list:预算提醒邮件列表
        :param budget_warning_mobile_no_list: 预算提醒手机号列表
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "activity_name": activity_name,
            "start_time": start_time,
            "end_time": end_time,
            "min_money_limit": min_money_limit,
            "max_money_limit": max_money_limit,
            "amount_budget": amount_budget,
            "install_num_str_list": install_num_str_list,
            "budget_warning_money": budget_warning_money,
            "budget_warning_mail_list": budget_warning_mail_list,
            "budget_warning_mobile_no_list": budget_warning_mobile_no_list
        }
        required_params.update(kwargs)
        return request_post(create_solution, required_params)

    @classmethod
    def modify_solution_status(cls, solution_id, status, **kwargs):
        """
        上架/下架花呗分期贴息

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_hbfasxj
        :param solution_id:贴息方案实例id 创建花呗分期商家贴息接口 的返参solution_id，
        :param status: 状态控制
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "solution_id": solution_id,
            "status": status
        }

        required_params.update(kwargs)
        return request_post(modify_solution_status, required_params)

    @classmethod
    def modify_pcredit_solution(cls, app_id, solution_id, start_time, end_time, **kwargs):
        """
        更新花呗分期商家贴息方案

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_hbfqfagx
        :param solution_id:贴息方案实例id 创建花呗分期商家贴息接口 的返参solution_id，
        :param app_id: 开发者的应用ID
        :param start_time: 开发者的应用ID
        :param end_time: 开发者的应用ID
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "solution_id": solution_id,
            "app_id": app_id,
            "start_time": start_time,
            "end_time": end_time
        }

        required_params.update(kwargs)
        return request_post(modify_solution, required_params)

    @classmethod
    def query_hb_solution(cls, solution_id, start_time, end_time, **kwargs):
        """
        查询花呗分期贴息账单

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_hbfacx
        :param solution_id:贴息方案实例id 创建花呗分期商家贴息接口 的返参solution_id，
        :param start_time: 开发者的应用ID
        :param end_time: 开发者的应用ID
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "solution_id": solution_id,
            "start_time": start_time,
            "end_time": end_time
        }

        required_params.update(kwargs)
        return request_post(query_solution, required_params)

    @classmethod
    def query_hb_activity(cls, solution_id, **kwargs):
        """
        花呗活动详情查询

        https://paas.huifu.com/partners/api/#/hfq/api_hfq_hbhdxqcx
        :param solution_id:贴息方案实例id 创建花呗分期商家贴息接口 的返参solution_id，
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "solution_id": solution_id
        }
        required_params.update(kwargs)
        return request_post(query_act_detail, required_params)
