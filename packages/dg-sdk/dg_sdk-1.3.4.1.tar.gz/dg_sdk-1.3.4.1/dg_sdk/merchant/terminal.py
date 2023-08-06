from dg_sdk.request_tools import request_post
from dg_sdk.dg_client import DGClient
from dg_sdk.merchant.terminal_api_urls import *


class Terminal(object):
    """
    终端设备
    """

    @classmethod
    def add(cls, **kwargs):
        """
        新增终端设备

        https://paas.huifu.com/partners/api/#/zdsb/api_zdbb_xzzd
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
        }
        required_params.update(kwargs)
        return request_post(add_terminal, required_params)

    @classmethod
    def cancel(cls, device_id, **kwargs):
        """
        注销终端设备

        https://paas.huifu.com/partners/api/#/zdsb/api_zdbb_zxzd
        :param device_id: 每页条数
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "device_id": device_id
        }
        required_params.update(kwargs)
        return request_post(cancel_terminal, required_params)

    @classmethod
    def query_list(cls, device_id="", page_size="10", page_num="1", **kwargs):
        """
        绑定终端查询

        https://paas.huifu.com/partners/api/#/zdsb/api_zdbb_bdzdxxcx
        :param device_id: 订单号
        :param page_size: 分页条数，最大50，最小1
        :param page_num: 分页页码，不传则默认为第1页
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "device_id": device_id,
            "product_id": DGClient.mer_config.product_id,
            "page_size": page_size,
            "page_num": page_num
        }
        required_params.update(kwargs)
        return request_post(query_list, required_params)
