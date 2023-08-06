from dg_sdk.request_tools import request_post
from dg_sdk.merchant.alimerchant_api_urls import *
from dg_sdk.merchant.merchant_api_urls import add_cert_info
from dg_sdk.dg_client import DGClient
from typing import List
from dg_sdk.merchant.module.file_info import FileInfo
from dg_sdk.merchant.module.zft_merchant_info import ZFTMerchantInfo
from dg_sdk.merchant.module.zft_split_receiver import ZFTSplitReceiver
import json


class AliMerchant(object):

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
    def exchange_app_auth_token(cls, app_id, oper_type, **kwargs):
        """
        签约版-换取应用授权令牌
        :param oper_type: 0-换取令牌;1-刷新令牌
        :param app_id: 支付宝：开发者应用ID
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "oper_type": oper_type,
            "app_id": app_id,
        }

        required_params.update(kwargs)
        return request_post(exchange_app_auth_token, required_params)

    @classmethod
    def apply_face2face_sign(cls, upper_huifu_id, direct_category, app_id, account, contact_name, contact_mobile_no,
                             contact_email, file_list: List[FileInfo], **kwargs):
        """
        签约版-申请当面付代签约
        :param upper_huifu_id: 渠道商汇付Id
        :param direct_category: 经营类目
        :param app_id: 开发者的应用ID
        :param account: 商户账号
        :param contact_name: 联系人姓名
        :param contact_mobile_no: 联系人手机号
        :param contact_email: 联系人电子邮箱
        :param file_list: 文件列表
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
            "upper_huifu_id": upper_huifu_id,
            "direct_category": direct_category,
            "account": account,
            "contact_name": contact_name,
            "contact_mobile_no": contact_mobile_no,
            "contact_email": contact_email,
            "file_list": json.dumps(file_info_list)
        }
        required_params.update(kwargs)
        return request_post(apply_face_to_face_sign, required_params)

    @classmethod
    def query_apply_order_status(cls, app_id, **kwargs):
        """
        签约版-查询申请状态
        :param app_id: 开发者的应用ID
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
        }

        required_params.update(kwargs)
        return request_post(query_apply_order_status, required_params)

    @classmethod
    def zft_apply_register_mer(cls, merchant_info: ZFTMerchantInfo, service, sign_time_with_isv, default_settle_type,
                               file_list: List[FileInfo], **kwargs):
        """
        直付通-商户进件申请
        :param merchant_info: 商户经营信息
        :param service: 商户使用服务1：当面付、2：app支付、3：wap支付:4：电脑支付 多个英文逗号分隔
        :param sign_time_with_isv: 二级商户与服务商的签约时间格式:yyyy-MM-dd
        :param default_settle_type:默认结算类型bankCard/alipayAccount。bankCard表示结算到银行卡；alipayAccount表示结算到支付宝账号
        :param file_list:文件列表，附件资料列表fileList
        :param kwargs: 非必填额外参数
        :return:
        """
        file_info_list = []
        if file_list:
            for file in file_list:
                file_info_list.append(file.obj_to_dict())

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "service": service,
            "sign_time_with_isv": sign_time_with_isv,
            "default_settle_type": default_settle_type,
            "file_list": json.dumps(file_info_list)
        }
        required_params.update(merchant_info.obj_to_dict())
        required_params.update(kwargs)
        return request_post(reg_zft_mer_info, required_params)

    @classmethod
    def zft_split_config(cls, app_id, split_flag, receiver_list: List[ZFTSplitReceiver], status, **kwargs):
        """
        直付通-分账关系绑定&解绑
        :param app_id: 开发者的应用ID
        :param split_flag:分账开关1开通 2关闭
        :param receiver_list:分账接收方列表
        :param status:状态，0解绑 1绑定
        :param kwargs: 非必填额外参数
        :return:
        """
        zft_split_receiver_list = []
        if receiver_list:
            for receiver in receiver_list:
                zft_split_receiver_list.append(receiver.obj_to_dict())
        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "split_flag": split_flag,
            "status": status,
            "zft_split_receiver_list": json.dumps(zft_split_receiver_list)
        }

        required_params.update(kwargs)
        return request_post(config_zft_split_receiver, required_params)

    @classmethod
    def query_zft_split_config(cls, app_id, page_num, page_size, **kwargs):
        """
        直付通-分账关系查询
        :param app_id: 开发者的应用ID
        :param page_num: 页数起始页为 1
        :param page_size:页面大小。每页记录数，取值范围是(0,100]
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "app_id": app_id,
            "page_num": page_num,
            "page_size": page_size
        }

        required_params.update(kwargs)
        return request_post(query_zft_split_receiver, required_params)
