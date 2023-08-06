from dg_sdk.request_tools import request_post
from dg_sdk.merchant.unipaymerchant_api_urls import *
from dg_sdk.dg_client import DGClient
from typing import List
from dg_sdk.merchant.module.file_info import FileInfo


class UniPayMerchant(object):

    @classmethod
    def apply_register_mer(cls, mer_type, legal_mobile, contract_id_no, file_list: List[FileInfo] = None, **kwargs):
        """
        云闪付活动商户入驻
        :param mer_type: 商户类型 MERCHANT_01-自然人; MERCHANT_02-个体工商户; MERCHANT_03-企业
        :param legal_mobile: 负责人手机号
        :param contract_id_no: 联系人身份证号
        :param file_list: 附件资料列表 fileList
        :param kwargs: 非必填额外参数
        :return:
        """

        file_info_list = []
        if file_list:
            for file in file_list:
                file_info_list.append(file.obj_to_dict())

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "mer_type": mer_type,
            "legal_mobile": legal_mobile,
            "contract_id_no": contract_id_no,
            "file_list": file_info_list
        }

        required_params.update(kwargs)
        return request_post(reg_mer_base_info, required_params)

    @classmethod
    def query_apply_reg(cls, serial_no, **kwargs):
        """
        云闪付活动商户入驻状态查询
        :param serial_no: 工单号参考 云闪付活动商户入驻接口 的返参serial_no
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "serial_no": serial_no,
        }

        required_params.update(kwargs)
        return request_post(query_mer_reg_stat, required_params)

    @classmethod
    def query_mer_base_info(cls, mer_no, **kwargs):
        """
        云闪付活动商户详细信息查询
        :param mer_no: 渠道商汇付Id
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "mer_no": mer_no,
        }
        required_params.update(kwargs)
        return request_post(query_mer_base, required_params)

    @classmethod
    def query_activity_list(cls, **kwargs):
        """
        云闪付活动列表查询
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
        }

        required_params.update(kwargs)
        return request_post(query_act_list, required_params)

    @classmethod
    def enlist_activity(cls, activity_id, mer_no, **kwargs):
        """
        云闪付活动报名
        :param activity_id: 商户使用服务1：当面付、2：app支付、3：wap支付:4：电脑支付 多个英文逗号分隔
        :param mer_no: 二级商户与服务商的签约时间格式:yyyy-MM-dd
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "activity_id": activity_id,
            "mer_no": mer_no,
        }
        required_params.update(kwargs)
        return request_post(enlist_act, required_params)

    @classmethod
    def query_enlish_activity_status(cls, enlist_id="", serial_number="", **kwargs):
        """
        云闪付活动报名进度查询
        :param enlist_id: 报名编号，与serialNumber二选一
        :param serial_number:报名请求流水号，与enlistId二选一 报名时传递的reqSysId
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "enlist_id": enlist_id,
            "serial_number": serial_number,
        }

        required_params.update(kwargs)
        return request_post(query_en_list_act_stat, required_params)
