from dg_sdk.request_tools import request_post
from dg_sdk.merchant.member_api_urls import *
from dg_sdk.merchant.module.legal_info import LegalInfo
from dg_sdk.merchant.module.bussiness_lic_info import BussinessLicInfo


class SettleAccount(object):
    """
    结算对象，包含以下接口
    创建结算账户对象
    删除结算账户对象
    查询结算配置记录
    结算记录分页查询接口
    """

    # TODO
    @classmethod
    def create(cls, reg_name,
               lic_info: BussinessLicInfo,
               legal_info: LegalInfo,
               contact_name,
               contact_mobile_no,
               **kwargs):
        """
        创建结算账户对象
        :param reg_name: 企业用户名称
        :param lic_info: 营业执照信息
        :param legal_info: 法人信息
        :param contact_name: 联系人姓名
        :param contact_mobile_no:联系人手机号
        :param kwargs: 非必填额外参数
        :return:
        """

        required_params = {
            "reg_name": reg_name,
            "contact_name": contact_name,
            "contact_mobile_no": contact_mobile_no
        }

        if lic_info:
            required_params.update(lic_info.obj_to_dict())
        if legal_info:
            required_params.update(legal_info.obj_to_dict())
        required_params.update(kwargs)
        return request_post(reg_usr_ent_base_info, required_params)

    @classmethod
    def delete(cls, name,
               cert_type,
               cert_no,
               cert_validity_type,
               cert_begin_date,
               mobile_no,
               cert_end_date="",
               **kwargs):
        """
        删除结算账户对象
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
    def query_list(cls, name,
                   cert_type,
                   cert_no,
                   cert_validity_type,
                   cert_begin_date,
                   mobile_no,
                   cert_end_date="",
                   **kwargs):
        """
        查询结算配置记录
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

        # todo

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
    def query_settle_trans(cls, **kwargs):
        """
        结算记录分页查询接口
        :param kwargs: 非必填额外参数
        :return:
        """
        return request_post(modify_usr_ent_base_info, **kwargs)
