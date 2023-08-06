from dg_sdk.request_tools import request_post
from dg_sdk.merchant.wxmerchant_api_urls import *
from dg_sdk.merchant.merchant_api_urls import add_cert_info
from dg_sdk.dg_client import DGClient
from typing import List
from dg_sdk.merchant.module.file_info import FileInfo
import json
from dg_sdk.merchant.module.sales_info import SalesInfo
from dg_sdk.merchant.module.settlement_info import SettlementInfo


class WXMerchant(object):
    """
    微信商户配置类，包含以下接口
    微信商户配置
    微信商户配置查询
    微信实名认证
    微信实名认证状态查询
    证书登记
    微信特约商户进件申请
    查询微信申请状态
    修改微信结算帐号
    查询微信结算账户
    微信关注配置
    微信关注配置查询
    """

    @classmethod
    def config(cls, fee_type, *, wx_woa_app_id="", wx_applet_app_id="", **kwargs):
        """
        微信商户配置

        https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_wxshpz
        :param fee_type: 业务开通类型
        :param wx_woa_app_id: 公众号支付Appid
        :param wx_applet_app_id: 微信小程序APPID
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "fee_type": fee_type,
            "wx_woa_app_id": wx_woa_app_id,
            "wx_applet_app_id": wx_applet_app_id,
            "product_id": DGClient.mer_config.product_id
        }
        required_params.update(kwargs)
        return request_post(config, required_params)

    @classmethod
    def query_config(cls, **kwargs):
        """
        微信商户配置查询

        https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_wxshpzcx
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "product_id": DGClient.mer_config.product_id,
        }
        required_params.update(kwargs)
        return request_post(query_config, required_params)

    @classmethod
    def realname(cls, name, mobile, id_card_number, **kwargs):
        """
        微信实名认证

        https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_wxsmrz
        :param name: 联系人姓名
        :param mobile: 联系人手机号
        :param id_card_number: 联系人身份证号码
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "name": name,
            "mobile": mobile,
            "id_card_number": id_card_number
        }
        required_params.update(kwargs)
        return request_post(apply_wx_real_name, required_params)

    @classmethod
    def query_realname_state(cls, **kwargs):
        """
        查询微信实名认证
        https://paas.huifu.com/partners/api/#/shgl/shjj/api_shjj_wxsmrzztcx
        :return:
        """

        required_params = {
        }
        required_params.update(kwargs)
        return request_post(query_apply_wx_real_name, required_params)

    @classmethod
    def add_cert_info(cls, pay_way, app_id, file_list: List[FileInfo], **kwargs):
        """
        证书登记
        :param pay_way: 开通类型 W:微信 A:支付宝
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
            "pay_way": pay_way,
            "app_id": app_id,
            "file_list": json.dumps(file_info_list)
        }

        required_params.update(kwargs)
        return request_post(add_cert_info, required_params)

    @classmethod
    def apply_register_mer(cls,
                           upper_huifu_id,
                           app_id,
                           mch_id,
                           owner,
                           sales_scenes_type,
                           sales_info: SalesInfo,
                           settlement_info: SettlementInfo,
                           **kwargs):
        """
        微信特约商户进件
        :param upper_huifu_id: 渠道商汇付Id
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param owner: 经营者/法人是否为受益人
        :param sales_scenes_type:  经营场景类型，多个以英文逗号分割，SALES_SCENES_STORE 公众号：SALES_SCENES_MP
        小程序：SALES_SCENES_MINI_PROGRAM 互联网：SALES_SCENES_WEB APP：SALES_SCENES_APP 企业微信：SALES_SCENES_WEWORK
        :param sales_info: 经营场景
        :param settlement_info: 结算信息
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "upper_huifu_id": upper_huifu_id,
            "mch_id": mch_id,
            "owner": owner,
            "sales_scenes_type": sales_scenes_type,
            "sales_info": sales_info.obj_to_dict(),
            "settlement_info": settlement_info.obj_to_dict()
        }

        required_params.update(kwargs)
        return request_post(apply_wx_special_mer_sign, required_params)

    @classmethod
    def query_apply_reg(cls, app_id, mch_id, **kwargs):
        """
        查询微信申请状态
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "mch_id": mch_id,
        }

        required_params.update(kwargs)
        return request_post(query_wx_special_mer_sign, required_params)

    @classmethod
    def modify_settlement_info(cls, app_id, mch_id, sub_mchid, account_type, account_bank, bank_address_code,
                               account_number, **kwargs):
        """
        修改微信结算帐号
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param sub_mchid: 特约商户号
        :param account_type: 账户类型
        :param account_bank: 开户银行
        :param bank_address_code: 开户银行省市编码
        :param account_number: 银行账号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "mch_id": mch_id,
            "sub_mchid": sub_mchid,
            "account_type": account_type,
            "account_bank": account_bank,
            "bank_address_code": bank_address_code,
            "account_number": account_number,
        }

        required_params.update(kwargs)
        return request_post(modify_wx_settle_info, required_params)

    @classmethod
    def query_settlement_info(cls, app_id, mch_id, sub_mchid, **kwargs):
        """
        查询微信结算账户
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param sub_mchid: 特约商户号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "mch_id": mch_id,
            "sub_mchid": sub_mchid
        }

        required_params.update(kwargs)
        return request_post(query_wx_settle_info, required_params)

    @classmethod
    def subscribe_config(cls, app_id, mch_id, sub_mchid, **kwargs):
        """
        微信关注配置
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param sub_mchid: 特约商户号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "mch_id": mch_id,
            "sub_mchid": sub_mchid
        }

        required_params.update(kwargs)
        return request_post(wx_subscribe_config, required_params)

    @classmethod
    def query_subscribe_config(cls, app_id, mch_id, sub_mchid, **kwargs):
        """
        查询微信关注配置
        :param app_id: 开发者的应用ID,服务商的APPID
        :param mch_id: 服务商的商户号
        :param sub_mchid: 特约商户号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "mch_id": mch_id,
            "sub_mchid": sub_mchid
        }

        required_params.update(kwargs)
        return request_post(query_wx_subscribe_config, required_params)
