from dg_sdk.dg_client import DGClient
from dg_sdk.core.rsa_utils import rsa_long_encrypt


class BankCard(object):
    """
    代发银行卡片对象
    """
    bank_account_name = ""  # 银行卡用户名
    bank_card_no_crypt = ""  # 银行账号
    bank_code = ""  # 银行编号
    card_acct_type = ""  # 对公对私标识
    province = ""  # 省份
    area = ""  # 地区

    def __init__(self, bank_account_name, bank_card_no, bank_code, card_acct_type, province, area):
        """
        代发银行卡片对象
        :param bank_account_name: 银行卡用户名
        :param bank_card_no: 银行账号
        :param bank_code: 银行编号
        :param card_acct_type: 对公对私标识
        :param province: 省份
        :param area: 地区
        """

        self.bank_account_name = bank_account_name
        self.bank_code = bank_code
        self.bank_card_no_crypt = rsa_long_encrypt(bank_card_no, DGClient.mer_config.public_key)
        self.card_acct_type = card_acct_type
        self.province = province
        self.area = area
