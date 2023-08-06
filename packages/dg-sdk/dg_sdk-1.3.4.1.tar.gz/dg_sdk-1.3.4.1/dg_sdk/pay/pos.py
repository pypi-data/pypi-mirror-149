from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import card_trade_query


class POS(object):
    """
    POS 机交易
    """

    @classmethod
    def query(cls, trans_date, order_type, trade_terminal_device_data, *, out_order_id="", req_seq_id="", **kwargs):
        """
        银行卡交易查询接口
        https://paas.huifu.com/partners/api/#/znapp/zn_term_xt_yhkjyxqcx
        :param trans_date: 交易日期
        :param order_type: 订单类型
        :param trade_terminal_device_data: 交易终端设备数据
        :param out_order_id: 外部交易订单号
        :param req_seq_id: 终端交易订单号
        :param kwargs:  非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "trans_date": trans_date,
            "order_type": order_type,
            "out_order_id": out_order_id,
            "req_seq_id": req_seq_id,
            "trade_terminal_device_data": trade_terminal_device_data,
        }

        required_params.update(kwargs)
        return request_post(card_trade_query, required_params, need_seq_id=False)
