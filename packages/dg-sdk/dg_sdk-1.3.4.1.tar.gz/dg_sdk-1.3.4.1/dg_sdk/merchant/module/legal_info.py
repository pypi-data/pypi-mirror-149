class LegalInfo(object):
    """
    法人信息
    """
    legal_name = ""
    legal_cert_type = ""
    legal_cert_no = ""
    legal_cert_validity_type = ""
    legal_cert_begin_date = ""
    legal_cert_end_date = ""

    def __init__(self, legal_name, legal_cert_type, legal_cert_no, legal_cert_validity_type, legal_cert_begin_date,
                 legal_cert_end_date=""):
        """
        法人信息
        :param legal_name: 法人姓名
        :param legal_cert_type: 法人证件类型00:身份证 01:护照 02:军官证 03:士兵证 04:回乡证 05:户口本 06:外国护照 07:其他
        08:暂住证 09:警官证 10:文职干部证 11:港澳同胞回乡证
        :param legal_cert_no: 法人证件号码
        :param legal_cert_validity_type: 法人证件有效期类型1:长期有效 0:非长期有效
        :param legal_cert_begin_date: 法人证件有效期开始日期 yyyyMMdd
        :param legal_cert_end_date: 法人证件有效期截止日期，长期有效可不填 yyyyMMdd
        """
        self.legal_name = legal_name
        self.legal_cert_type = legal_cert_type
        self.legal_cert_no = legal_cert_no
        self.legal_cert_validity_type = legal_cert_validity_type
        self.legal_cert_begin_date = legal_cert_begin_date
        self.legal_cert_end_date = legal_cert_end_date

    def obj_to_dict(self):
        return {
            "legal_name": self.legal_name,
            "legal_cert_type": self.legal_cert_type,
            "legal_cert_no": self.legal_cert_no,
            "legal_cert_validity_type": self.legal_cert_validity_type,
            "legal_cert_begin_date": self.legal_cert_begin_date,
            "legal_cert_end_date": self.legal_cert_end_date
        }
