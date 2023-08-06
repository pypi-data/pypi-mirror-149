from dg_sdk.request_tools import request_post
from dg_sdk.merchant.member_api_urls import *
from dg_sdk.dg_client import DGClient
from dg_sdk.merchant.module.legal_info import LegalInfo
from dg_sdk.merchant.module.bussiness_lic_info import BussinessLicInfo


class Member(object):
    """
    分账用户对象，包含以下接口
    企业用户基本信息注册
    个人用户基本信息注册
    查询账户信息
    企业用户基本信息修改
    个人用户基本信息修改
    用户业务入驻
    用户详情查询
    """

    @classmethod
    def create_enterprise(cls, short_name,
                          lic_info: BussinessLicInfo,
                          legal_info: LegalInfo,
                          contact_name,
                          contact_mobile,
                          **kwargs):
        """
        企业用户基本信息开户
        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_qyyhjbxxzc
        :param short_name: 企业用户名称
        :param lic_info: 营业执照信息
        :param legal_info: 法人信息
        :param contact_name: 联系人姓名
        :param contact_mobile:联系人手机号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "short_name": short_name,
            "contact_name": contact_name,
            "contact_mobile": contact_mobile
        }

        if lic_info:
            required_params.update(lic_info.obj_to_dict())
        if legal_info:
            required_params.update(legal_info.obj_to_dict())
        required_params.update(kwargs)
        return request_post(reg_usr_ent_base_info, required_params)

    @classmethod
    def create_individual(cls, name,
                          cert_type,
                          cert_no,
                          cert_validity_type,
                          cert_begin_date,
                          mobile_no,
                          cert_end_date="",
                          **kwargs):
        """
        个人用户基本信息开户

        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_gryhjbxxzc
        :param name: 个人姓名
        :param cert_type: 个人证件类型
        :param cert_no: 个人证件号码
        :param cert_validity_type: 个人证件有效期类型
        :param cert_begin_date:个人证件有效期开始日期
        :param mobile_no: 手机号
        :param cert_end_date: 个人证件有效期截止日期
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "name": name,
            "cert_type": cert_type,
            "cert_no": cert_no,
            "cert_validity_type": cert_validity_type,
            "cert_begin_date": cert_begin_date,
            "mobile_no": mobile_no,
            "cert_end_date": cert_end_date
        }

        required_params.update(kwargs)
        return request_post(reg_usr_indv_base_info, required_params)

    @classmethod
    def modify_enter_base_info(cls, **kwargs):
        """
        企业用户基本信息修改

        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_qyyhjbxxxg
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {

        }

        required_params.update(kwargs)
        return request_post(modify_usr_ent_base_info, required_params)

    @classmethod
    def modify_individual_base_info(cls, **kwargs):
        """
        个人用户基本信息修改

        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_gryhjbxxxg
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {

        }

        required_params.update(kwargs)
        return request_post(modify_use_indv_base_info, required_params)

    @classmethod
    def reg_busi_info(cls, upper_huifu_id, **kwargs):
        """
        用户业务入驻

        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_ywrz
        :param upper_huifu_id: 渠道商汇付Id
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "upper_huifu_id": upper_huifu_id
        }
        required_params.update(kwargs)
        return request_post(reg_usr_busi_info, required_params)

    @classmethod
    def query_user_detail(cls, **kwargs):
        """
        用户业务查询
        https://paas.huifu.com/partners/api/#/yhgl/api_yhgl_yhywcx
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
        }
        required_params.update(kwargs)
        return request_post(query_user_detail, required_params)
