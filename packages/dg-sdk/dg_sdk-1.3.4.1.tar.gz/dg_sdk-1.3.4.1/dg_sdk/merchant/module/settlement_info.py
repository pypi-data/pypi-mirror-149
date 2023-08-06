from dg_sdk.merchant.module.file_info import FileInfo
from typing import List


class SettlementInfo(object):
    """
    结算信息
    """
    settlement_id = ""
    qualification_type = ""
    activities_id = ""
    file_list = ""
    activities_rate = ""

    def __init__(self, settlement_id, qualification_type, file_list: List[FileInfo], activities_rate="",
                 activities_id=""):
        """
        结算配置信息
        :param settlement_id: 营业执照信息
        :param qualification_type: 法人手机号
        :param activities_id: 是否允许商户使用总部资质
        :param file_list: 文件列表
        :param activities_rate: 行业一级分类
        """

        self.settlement_id = settlement_id
        self.qualification_type = qualification_type
        self.activities_id = activities_id
        self.file_list = file_list
        self.activities_rate = activities_rate

    def obj_to_dict(self):
        result = {
            "qualification_type": self.qualification_type,
            "activities_id": self.activities_id,
            "activities_rate": self.activities_rate,
            "settlement_id": self.settlement_id
        }

        if self.file_list:
            file_info_list = []
            for file in self.file_list:
                file_info_list.append(file.obj_to_dict())
            result["file_list"] = file_info_list

        return result
