from dg_sdk.dg_client import DGClient
from dg_sdk.core.rsa_utils import rsa_long_encrypt


class Card(object):
    """
    银行卡片对象
    """
    card_id = ""  # 卡号
    card_name = ""  # 卡户姓名
    card_mp = ""  # 卡片手机号
    vip_code = ""  # 卡片安全码
    expiration = ""  # 卡片有效期

    def __init__(self, card_id, card_name, card_mp, vip_code="", expiration=""):
        self.card_id = rsa_long_encrypt(card_id, DGClient.mer_config.public_key)
        self.card_name = rsa_long_encrypt(card_name, DGClient.mer_config.public_key)
        self.card_mp = rsa_long_encrypt(card_mp, DGClient.mer_config.public_key)
        self.vip_code = rsa_long_encrypt(vip_code, DGClient.mer_config.public_key)
        self.expiration = rsa_long_encrypt(expiration, DGClient.mer_config.public_key)
