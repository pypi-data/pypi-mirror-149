from dg_sdk.merchant.module.merchant_info import MerchantInfo


class ZFTMerchantInfo(MerchantInfo):
    """
    直付通商户经营信息
    """
    name = ""
    cert_no = ""
    cert_type = ""
    contact_tag = ""
    contact_type = ""

    def __init__(self, name, mcc, cert_type, cert_no, service_phone, prov_id, area_id, district_id, detail_addr,
                 contact_name, contact_tag, contact_type, contact_mobile_no):
        """
        直付通商户经营信息
        :param name:进件的二级商户名称
        :param mcc:商户类别码mcc
        :param cert_type:商户证件类型
        :param cert_no:商户证件编号
        :param service_phone:客服电话
        :param prov_id:经营省
        :param area_id:经营市
        :param district_id:经营区
        :param detail_addr:经营详细地址
        :param contact_name:联系人姓名
        :param contact_tag:	商户联系人业务标识
        :param contact_type:联系人类型，取值范围：LEGAL_PERSON：法人；CONTROLLER：实际控制人；AGENT：代理人；OTHER：其他
        :param contact_mobile_no:联系人手机号
        """

        super().__init__(name, prov_id, area_id, district_id, detail_addr, contact_name, contact_mobile_no,
                         "", "", "", mcc, service_phone)

        self.name = name
        self.cert_no = cert_no
        self.cert_type = cert_type
        self.contact_tag = contact_tag
        self.contact_type = contact_type

    def obj_to_dict(self):
        return {
            "name": self.name,
            "mcc": self.mcc,
            "cert_no": self.cert_no,
            "cert_type": self.cert_type,
            "service_phone": self.service_phone,
            "prov_id": self.prov_id,
            "area_id": self.area_id,
            "district_id": self.district_id,
            "detail_addr": self.detail_addr,
            "contact_name": self.contact_name,
            "contact_tag": self.contact_tag,
            "contact_type": self.contact_type,
            "contact_mobile_no": self.contact_mobile_no
        }
