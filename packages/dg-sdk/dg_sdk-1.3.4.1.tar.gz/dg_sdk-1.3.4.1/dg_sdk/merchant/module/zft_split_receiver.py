class ZFTSplitReceiver(object):
    """
    分账接收方
    """
    split_type = ""
    account = ""
    name = ""
    memo = ""

    def __init__(self, split_type, account, name="", memo=""):
        """
        分账接收方
        :param split_type: 文件类型
        :param account: 文件ID
        :param name: 文件名称
        :param memo: 分账关系描述
        """
        self.split_type = split_type
        self.account = account
        self.name = name
        self.memo = memo

    def obj_to_dict(self):
        return {
            "split_type": self.split_type,
            "account": self.account,
            "name": self.name,
            "memo": self.memo
        }
