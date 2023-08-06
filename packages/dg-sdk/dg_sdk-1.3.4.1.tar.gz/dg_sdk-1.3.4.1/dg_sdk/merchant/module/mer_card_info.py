class MerCardInfo(object):
    """
    卡信息
    """
    card_type = ""
    card_name = ""
    card_no = ""
    prov_id = ""
    area_id = ""
    bank_code = ""
    branch_code = ""
    branch_name = ""
    cert_type = ""
    cert_no = ""
    cert_validity_type = ""
    cert_begin_date = ""
    cert_end_date = ""
    mp = ""

    def __init__(self, card_type, card_name, card_no, prov_id, area_id,
                 bank_code="", branch_code="", branch_name="", cert_type="", cert_no="", cert_validity_type="",
                 cert_begin_date="", cert_end_date="", mp=""):
        """
        卡信息
        :param card_type: 卡类型0:对公 1：对私法人 2：对私非法人
        :param card_name: 卡户名
        :param card_no: 卡号
        :param prov_id: 银行所在省
        :param area_id: 银行所在市
        :param bank_code: 银行号
        :param branch_code: 支行联行号
        :param branch_name: 支行名称
        :param cert_type: 持卡人证件类型00:身份证 01:护照 02:军官证 03:士兵证 04:回乡证 05:户口本 06:外国护照 07:其他
        08:暂住证 09:警官证 10:文职干部证 11:港澳同胞回乡证
        :param cert_no: 持卡人证件号码
        :param cert_validity_type: 持卡人证件有效期类型，1:长期有效 0:非长期有效
        :param cert_begin_date: 持卡人证件有效期（起始）YYYYMMDD
        :param cert_end_date: 持卡人证件有效期（截止），长期有效可不填
        :param mp: 银行卡绑定手机号
        """

        self.card_type = card_type
        self.card_name = card_name
        self.card_no = card_no
        self.prov_id = prov_id
        self.area_id = area_id
        self.bank_code = bank_code
        self.branch_code = branch_code
        self.branch_name = branch_name
        self.cert_type = cert_type
        self.cert_no = cert_no
        self.cert_validity_type = cert_validity_type
        self.cert_begin_date = cert_begin_date
        self.cert_end_date = cert_end_date
        self.mp = mp

    def obj_to_dict(self):
        return {
            "card_type": self.card_type,
            "card_name": self.card_name,
            "card_no": self.card_no,
            "prov_id": self.prov_id,
            "area_id": self.area_id,
            "bank_code": self.bank_code,
            "branch_code": self.branch_code,
            "branch_name": self.branch_name,
            "cert_type": self.cert_type,
            "cert_no": self.cert_no,
            "cert_validity_type": self.cert_validity_type,
            "cert_begin_date": self.cert_begin_date,
            "cert_end_date": self.cert_end_date,
            "mp": self.mp
        }
