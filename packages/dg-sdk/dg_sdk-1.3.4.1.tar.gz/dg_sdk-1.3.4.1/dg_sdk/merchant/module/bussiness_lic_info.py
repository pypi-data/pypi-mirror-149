class BussinessLicInfo(object):
    """
    营业执照信息
    """
    reg_name = ""
    ent_type = ""
    license_code = ""
    license_validity_type = ""
    license_begin_date = ""
    license_end_date = ""
    reg_prov_id = ""
    reg_area_id = ""
    reg_district_id = ""
    reg_detail = ""

    def __init__(self, reg_name, ent_type, license_code, license_validity_type, reg_prov_id, reg_area_id,
                 reg_district_id, reg_detail, license_begin_date, license_end_date=""):
        """
        营业执照信息
        :param reg_name: 商户名称
        :param ent_type: 公司类型，1:政府机构 2:国营企业 3:私营企业 4:外资企业 5:个体工商户 7:事业单位
        :param license_code: 营业执照编号
        :param license_validity_type: 营业执照有效期类型，1:长期有效 0:非长期有效
        :param license_begin_date: 营业执照有效期开始日期yyyyMMdd
        :param license_end_date: 营业执照有效期截止日期
        :param reg_prov_id: 注册省
        :param reg_area_id: 注册市
        :param reg_district_id: 注册区
        :param reg_detail: 注册详细地址
        """

        self.reg_name = reg_name
        self.ent_type = ent_type
        self.license_code = license_code
        self.license_validity_type = license_validity_type
        self.license_begin_date = license_begin_date
        self.license_end_date = license_end_date
        self.reg_prov_id = reg_prov_id
        self.reg_area_id = reg_area_id
        self.reg_district_id = reg_district_id
        self.reg_detail = reg_detail

    def obj_to_dict(self):
        return {
            "reg_name": self.reg_name,
            "ent_type": self.ent_type,
            "license_code": self.license_code,
            "license_validity_type": self.license_validity_type,
            "license_begin_date": self.license_begin_date,
            "license_end_date": self.license_end_date,
            "reg_prov_id": self.reg_prov_id,
            "reg_area_id": self.reg_area_id,
            "reg_district_id": self.reg_district_id,
            "reg_detail": self.reg_detail
        }
