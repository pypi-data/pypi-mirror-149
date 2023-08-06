class SettleConfigInfo(object):
    """
    结算配置信息
    """
    settle_cycle = ""
    min_amt = ""
    remained_amt = ""
    settle_abstract = ""
    out_settle_flag = ""
    out_settle_huifuid = ""
    out_settle_acct_type = ""
    fixed_ratio = ""
    settle_batch_no = ""

    def __init__(self, settle_cycle, min_amt="", remained_amt="", settle_abstract="", out_settle_flag="",
                 out_settle_huifuid="", out_settle_acct_type="", fixed_ratio="", settle_batch_no=""):
        """
        结算配置信息
        :param settle_cycle: 结算周期T1:下个工作日到账;D1:下个自然日到账
        :param min_amt: 起结金额整数最多14位，小数最多两位
        :param remained_amt: 留存金额
        :param settle_abstract: 结算摘要
        :param out_settle_flag: 手续费外扣标记1:外扣：结算时，从out_settle_huifuid账户扣手续费 2:内扣：从结算金额中扣手续费
        :param out_settle_huifuid: 结算手续费外扣时的汇付ID，out_settle_flag=1时必填
        :param out_settle_acct_type: 结算手续费外扣时的账户类型01-基本户05-充值户不填默认01
        :param fixed_ratio: 节假日结算手续费率T1时无意义，D1时节假日按此费率结算;整数最多14位，小数最多两位
        :param settle_batch_no: 结算批次号0(0点昨日余额结算批次),300(3点余额结算批次),600(6点余额结算批次),900(9点余额结算批次)
        """

        self.settle_cycle = settle_cycle
        self.min_amt = min_amt
        self.remained_amt = remained_amt
        self.settle_abstract = settle_abstract
        self.out_settle_flag = out_settle_flag
        self.out_settle_huifuid = out_settle_huifuid
        self.out_settle_acct_type = out_settle_acct_type
        self.fixed_ratio = fixed_ratio
        self.settle_batch_no = settle_batch_no

    def obj_to_dict(self):
        return {
            "settle_cycle": self.settle_cycle,
            "min_amt": self.min_amt,
            "remained_amt": self.remained_amt,
            "settle_abstract": self.settle_abstract,
            "out_settle_flag": self.out_settle_flag,
            "out_settle_huifuid": self.out_settle_huifuid,
            "out_settle_acct_type": self.out_settle_acct_type,
            "fixed_ratio": self.fixed_ratio,
            "settle_batch_no": self.settle_batch_no
        }
