from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import card_bind_apply, card_payment_confirm, card_payment_apply, \
    card_payment_page_pay, online_payment_query, online_payment_refund, online_payment_refund_query, \
    card_bind_confirm, card_un_bind, card_payment_sms, withhold_pay, customer_reg

from dg_sdk.dg_client import DGClient
from dg_sdk.pay.module.card import Card
from dg_sdk.pay.module.cert import Cert


class QuickAndHoldPay(object):
    """
    快捷支付与代扣相关接口，
    支付申请，首次四要素验证+发短信
    快捷支付确认
    快捷/代扣绑卡申请接口
    快捷/代扣绑卡确认接口
    快捷代扣解绑
    快捷代扣短信重发时使用
    快捷页面版
    代扣
    线上交易查询
    扫码交易列表查询
    退款
    退款查询
    线上快捷代扣用户注册接口
    """

    @classmethod
    def apply(cls,
              trans_amt,
              user_huifu_id,
              card_bind_id,
              notify_url,
              risk_check_data,
              terminal_device_data,
              extend_pay_data, **kwargs):
        """
        支付申请，首次四要素验证+发短信

        https://paas.huifu.com/partners/api/#/kuaijie/api_kjzfsq
        :param trans_amt: 交易金额
        :param user_huifu_id: 用户客户号
        :param card_bind_id: 绑卡ID
        :param notify_url: 异步通知地址#{http_server_url}，
        :param risk_check_data: 安全信息
        :param terminal_device_data: 设备数据
        :param extend_pay_data: 银行扩展字段
        :param kwargs: 非必填额外参数
        """
        required_params = {
            "transamt": trans_amt,
            "user_huifu_id": user_huifu_id,
            "card_bind_id": card_bind_id,
            "notify_url": notify_url,
            "risk_check_data": risk_check_data,
            "terminal_device_data": terminal_device_data,
            "extend_pay_data": extend_pay_data
        }
        required_params.update(kwargs)
        return request_post(card_payment_apply, required_params)

    @classmethod
    def bind_card(cls, order_id, order_date, card_info: Card, cert_info: Cert, **kwargs):
        """
        快捷/代扣绑卡申请接口
        :param order_id:订单号
        :param order_date:订单日期
        :param card_info:银行卡信息
        :param cert_info:证件信息
        :param kwargs: 非必填额外参数
        :return: 绑卡接口返回
        """
        required_params = {
            "order_id": order_id,
            "order_date": order_date,
            "card_id": card_info.card_id,
            "card_name": card_info.card_name,
            "cert_type": cert_info.cert_type,
            "cert_id": cert_info.cert_id,
            "cert_validity_type": cert_info.cert_validity_type,
            "cert_begin_date": cert_info.cert_begin_date,
            "cert_end_date": cert_info.cert_end_date,
            "card_mp": card_info.card_mp,
            "vip_code": card_info.vip_code,
            "expiration": card_info.expiration
        }
        required_params.update(kwargs)
        return request_post(card_bind_apply, required_params)

    @classmethod
    def bind_card_confirm(cls, order_id, order_date, out_cust_id, card_info: Card, cert_info: Cert,
                          **kwargs):
        """
        快捷/代扣绑卡确认接口
        :param order_id:订单号
        :param order_date:订单日期
        :param out_cust_id:顾客用户号
        :param card_info:银行卡信息
        :param cert_info:证件信息
        :param kwargs: 非必填额外参数
        :return: 绑卡接口返回
        """
        required_params = {
            "order_id": order_id,
            "order_date": order_date,
            "out_cust_id": out_cust_id,
            "card_id": card_info.card_id,
            "card_name": card_info.card_name,
            "card_mp": card_info.card_id,
            "vip_code": card_info.vip_code,
            "expiration": card_info.expiration,
            "cert_type": cert_info.cert_type,
            "cert_id": cert_info.cert_id,
            "cert_validity_type": cert_info.cert_validity_type,
            "cert_begin_date": cert_info.cert_begin_date,
            "cert_end_date": cert_info.cert_end_date,

        }
        required_params.update(kwargs)
        return request_post(card_bind_confirm, required_params)

    @classmethod
    def un_bind(cls, out_cust_id, token_no, **kwargs):
        """
        快捷/代扣解绑接口

        :param out_cust_id: 顾客用户号
        :param token_no: 卡令牌
        :param kwargs: 非必填额外参数
        :return: 解绑响应
        """
        required_params = {
            "out_cust_id": out_cust_id,
            "token_no": token_no
        }
        required_params.update(kwargs)
        return request_post(card_un_bind, required_params)

    @classmethod
    def confirm(cls, sms_code, req_date, req_seq_id, goods_desc, notify_url, **kwargs):
        """
        快捷支付确认

        https://paas.huifu.com/partners/api/#/kuaijie/api_kjzfqr
        :param sms_code: 短信验证码
        :param req_date: 原快捷支付申请请求时间
        :param goods_desc: 商品描述
        :param req_seq_id: 原快捷支付申请请求序列号
        :param notify_url: 异步通知地址
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "sms_code": sms_code,
            "goods_desc": goods_desc,
            "notify_url": notify_url,
            "req_date": req_date,
            "req_seq_id": req_seq_id
        }

        required_params.update(kwargs)
        return request_post(card_payment_confirm, required_params)

    @classmethod
    def sms_code(cls, out_cust_id, order_id, order_date, **kwargs):
        """
        快捷代扣短信重发(v1)
        :param out_cust_id: 顾客用户号
        :param order_id:订单号
        :param order_date:订单日期
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "out_cust_id": out_cust_id,
            "order_id": order_id,
            "order_date": order_date,
        }
        required_params.update(kwargs)
        return request_post(card_payment_sms, required_params)

    @classmethod
    def page(cls, trans_amt, notify_url, terminal_device_data, extend_pay_data, risk_check_data, **kwargs):
        """
        快捷支付页面版

        https://paas.huifu.com/partners/api/#/kuaijie/api_kjweb
        :param trans_amt: 交易金额
        :param notify_url: 异步通知地址
        :param terminal_device_data: 设备信息
        :param extend_pay_data:银行扩展信息
        :param risk_check_data: 安全信息
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "trans_amt": trans_amt,
            "notify_url": notify_url,
            "terminal_device_data": terminal_device_data,
            "extend_pay_data": extend_pay_data,
            "risk_check_data": risk_check_data
        }
        required_params.update(kwargs)
        return request_post(card_payment_page_pay, required_params)

    @classmethod
    def with_hold_pay(cls, trans_amt, card_bind_id, goods_desc, user_huifu_id, risk_check_data, **kwargs):
        """
        代扣
        :param trans_amt: 交易金额
        :param card_bind_id: 绑卡ID
        :param goods_desc: 商品描述
        :param user_huifu_id: 用户客户号
        :param risk_check_data: 安全信息
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "trans_amt": trans_amt,
            "card_bind_id": card_bind_id,
            "goods_desc": goods_desc,
            "user_huifu_id": user_huifu_id,
            "risk_check_data": risk_check_data
        }
        required_params.update(kwargs)
        return request_post(withhold_pay, required_params)

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", pay_type="", **kwargs):
        """
        线上交易查询接口
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

        return request_post(online_payment_query, required_params)

    @classmethod
    def refund(cls, ord_amt, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上退款接口
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
    def customer_reg(cls, name, cert_type, cert_no, cert_validity_type, cert_begin_date, cert_end_date, mobile_no,
                     expand_id, **kwargs):
        """
        线上快捷代扣用户注册接口
        :param name: 个人姓名
        :param cert_type: 证件类型
        :param cert_no: 个人证件号
        :param cert_validity_type: 个人证件有效期类型
        :param cert_begin_date: 个人证件有效期起始日
        :param cert_end_date: 个人证件有效期到期日
        :param mobile_no: 手机号
        :param expand_id: 扩展方字段
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "name": name,
            "cert_type": cert_type,
            "cert_no": cert_no,
            "cert_validity_type": cert_validity_type,
            "cert_begin_date": cert_begin_date,
            "cert_end_date": cert_end_date,
            "mobile_no": mobile_no,
            "expand_id": expand_id
        }
        required_params.update(kwargs)
        return request_post(customer_reg, required_params)
