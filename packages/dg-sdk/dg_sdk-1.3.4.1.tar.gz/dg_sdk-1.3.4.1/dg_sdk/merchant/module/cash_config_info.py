class CashConfigInfo(object):
    """
    取现配置
    """
    cash_type = ""
    fix_amt = ""
    fee_rate = ""

    def __init__(self, cash_type="", fix_amt="", fee_rate=""):
        """
        结算配置信息
        :param cash_type: 业务类型D0:当日到账;T1:下个工作日到账;D1:下个自然日到账
        :param fix_amt: 提现手续费（固定/元）开通提现业务时必须填写一种收费方式
        :param fee_rate: 费率（百分比/%）开通提现业务时必须填写一种收费方式
        """

        self.cash_type = cash_type
        self.fix_amt = fix_amt
        self.fee_rate = fee_rate

    def obj_to_dict(self):
        return {
            "cash_type": self.cash_type,
            "fix_amt": self.fix_amt,
            "fee_rate": self.fee_rate
        }
