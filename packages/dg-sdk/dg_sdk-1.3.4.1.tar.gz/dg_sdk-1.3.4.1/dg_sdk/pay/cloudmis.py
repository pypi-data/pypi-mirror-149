from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import card_trade_query


class Cloudmis(object):
    """
    智能终端mis接入
    """

    @classmethod
    def device_info(cls, device_id, json_data, **kwargs):
        """
        智能终端接入
        https://paas.huifu.com/partners/api/#/znmis/zn_sbtx
        :param device_id: 终端设备号
        :param json_data: 交易信息
        :param kwargs:  非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "device_id": device_id,
            "json_data": json_data,
        }
        required_params.update(kwargs)
        return request_post(card_trade_query, required_params, need_seq_id=False)
