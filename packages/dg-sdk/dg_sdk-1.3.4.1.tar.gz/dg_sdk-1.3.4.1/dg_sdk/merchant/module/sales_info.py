from typing import List
from dg_sdk.merchant.module.file_info import FileInfo


class SalesInfo(object):
    """
    经营场景信息
    """
    biz_store_name = ""
    biz_address_code = ""
    biz_store_address = ""
    biz_sub_appid = ""
    mp_appid = ""
    mp_sub_appid = ""
    mini_program_appid = ""
    mini_program_sub_appid = ""
    app_appid = ""
    app_sub_appid = ""
    domain = ""
    file_list = ""
    web_appid = ""
    sub_corp_id = ""

    def __init__(self, biz_store_name, biz_address_code, biz_store_address, biz_sub_appid, mp_appid, mp_sub_appid,
                 mini_program_appid="", mini_program_sub_appid="", app_appid="", app_sub_appid="", domain="",
                 file_list: List[FileInfo] = None, web_appid="", sub_corp_id=""):
        """
        结算配置信息
        :param biz_store_name: 门店名称
        :param biz_address_code: 门店省市编码
        :param biz_store_address: 门店地址
        :param biz_sub_appid: 线下场所对应的商家APPID
        :param mp_appid: 服务商公众号APPID
        :param mp_sub_appid: 商家公众号APPID
        :param mini_program_appid: 服务商小程序APPID
        :param mini_program_sub_appid: 商家小程序APPID
        :param app_appid: 服务商应用APPID
        :param app_sub_appid: 商家应用APPID
        :param domain: 互联网网站域名
        :param file_list: 文件列表
        :param web_appid: 互联网网站对应的商家APPID
        :param sub_corp_id: 商家企业微信CorpID
        """

        self.biz_store_name = biz_store_name
        self.biz_address_code = biz_address_code
        self.biz_store_address = biz_store_address
        self.biz_sub_appid = biz_sub_appid
        self.mp_appid = mp_appid
        self.mp_sub_appid = mp_sub_appid
        self.mini_program_appid = mini_program_appid
        self.mini_program_sub_appid = mini_program_sub_appid
        self.app_appid = app_appid
        self.app_sub_appid = app_sub_appid
        self.domain = domain
        self.file_list = file_list
        self.web_appid = web_appid
        self.sub_corp_id = sub_corp_id

    def obj_to_dict(self):

        result = {
            "biz_store_name": self.biz_store_name,
            "biz_address_code": self.biz_address_code,
            "biz_store_address": self.biz_store_address,
            "biz_sub_appid": self.biz_sub_appid,
            "mp_appid": self.mp_appid,
            "mp_sub_appid": self.mp_sub_appid,
            "mini_program_appid": self.mini_program_appid,
            "mini_program_sub_appid": self.mini_program_sub_appid,
            "app_appid": self.app_appid,
            "app_sub_appid": self.app_sub_appid,
            "domain": self.domain,
            "web_appid": self.web_appid,
            "sub_corp_id": self.sub_corp_id
        }

        if self.file_list:
            file_info_list = []
            for file in self.file_list:
                file_info_list.append(file.obj_to_dict())
            result["file_list"] = file_info_list

        return result
