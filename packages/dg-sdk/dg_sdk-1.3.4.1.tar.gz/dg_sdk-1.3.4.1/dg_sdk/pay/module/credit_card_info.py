from dg_sdk.dg_client import DGClient
from dg_sdk.core.rsa_utils import rsa_long_encrypt


class CreditCardInfo(object):
    """
    银行卡分期卡片对象
    """
    bank_card_mobile_no = ""  # 银行卡手机号
    bank_card_no = ""  # 银行卡号
    card_name = ""  # 持卡人姓名
    certificate_no = ""  # 证件号
    certificate_type = ""  # 证件类型
    bank_no = ""  # 银行编号
    card_act_type = ""  # 银行账户类型， E：对公，P：对私
    card_type = ""  # 卡类型，D:借记卡 C:信用卡 P:存折 Y:预付费卡 V:虚拟账户 Z:借贷合一卡
    cvv2 = ""  # cvv2
    valid_date = ""  # 有效期

    def __init__(self, bank_card_mobile_no, bank_card_no, card_name, certificate_no, certificate_type, bank_no="",
                 card_act_type="", card_type="", cvv2="", valid_date=""):
        """
        银行卡分期卡片对象
        :param bank_card_mobile_no: 银行卡手机号
        :param bank_card_no: 银行卡号
        :param card_name: 持卡人姓名
        :param certificate_no: 证件号
        :param certificate_type: 证件类型
        :param bank_no: 银行编号
        :param card_act_type: 银行账户类型， E：对公，P：对私
        :param card_type:  卡类型，D:借记卡 C:信用卡 P:存折 Y:预付费卡 V:虚拟账户 Z:借贷合一卡
        :param cvv2: cvv2
        :param valid_date: 有效期
        """
        self.bank_card_mobile_no = rsa_long_encrypt(bank_card_mobile_no, DGClient.mer_config.public_key)
        self.bank_card_no = rsa_long_encrypt(bank_card_no, DGClient.mer_config.public_key)
        self.certificate_no = rsa_long_encrypt(certificate_no, DGClient.mer_config.public_key)
        self.cvv2 = rsa_long_encrypt(cvv2, DGClient.mer_config.public_key)
        self.valid_date = rsa_long_encrypt(valid_date, DGClient.mer_config.public_key)
        self.card_name = card_name
        self.certificate_type = certificate_type
        self.bank_no = bank_no
        self.card_act_type = card_act_type
        self.card_type = card_type
