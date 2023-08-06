class MerConfig(object):
    """
    商户配置信息
    """
    private_key = ""
    public_key = ""
    product_id = ""
    sys_id = ""
    huifu_id = ""

    def __init__(self, private_key, public_key, sys_id, product_id, huifu_id):
        """
        商户配置信息初始化
        :param private_key: 商户私钥，发送请求时加签时使用
        :param public_key: 汇付公钥，返回报文时用来验签
        :param sys_id: 系统号
        :param product_id: 产品号
        :param huifu_id: 商户号，
        """
        self.product_id = product_id
        self.private_key = private_key
        self.public_key = public_key
        self.sys_id = sys_id
        self.huifu_id = huifu_id
