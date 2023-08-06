class MerchantInfo(object):
    """
    商户经营信息
    """
    short_name = ""
    prov_id = ""
    area_id = ""
    district_id = ""
    detail_addr = ""
    contact_name = ""
    contact_mobile_no = ""
    contact_email = ""
    service_phone = ""
    sms_send_flag = ""
    login_name = ""
    busi_type = ""
    receipt_name = ""
    mcc = ""

    def __init__(self, short_name, prov_id, area_id, district_id, detail_addr, contact_name, contact_mobile_no,
                 contact_email, busi_type, receipt_name, mcc, service_phone, sms_send_flag="", login_name=""):
        """
        商户经营信息
        :param short_name: 商户简称
        :param prov_id: 经营省
        :param area_id: 经营市
        :param district_id: 经营区
        :param detail_addr: 经营详细地址
        :param contact_name: 联系人姓名
        :param contact_mobile_no: 联系人手机号
        :param contact_email: 联系人电子邮箱
        :param service_phone: 客服电话
        :param sms_send_flag: 是否发送短信通知商户，默认否, 1：短信通知联系人手机号
        :param login_name: 管理员账号，自定义值，必须全网唯一；作为控台的登陆用户名POS机的登陆用户名；为空不生成。
        :param busi_type: 经营类型1:实体 2:虚拟
        :param receipt_name: 小票名称，可以作为POS小票的名称
        :param mcc: 所属行业（MCC）
        """

        self.short_name = short_name
        self.prov_id = prov_id
        self.area_id = area_id
        self.district_id = district_id
        self.detail_addr = detail_addr
        self.contact_name = contact_name
        self.contact_mobile_no = contact_mobile_no
        self.contact_email = contact_email
        self.service_phone = service_phone
        self.sms_send_flag = sms_send_flag
        self.login_name = login_name
        self.busi_type = busi_type
        self.receipt_name = receipt_name
        self.mcc = mcc

    def obj_to_dict(self):
        return {
            "short_name": self.short_name,
            "prov_id": self.prov_id,
            "area_id": self.area_id,
            "district_id": self.district_id,
            "detail_addr": self.detail_addr,
            "contact_name": self.contact_name,
            "contact_mobile_no": self.contact_mobile_no,
            "contact_email": self.contact_email,
            "service_phone": self.service_phone,
            "sms_send_flag": self.sms_send_flag,
            "login_name": self.login_name,
            "busi_type": self.busi_type,
            "receipt_name": self.receipt_name,
            "mcc": self.mcc,
        }
