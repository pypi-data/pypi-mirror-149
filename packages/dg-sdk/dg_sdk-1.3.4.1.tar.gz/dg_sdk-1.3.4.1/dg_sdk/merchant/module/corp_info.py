from dg_sdk.merchant.module.bussiness_lic_info import BussinessLicInfo
from dg_sdk.merchant.module.legal_info import LegalInfo
from dg_sdk.merchant.module.file_info import FileInfo
from typing import List


class CorpInfo(object):
    """
    企业信息
    """
    lic_info = ""
    legal_info = ""
    legal_mobile_no = ""
    allow_mer_use_chains_flag = ""
    file_list = ""
    category_one = ""
    category_two = ""

    def __init__(self, lic_info: BussinessLicInfo, legal_info: LegalInfo, legal_mobile_no, allow_mer_use_chains_flag,
                 file_list: List[FileInfo] = None, category_one="", category_two=""):
        """
        结算配置信息
        :param lic_info: 营业执照信息
        :param legal_info: 法人信息
        :param legal_mobile_no: 法人手机号
        :param allow_mer_use_chains_flag: 是否允许商户使用总部资质
        :param file_list: 文件列表
        :param category_one: 行业一级分类
        :param category_two: 行业二级分类
        """

        self.lic_info = lic_info
        self.legal_info = legal_info
        self.legal_mobile_no = legal_mobile_no
        self.allow_mer_use_chains_flag = allow_mer_use_chains_flag
        self.file_list = file_list
        self.category_one = category_one
        self.category_two = category_two

    def obj_to_dict(self):
        result = {
            "legal_mobile_no": self.legal_mobile_no,
            "allow_mer_use_chains_flag": self.allow_mer_use_chains_flag,
            "category_one": self.category_one,
            "category_two": self.category_two
        }
        result.update(self.lic_info.obj_to_dict())
        result.update(self.legal_info.obj_to_dict())

        if self.file_list:
            file_info_list = []
            for file in self.file_list:
                file_info_list.append(file.obj_to_dict())
            result["file_list"] = file_info_list

        return result
