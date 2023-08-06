from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import online_payment_query, online_payment_refund, online_payment_refund_query, \
    union_app_pay, wap_pay, web_page, bank_pay_payer_query, bank_pay_bank_list
from dg_sdk.dg_client import DGClient
import json


class OnlinePayment(object):
    """
    线上交易相关接口，
    银联APP支付，
    网银支付页面版，
    手机网页支付，
    线上交易退款，
    线上交易退款查询，
    线上交易交易查询
    网银付款银行账户接口
    网银支付银行列表查询接口
    """

    @classmethod
    def web_page(cls, trans_amt, goods_desc, goods_short_name, gw_chnnl_tp, biz_tp, notify_url, **kwargs):
        """
        网银支付页面版

        https://paas.huifu.com/partners/api/#/wy/api_wypc
        :param trans_amt: 订单金额
        :param goods_desc: 商品描述
        :param goods_short_name: 商品简称
        :param gw_chnnl_tp 网关支付受理渠道
        :param biz_tp 商品名
        :param notify_url 通知地址
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "trans_amt": trans_amt,
            "goods_desc": goods_desc,
            "extend_pay_data": json.dumps({
                "goods_short_name": goods_short_name,
                "gw_chnnl_tp": gw_chnnl_tp,
                "biz_tp": biz_tp
            }),
            "product_id": DGClient.mer_config.product_id,
            "notify_url": notify_url
        }

        required_params.update(kwargs)
        return request_post(web_page, required_params)

    @classmethod
    def union_app_create(cls, trans_amt, **kwargs):
        """
        银联APP支付

        https://paas.huifu.com/partners/api/#/api_unionapp
        :param trans_amt: 交易金额，单位为元，（例如：100.00）
        :param kwargs:  非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "trans_amt": trans_amt,
        }

        required_params.update(kwargs)
        return request_post(union_app_pay, required_params)

    @classmethod
    def wap_page(cls, bank_card_no, front_url, trans_amt, **kwargs):
        """
        手机网页支付

        https://paas.huifu.com/partners/api/#/wy/api_wymobile
        :param bank_card_no: 银行卡号
        :param front_url: 前端跳转URL
        :param trans_amt: 交易金额
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "trans_amt": trans_amt,
            "bank_card_no": bank_card_no,
            "front_url": front_url,
        }

        required_params.update(kwargs)
        return request_post(wap_pay, required_params)

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", pay_type="", **kwargs):
        """
        线上交易查询接口

        https://paas.huifu.com/partners/api/#/api_xsjycx
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param pay_type: 原交易支付类型, 快捷支付传quick_pay
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
            "pay_type": pay_type
        }

        required_params.update(kwargs)

        return request_post(online_payment_query, required_params, need_seq_id=False)

    @classmethod
    def refund(cls, ord_amt, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上退款接口

        https://paas.huifu.com/partners/api/#/api_xsjytk
        :param ord_amt: 退款金额
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """

        required_params = {
            "ord_amt": ord_amt,
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }

        required_params.update(kwargs)

        return request_post(online_payment_refund, required_params)

    @classmethod
    def refund_query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上退款查询接口

        https://paas.huifu.com/partners/api/#/api_xsjytkcx
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始退款请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }
        required_params.update(kwargs)
        return request_post(online_payment_refund_query, required_params)

    @classmethod
    def payer_query(cls, org_req_date, org_req_seq_id, **kwargs):
        """
        网银付款银行账户查询接口

        https://paas.huifu.com/partners/api/#/wy/api_wyfkyhzhcx
        :param org_req_date: 原交易请求日期
        :param org_req_seq_id: 原交易请求流水号
        :param kwargs:
        :return:
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
        }
        required_params.update(kwargs)
        return request_post(bank_pay_payer_query, required_params)

    @classmethod
    def bank_list(cls, gate_type, order_type, **kwargs):
        """
        网银支付银行列表查询接口

        https://paas.huifu.com/partners/api/#/wy/api_wyzfyhlbcx
        :param gate_type: 网关支付类型 01：个人网关 02：企业网关
        :param order_type: 订单类型 P：支付 R：充值
        :param kwargs:
        :return:
        """
        required_params = {
            "gate_type": gate_type,
            "order_type": order_type,
        }
        required_params.update(kwargs)
        return request_post(bank_pay_bank_list, required_params)
